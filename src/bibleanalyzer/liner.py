#
# Copyright (c) 2021 by Kristoffer Paulsson <kristoffer.paulsson@talenten.se>.
#
# Permission to use, copy, modify, and/or distribute this software for any purpose with
# or without fee is hereby granted, provided that the above copyright notice and this
# permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO
# THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO
# EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
# DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
#     https://opensource.org/licenses/ISC
#
# SPDX-License-Identifier: ISC
#
# Contributors:
#     Kristoffer Paulsson - initial implementation
#
"""Parsing liner. Lines up the corpora parsings in a linear fashion and caches them for analysis."""
import re

from bibleanalyzer.util.model import PunctuationToken, WordToken, ChapterToken, VerseToken, DataEntry, SectionToken
from bibleanalyzer.util.transliterator import KoineTransliterator
from . import Processor, ProcessException
from .app import Application
from .grammar import Grammar
from bibleanalyzer.app.logging import Logger
from .loader import LoaderIterator, PickleLoaderIterator
from .util.morphology import Speech, TypeNoun
from .util.reference import BibleReferenceCounter

TOKEN_REGEX = r"""([᾽\w]+|[\W])"""
PUNCTUATION = ("·", ".", ",", ";", ":", "-")


class LinerIterator:

    def __init__(self, loader: LoaderIterator, book: str):
        self._loader = loader
        self._logger = Application.instance().logger
        self._counter = None
        self._book = book

    def _entry_iter(self):
        for item in self._loader:
            if not item.text:
                self._logger.warning(
                    "Verse {} {}:{} has not text".format(self._book.title(), self._counter.chapter, self._counter.verse))
                continue
            yield item

    def _chapter_iter(self, verse_first: bool):
        if not verse_first:
            yield SectionToken()

        for item in self._entry_iter():

            if item.chapter == 1 and item.verse == 1:
                yield ChapterToken(number=1)
                yield VerseToken(number=1)

            if item.chapter == (self._counter.chapter + 1):
                self._counter.increase_chapter()
                yield ChapterToken(number=item.chapter)
                yield VerseToken(number=item.verse)

                if item.chapter == 1 and item.verse == 1 and verse_first:
                    yield SectionToken()

                if not item.text:
                    continue

            if item.verse == (self._counter.verse + 1):
                self._counter.increase_verse()
                yield VerseToken(number=item.verse)

                if item.chapter == 1 and item.verse == 1 and verse_first:
                    yield SectionToken()

                if not item.text:
                    continue

            for token in self._tokenizer_iter(item):
                yield token

    def _token_iter(self, verse_first: bool = True):
        stack = list()
        idx = 0 if verse_first else 1
        for token in self._chapter_iter(verse_first):

            if isinstance(token, PunctuationToken):
                if token.diacritic in (".", ";"):
                    stack.append(token)
                    continue

            if stack and isinstance(token, (ChapterToken, VerseToken)):
                stack.append(token)
                continue

            if stack and isinstance(token, WordToken):
                if not verse_first:
                    yield stack[0]

                    if KoineTransliterator.contains_upper(token.word):
                        yield SectionToken()

                for item in stack[idx:]:
                    yield item

                if KoineTransliterator.contains_upper(token.word) and verse_first:
                    word = Grammar.classify(token)
                    if word.speech == Speech.NOUN and word.type == TypeNoun.PROPER:
                        yield SectionToken(level=-1)
                    else:
                        yield SectionToken(level=1)

                stack = list()
                yield token
                continue

            if stack:
                stack.append(token)
            else:
                yield token

        for item in stack:
            yield item

    def _tokenizer_iter(self, item: DataEntry):
        word_count = 0
        for match in re.findall(TOKEN_REGEX, item.text.replace("[", "").replace("]", "")):
            token = match.strip()
            if token:
                if token in PUNCTUATION:
                    yield PunctuationToken(diacritic=token)
                elif KoineTransliterator.koine_only(token):
                    word = item.words[word_count]

                    if KoineTransliterator.normalize(word.word).lower() != KoineTransliterator.normalize(token).lower():
                        raise ProcessException("Not the right word. {} {}".format(token, word.word))

                    word_count += 1
                    yield WordToken(word=token, lexeme=word.lexeme, grammar=word.grammar)
                else:
                    self._logger.warning("Token excluded: '{}'".format(token))
            elif match != " ":
                self._logger.debug("Match left untokenized: '{}'".format(match))

    def _proc_iter(self):
        for token in self._token_iter(False):
            yield token

    def __iter__(self):
        self._iter = self._proc_iter()
        self._counter = BibleReferenceCounter()
        return self

    def __next__(self):
        token = next(self._iter)
        if token:
            return token
        else:
            raise StopIteration()


class Liner(Processor):

    def __init__(self, logger: Logger):
        super().__init__(logger)
        self._linear = list()
        self._letters = set()
        self._stats = dict()
        self._verify = ""

    @property
    def linear(self) -> list:
        return self._linear

    @property
    def letters(self) -> set:
        return self._letters

    @property
    def stats(self) -> dict:
        return self._stats

    @property
    def verify(self) -> str:
        return self._verify.strip()

    def _stat(self, letters: str):
        for char in set(KoineTransliterator.expand(letters)):
            if char not in self._stats.keys():
                self._stats[char] = 1
            else:
                self._stats[char] += 1

    def process(self, data: list, book: str):
        for token in LinerIterator(PickleLoaderIterator(data, "one"), book):
            if isinstance(token, WordToken):
                self._letters |= set(token.word)
                self._stat(token.word)

            self._verify_token(token)
            self._linear.append(token)

    def _verify_token(self, token):
        if isinstance(token, WordToken):
            self._verify += " " + token.word
        elif isinstance(token, PunctuationToken):
            self._verify += token.diacritic
        elif isinstance(token, VerseToken):
            self._verify += "\n"
