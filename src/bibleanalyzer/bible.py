#
# Copyright (c) 2022 by Kristoffer Paulsson <kristoffer.paulsson@talenten.se>.
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
"""Bible class for examining certain passages based on bible reference."""
import json

from bibleanalyzer.app import Application
from bibleanalyzer.data import CORPUS, NEW_TESTAMENT, OLD_TESTAMENT
from bibleanalyzer.grammar import Grammar
from bibleanalyzer.liner import LinerIterator
from bibleanalyzer.loader import FreshLoaderIterator
from bibleanalyzer.util.model import ChapterToken, VerseToken, WordToken
from bibleanalyzer.util.reference import BibleReference, BibleReferenceCounter


class BookIterator:

    def __init__(self, corpus: str = "all"):
        if corpus == OLD_TESTAMENT:
            self._books = json.loads()


class TokenCounterIterator:

    def __init__(self, liner: LinerIterator):
        self._liner = liner
        self._counter = BibleReferenceCounter()

    @property
    def counter(self) -> BibleReferenceCounter:
        return self._counter

    def __iter__(self):
        self._iter = iter(self._liner)
        return self

    def __next__(self):
        token = next(self._iter)
        if isinstance(token, ChapterToken):
            if token.number > self._counter.chapter:
                self._counter.increase_chapter()
        elif isinstance(token, VerseToken):
            if token.number > self._counter.verse:
                self._counter.increase_verse()
        elif isinstance(token, type(None)):
            raise StopIteration()
        return token


class Bible:
    """Bible parser for use in analysing of the corpus of the bible in part or in full."""

    def __init__(self):
        pass

    @classmethod
    def reference(cls, reference: str) -> BibleReference:
        """Parsing a bible reference, including checks."""
        return BibleReference.reference(reference)

    def loader(self):
        for verse in FreshLoaderIterator(Application.instance().config.get("corpus").joinpath("nt/luke.txt"), CORPUS[NEW_TESTAMENT]):
            if(verse.text):
                Application.instance().logger.info(verse)
            else:
                print(verse)

    def liner(self):
        for token in LinerIterator(FreshLoaderIterator(Application.instance().config.get("corpus").joinpath("nt/mark.txt"), CORPUS[NEW_TESTAMENT]), "mark"):
            Application.instance().logger.info(token)

    def referencing(self):
        ref = BibleReference.reference("john 3:36")
        liner = LinerIterator(FreshLoaderIterator(Application.instance().config.get("corpus").joinpath("nt/john.txt"), CORPUS[NEW_TESTAMENT]), "john")
        for token in liner:
            if ref.is_inside(liner.counter):
                Application.instance().logger.info(token)

    def filter(self):
        ref = BibleReference.reference("john 3:16")
        token_iter = TokenCounterIterator(LinerIterator(FreshLoaderIterator(Application.instance().config.get("corpus").joinpath("nt/john.txt"), CORPUS[NEW_TESTAMENT]), "john"))
        for token in token_iter:
            if ref.is_inside(token_iter.counter):
                if isinstance(token, WordToken):
                    Application.instance().logger.info(Grammar.format(Grammar.classify(token)))
                else:
                    Application.instance().logger.info(token)
