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
"""Module containing the CSV command class."""
import csv
import hashlib
import json
from pathlib import Path
from pickle import Unpickler

from . import Command
from ..data import BOOKS


class CsvCommand(Command):
    def __call__(self):
        if self._args.corpus == "all":
            self.iterate("ot")
            self.iterate("nt")
        else:
            self.iterate(self._args.corpus)

    def iterate(self, corpus: str):
        self.logger.info("Starting with parsing: {}".format(corpus.upper()))
        path = self._config.get("cache")
        for book in json.loads(BOOKS)[corpus]:
            filename = path.joinpath("parsing-{}.pickle".format(book))
            if not filename.is_file():
                self.logger.error("The parsing for {} is missing at: {}".format(book.capitalize(), filename))
            print(self.export(filename, corpus, book))
        self.logger.info("Finished with corpus: {}".format(corpus.upper()))

    def export(self, filename: Path, corpus: str, book: str) -> str:
        with filename.open("rb") as cache:
            data = Unpickler(cache).load()

        csv_path = self._config.get("cache").joinpath(book + ".csv")
        with csv_path.open("w", encoding="utf-8") as csv_file:
            csv_file.truncate()
            writer = csv.DictWriter(csv_file, fieldnames=("chapter", "verse", "corpus"))
            writer.writeheader()
            for entry in data:
                writer.writerow({"chapter": entry.chapter, "verse": entry.verse, "corpus": str(entry.text if entry.text else "").strip().lower().replace("·", "").replace(".", "").replace(",", "").replace(":", "").replace(";", "").replace("(", "").replace(")", "")})

        hash = hashlib.sha256()
        content = csv_path.read_bytes()
        hash.update(content)
        return "{} {} {}".format(hash.hexdigest(), len(content), csv_path.relative_to(self._config.get("cache")))

