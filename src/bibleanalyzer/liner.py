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
from pathlib import Path

from . import Processor
from .logging import Logger


class Liner(Processor):

    def __init__(self, logger: Logger):
        super().__init__(logger)

        self._cur_file = None

    def process(self, filename: Path):
        self.logger.info("Load parsing: {}".format(filename.name))

        self._cur_file = str(filename)

        for line in self.iterate(filename):
            if not line:
                continue

            self.switch(line)
            try:
                self._processor[self._machine.state](line)
            except ProcessException as e:
                self.logger.error(self.format(e, self._cur_file, self._line_cnt))

