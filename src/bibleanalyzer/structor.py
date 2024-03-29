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
from bibleanalyzer.util.model import ChapterToken, VerseToken, SectionToken, WordToken, Linear, Token, PunctuationToken


class Section(Linear):

    def __init__(self, offset: int, marker: SectionToken):
        Linear.__init__(self, offset)

        self._sentences = list()
        self._sentences.append(Sentence(offset))
        self._marker = marker

    def dispatch(self, token: Token):
        self.add(token)
        if isinstance(token, PunctuationToken):
            if token.diacritic in (".", ";"):
                self._sentences[-1].marker(token)
                self._sentences.append(Sentence(self._offset + len(self._linear)))
                return

        self._sentences[-1].dispatch(token)

    def __str__(self) -> str:
        return " ".join([str(s) for s in self._sentences])

    def __iter__(self):
        for sentence in self._sentences:
            for clause in sentence._clauses:
                yield clause


class Sentence(Linear):

    def __init__(self, offset: int):
        Linear.__init__(self, offset)

        self._clauses = list()
        self._clauses.append(Clause(offset))
        self._marker = None

    def dispatch(self, token: Token):
        self.add(token)
        if isinstance(token, PunctuationToken):
            if token.diacritic in ("·", ",", ":", "-"):
                self._clauses[-1].marker(token)
                self._clauses.append(Clause(self._offset + len(self._linear)))
                return

        self._clauses[-1].dispatch(token)

    def marker(self, token: PunctuationToken):
        self._marker = token

    def __str__(self) -> str:
        return " ".join([str(c) for c in self._clauses]) + (self._marker.diacritic if self._marker else "")


class Clause(Linear):

    def __init__(self, offset: int):
        Linear.__init__(self, offset)
        self._marker = None
        self._tokens = list()

    @property
    def words(self) -> list:
        return self._tokens

    def dispatch(self, token: Token):
        self.add(token)
        if isinstance(token, WordToken):
            self._tokens.append(token)
        elif isinstance(token, (ChapterToken, VerseToken)):
            return
        else:
            raise ValueError("Not a word token: {}".format(token))

    def marker(self, token: PunctuationToken):
        self._marker = token

    def __str__(self) -> str:
        return " ".join([t.word for t in self._tokens if isinstance(
            t, WordToken)]) + (self._marker.diacritic if self._marker else "")


class Structor(Linear):
    REF = -1
    SEC = -2

    def __init__(self, linear: list):
        Linear.__init__(self, 0)
        self._linear = linear
        self._index = dict()
        self._ref = dict()
        self._sec = {
            1: list(),
            2: list(),
            3: list()
        }
        self._sections = list()

        self._structure()

        self._ctx = None
        self._slice = 0

    def _structure(self):
        chapter = 1
        verse = 1
        word = 0

        self._index[1] = dict()
        self._index[1][1] = dict()

        for index, token in enumerate(self._linear):
            if isinstance(token, WordToken):
                word += 1
            if isinstance(token, ChapterToken):
                chapter = token.number
                verse = 0

                if chapter not in self._index.keys():
                    self._index[chapter] = dict()

                if chapter not in self._ref.keys():
                    self._ref[chapter] = dict()

            elif isinstance(token, VerseToken):
                verse = token.number
                word = 0

                if verse not in self._index[chapter].keys():
                    self._index[chapter][verse] = dict()

                if verse not in self._ref.keys():
                    self._ref[chapter] = dict()
                self._ref[chapter][verse] = index

            elif isinstance(token, SectionToken):
                self._sections.append((Section(index, token)))
                self._index[chapter][verse][word] = token.level
                level = abs(token.level)
                if level == 1:
                    self._sec[1].append(index)
                    self._sec[2].append(index)
                    self._sec[3].append(index)
                elif level == 2:
                    self._sec[2].append(index)
                    self._sec[3].append(index)
                elif level == 3:
                    self._sec[3].append(index)
                else:
                    pass
                    # raise ValueError("Invalid section level: {}".format(token))

            if not isinstance(token, SectionToken):
                self._sections[-1].dispatch(token)

    def _backtrack(self, index: int, level: int = 1) -> int:
        indices = filter(self._sec.keys(), lambda x: x <= level, reversed=True)
        for index in indices:
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

    # def section(self, chapter: int, verse: int, level: int) -> list:
    #    tokens = list()
    #    stop = False

    #    for token in self._linear[self._backtrack(self.search(chapter, verse), level):]:
    #        if isinstance(token, (SectionToken)):
    #            if token.level == level:
    #                if stop:
    #                    break
    #                stop = True
    #        tokens.append(token)

    #    return tokens

    # def __enter__(self, kind: int, start: int):
    #    if kind == self.SEC and 0 <= start < len(self._sec):
    #        self._slice = slice(self._sec[start], self._sec[start + 1])
    #    else:
    #        raise IndexError("Unknown iteration type: {}".format(kind))
    #
    #    self._ctx = kind

    # def __exit__(self, exc_type, exc_val, exc_tb):
    #    self._ctx = None

    def section_iter(self, level: int = 1, index: int = 0):
        for section in self._sections:
            yield section
        # for current in range(len(self._sec[level]) - 1):
        #    yield self._linear[self._sec[level][current]:self._sec[level][current + 1]]

    def secref_iter(self):
        for chapter in self._index.keys():
            for verse in self._index[chapter].keys():
                for word, level in self._index[chapter][verse].items():
                    yield chapter, verse, word, level
