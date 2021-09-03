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

from bibleanalyzer.model import PunctuationToken, WordToken, ChapterToken, VerseToken, DataEntry
from bibleanalyzer.transform import Koine

from . import Processor, ProcessException
from .logging import Logger


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

    @property
    def linear(self) -> list:
        return self._letters

    @property
    def letters(self) -> set:
        return self._letters

    @property
    def stats(self) -> dict:
        return self._stats

    def _stat(self, letters: str):
        for char in set(Koine.expand(letters)):
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

    def chapter_iter(self):
        for item in self.verse_dispenser():
            if item.chapter == (self._chapter + 1):
                self._chapter += 1
                self._verse = 0
                yield ChapterToken(number=item.chapter)

            if item.verse == (self._verse + 1):
                self._verse += 1
                yield VerseToken(number=item.verse)

            for token in self.tokenizer_iter(item):
                yield token

    def token_iter(self):
        for token in self.chapter_iter():
            yield token

    def tokenizer_iter(self, item: DataEntry):
        word_count = 0
        for token in re.findall(TOKEN_REGEX, item.text.replace("[", "").replace("]", "")):
            token = token.strip()
            if token:
                if token in PUNCTUATION:
                    yield PunctuationToken(diacritic=token)
                else:
                    word = item.words[word_count]

                    if Koine.normalize(word.word).lower() != Koine.normalize(token).lower():
                        raise ProcessException("Not the right word. {} {}".format(token, word.word))

                    word_count += 1
                    self._letters |= set(token)
                    self._stat(token)
                    yield WordToken(word=token, lexeme=word.lexeme, grammar=word.grammar)

    def process(self, data: list, book: str):
        self._data = data
        self._book = book

        for token in self.token_iter():
            self._linear.append(token)