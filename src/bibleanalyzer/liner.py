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
from .grammar import Grammar
from bibleanalyzer.app.logging import Logger
from .util.morphology import Speech, TypeNoun

TOKEN_REGEX = r"""([᾽\w]+|[\W])"""
PUNCTUATION = ("·", ".", ",", ";", ":", "-")


class Liner(Processor):

    def __init__(self, logger: Logger):
        super().__init__(logger)
        self._data = None

        self._verse = 0
        self._chapter = 0
        self._book = None

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

    def verse_dispenser(self):
        for item in self._data:
            if not item.text:
                self.logger.warning(
                    "Verse {} {}:{} has not text".format(self._book.title(), self._chapter, self._verse))
                continue
            yield item

    def chapter_iter(self, verse_first: bool):
        if not verse_first:
            yield SectionToken()

        for item in self.verse_dispenser():

            if item.chapter == (self._chapter + 1):
                self._chapter += 1
                self._verse = 0
                yield ChapterToken(number=item.chapter)

            if item.verse == (self._verse + 1):
                self._verse += 1
                yield VerseToken(number=item.verse)

                if item.chapter == 1 and item.verse == 1 and verse_first:
                    yield SectionToken()

                if not item.text:
                    continue

            for token in self.tokenizer_iter(item):
                yield token

    def token_iter(self, verse_first: bool = True):
        stack = list()
        idx = 0 if verse_first else 1
        for token in self.chapter_iter(verse_first):

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

    def tokenizer_iter(self, item: DataEntry):
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
                    self._letters |= set(token)
                    self._stat(token)
                    yield WordToken(word=token, lexeme=word.lexeme, grammar=word.grammar)
                else:
                    self.logger.warning("Token excluded: '{}'".format(token))
            elif match != " ":
                self.logger.debug("Match left untokenized: '{}'".format(match))

    def process(self, data: list, book: str):
        self._data = data
        self._book = book

        for token in self.token_iter(False):
            self._verify_token(token)
            self._linear.append(token)

    def _verify_token(self, token):
        if isinstance(token, WordToken):
            self._verify += " " + token.word
        elif isinstance(token, PunctuationToken):
            self._verify += token.diacritic
        elif isinstance(token, VerseToken):
            self._verify += "\n"
