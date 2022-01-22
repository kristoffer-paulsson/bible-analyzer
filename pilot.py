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
"""Testing rig for piloting and evaluation of API:s."""
import json
from unittest import TestCase

from bibleanalyzer import Logger
from bibleanalyzer.config import Config
from bibleanalyzer.data import BOOKS
from bibleanalyzer.grammar import Grammar
from bibleanalyzer.liner import Liner
from bibleanalyzer.loader import TextLoader
from bibleanalyzer.model import WordToken, ChapterToken, VerseToken


class TestRig(TestCase):
    def setUp(self) -> None:
        self.config = Config(list())
        self.logger = Logger.create(self.config, "pilot")

    def test_pilot(self):
        for book in json.loads(BOOKS)["nt"]:
            loader = TextLoader(self.logger, "NA28")
            loader.process(self.config.get("corpus").joinpath("nt/{0}.txt".format(book)))

            liner = Liner(self.logger)
            liner.process(loader.data, book)

            chapter = 1
            verse = 1
            for item in liner.linear:
                if isinstance(item, WordToken):
                    self.logger.info("{0} {1}:{2} {3}".format(book, chapter, verse, Grammar.format(Grammar.classify(item))))
                elif isinstance(item, ChapterToken):
                    chapter = item.number
                elif isinstance(item, VerseToken):
                    verse = item.number
                else:
                    self.logger.info("{}".format(str(item)))

    def test_loader_output(self):
        for book in json.loads(BOOKS)["nt"]:
            loader = TextLoader(self.logger, "NA28")
            loader.process(self.config.get("corpus").joinpath("nt/{0}.txt".format(book)))
            for item in loader.data:
                self.logger.info("{0.book} {0.chapter}:{0.verse} ({0.translation}) {0.text}".format(item))

    def test_loader_stats(self):
        for book in json.loads(BOOKS)["nt"]:
            loader = TextLoader(self.logger, "NA28")
            loader.process(self.config.get("corpus").joinpath("nt/{0}.txt".format(book)))
            self.logger.info("Words per verse: max {max}, min {min}, avg {avg:.2f}".format(**loader.stats))