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
"""Module containing the LOAD command class."""
import json

from . import Command
from ..data import BOOKS
from ..loader import TextLoader


class LoadCommand(Command):
    def __call__(self):
        if self._args.corpus == "all":
            self.iterate("ot")
            self.iterate("nt")
        elif self._args.corpus == "nt":
            self.iterate("nt")
        elif self._args.corpus == "ot":
            self.iterate("ot")
        else:
            raise RuntimeError("Unsupported corpus: {}".format(self._args.corpus))

    def iterate(self, corpus):
        self.logger.info("Starting with corpus: {}".format(corpus.upper()))
        path = self._config.get("corpus").joinpath(corpus)
        for book in json.loads(BOOKS)[corpus]:
            filename = path.joinpath("{}.txt".format(book))
            if not filename.is_file():
                self.logger.error("The corpus for {} is missing at: {}".format(book.capitalize(), filename))
            self.parse(filename, corpus, book)
        self.logger.info("Finished with corpus: {}".format(corpus.upper()))

    def parse(self, filename, corpus, book):
        loader = TextLoader(self.logger)
        data = loader.parse(filename)
        print(data)
