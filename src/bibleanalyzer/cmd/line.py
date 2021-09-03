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
"""Module containing the LINE command class."""
import json
from pathlib import Path
from pickle import Pickler, Unpickler

from . import Command
from ..data import BOOKS
from ..liner import Liner


class LineCommand(Command):
    def __call__(self):
        if self._args.corpus == "all":
            self.iterate("ot")
            self.iterate("nt")
        else:
            self.iterate(self._args.corpus)

    def iterate(self, corpus: str):
        letters = set()
        stats = dict()

        self.logger.info("Starting with parsing: {}".format(corpus.upper()))
        path = self._config.get("cache")

        for book in json.loads(BOOKS)[corpus]:
            filename = path.joinpath("parsing-{}.pickle".format(book))
            if not filename.is_file():
                self.logger.error("The parsing for {} is missing at: {}".format(book.capitalize(), filename))
            liner = self.lineup(filename, corpus, book)

            letters |= liner.letters
            for key, value in liner.stats.items():
                if key in stats.keys():
                    stats[key] += value
                else:
                    stats[key] = value

        self.logger.info("Finished with corpus: {}".format(corpus.upper()))
        print(letters, stats)

    def lineup(self, filename: Path, corpus: str, book: str):
        liner = Liner(self.logger)
        with filename.open("rb") as cache:
            data = Unpickler(cache).load()

            liner.process(data, book)

        return liner
        # with self._config.get("cache").joinpath("linear-{}.pickle".format(book)).open("wb") as cache:
        #    Pickler(cache).dump(liner.data)
