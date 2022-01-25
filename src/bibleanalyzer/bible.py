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
from bibleanalyzer.app import Application
from bibleanalyzer.data import CORPUS, NEW_TESTAMENT
from bibleanalyzer.liner import LinerIterator
from bibleanalyzer.loader import LoaderIterator
from bibleanalyzer.util.reference import BibleReference


class Bible:
    """Bible parser for use in analysing of the corpus of the bible in part or in full."""

    def __init__(self):
        pass

    @classmethod
    def reference(cls, reference: str) -> BibleReference:
        """Parsing a bible reference, including checks."""
        return BibleReference.reference(reference)

    def loader(self):
        for verse in LoaderIterator(Application.instance().config.get("corpus").joinpath("nt/luke.txt"), CORPUS[NEW_TESTAMENT]):
            if(verse.text):
                Application.instance().logger.info(verse)
            else:
                print(verse)

    def liner(self):
        for token in LinerIterator(LoaderIterator(Application.instance().config.get("corpus").joinpath("nt/mark.txt"), CORPUS[NEW_TESTAMENT]), "mark"):
            Application.instance().logger.info(token)
