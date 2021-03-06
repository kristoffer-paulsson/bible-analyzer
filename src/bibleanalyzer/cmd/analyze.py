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
"""Module containing the ANALYZE command class."""
import json
from pathlib import Path
from pickle import Unpickler

from . import Command
from ..analyzer import Analyzer
from ..data import BOOKS
from bibleanalyzer.util.model import WordToken, PunctuationToken, VerseToken
from ..structor import Structor


class AnalyzeCommand(Command):
    def __call__(self):
        if self._args.corpus == "all":
            self.iterate("ot")
            self.iterate("nt")
        else:
            self.iterate(self._args.corpus)

    def iterate(self, corpus: str):
        letters = set()
        stats = dict()
        terms = set()

        self.logger.info("Starting with parsing: {}".format(corpus.upper()))
        path = self._config.get("cache")

        for book in json.loads(BOOKS)[corpus]:
            filename = path.joinpath("linear-{}.pickle".format(book))
            if not filename.is_file():
                self.logger.error("The linear for {} is missing at: {}".format(book.capitalize(), filename))
            terms |= self.analyze(filename, corpus, book)

        print(len(terms), terms)
        self.logger.info("Finished with corpus: {}".format(corpus.upper()))

    def analyze(self, filename: Path, corpus: str, book: str) -> set:
        terms = set()
        with filename.open("rb") as cache:
            for section in Structor(Unpickler(cache).load()).section_iter():
                for clause in section:
                    terms |= Analyzer.analyze(clause)
        return terms

    def export_json(self, filename: Path, corpus: str, book: str) -> list:
        sections = list()
        with filename.open("rb") as cache:
            for section in Structor(Unpickler(cache).load()).secref_iter():
                sections.append({
                    "chapter": section[0],
                    "verse": section[1],
                    "after_word": section[2],
                    "level": section[3]
                })
                # print(Grammar.classify(section))
        return sections


class Reconstructor:

    def __init__(self, book: str):
        self._book = book
        self._verify = ""

    @property
    def verify(self) -> str:
        return self._verify.strip()

    def process(self, data: list):
        for token in data:
            if isinstance(token, WordToken):
                self._verify += " " + token.word
            elif isinstance(token, PunctuationToken):
                self._verify += token.diacritic
            elif isinstance(token, VerseToken):
                self._verify += "\n"
