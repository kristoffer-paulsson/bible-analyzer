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
"""The purpose of the structor is to analyze and index a structure from the linear tokens."""
from bibleanalyzer.model import ChapterToken, VerseToken, SectionToken


class Structor:

    def __init__(self, linear: list):
        self._linear = linear
        self._index = dict()
        self._ref = dict()
        self._sec = dict()

        self._structure()

    def _structure(self):
        chapter = None
        verse = None

        for index, token in enumerate(self._linear):
            if isinstance(token, ChapterToken):
                chapter = token.number
                verse = 0

                if chapter not in self._index.keys():
                    self._index[chapter] = dict()

                if chapter not in self._ref.keys():
                    self._ref[chapter] = dict()

            elif isinstance(token, VerseToken):
                verse = token.number

                if verse not in self._index[chapter].keys():
                    self._index[chapter][verse] = dict()

                if verse not in self._ref.keys():
                    self._ref[chapter] = dict()
                self._ref[chapter][verse] = index

            elif isinstance(token, SectionToken):
                self._index[chapter][verse][index] = token.level
                self._sec[index] = token.level

    def _backtrack(self, index: int, level: int = 1) -> int:
        indicies = filter(self._sec.keys(), lambda x: x <= level, reversed=True)
        for index in indicies:
            if self._sec[index] == level:
                return index
        return 0

    def search(self, chapter: int, verse: int) -> int:
        try:
            return self._ref[chapter][verse]
        except KeyError:
            return -1

    def verse(self, chapter: int, verse: int) -> list:
        tokens = list()
        stop = False

        for token in self._linear[self.search(chapter, verse):]:
            if isinstance(token, (ChapterToken, VerseToken)):
                if stop:
                    break
                stop = True
            tokens.append(token)

        return tokens

    def section(self, chapter: int, verse: int, level: int) -> list:
        tokens = list()
        stop = False

        for token in self._linear[self._backtrack(self.search(chapter, verse), level):]:
            if isinstance(token, (SectionToken)):
                if token.level == level:
                    if stop:
                        break
                    stop = True
            tokens.append(token)

        return tokens
