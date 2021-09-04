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
from argparse import ArgumentParser, Namespace

from bibleanalyzer.data import DESCRIPTION


class CLI:

    def __init__(self):
        self._parser = ArgumentParser(description=DESCRIPTION)
        self._parser.add_argument("-d", "--debug", action="store_true", default=False,
                                  help="Print debug messages in the log file.")
        parsers = self._parser.add_subparsers(
            title="Commands",
            description="Operations on the corpus and compiled statistics.",
            dest="command",
            help="First the 'load' command must be invoked to compile the corpus.",
        )
        self._load(parsers)
        self._line(parsers)
        self._csv(parsers)
        self._clean(parsers)

    @classmethod
    def parse_args(cls) -> Namespace:
        return cls()._parser.parse_args()

    def _load(self, subparser):
        load = subparser.add_parser(name="load", help="Imports the corpora and caches them as \"parsings.\"")
        load.add_argument("corpus", choices=["all", "nt", "ot"], help="Which corpora to load.")
        load.add_argument("-v", "--verify", action="store_true", default=False, help="Verify output against source.")

    def _line(self, subparser):
        line = subparser.add_parser(name="line", help="Lines up the corpora \"parsings\" into \"linear\" for analysis.")
        line.add_argument("corpus", choices=["all", "nt", "ot"], help="Which parsings to process.")
        line.add_argument("-v", "--verify", action="store_true", default=False, help="Verify output against source.")

    def _csv(self, subparser):
        load = subparser.add_parser(name="csv", help="Exports the loaded corpora to comma separated value files.")
        load.add_argument("corpus", choices=["all", "nt", "ot"], help="Which parsings to export.")

    def _clean(self, subparser):
        clean = subparser.add_parser(name="clean", help="Cleanses the cache or the logs directories.")
        clean.add_argument("-c", "--cache", action="store_true", default=False, help="Clean the cache folder.")
        clean.add_argument("-l", "--logs", action="store_true", default=False, help="Clean the logs folder.")
