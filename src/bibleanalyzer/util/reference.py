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
"""Referencing utilities for the BibleAnalyzer."""
import json
import re

from bibleanalyzer.data import BOOKS, OLD_TESTAMENT, NEW_TESTAMENT

REFERENCE_REGEX = r"""^((?P<book>(?:[1-3]_)[\S ]+) (?:(?:(?P<chapter_lr1>\d+)\:(?P<verse_lr1>\d+)-(?P<chapter_lr2>\d+)\:(?P<verse_lr2>\d+))|(?:(?P<chapter_r1>\d+)\:(?P<verse_r1>\d+)-(?P<verse_r2>\d+))|(?P<chapter>\d+)\:(?P<verse>\d+)))$"""


class BibleReferenceError(RuntimeError):
    """Error due to parsing of reference failed."""
    UNRECOGNIZABLE = ("Failed to recognize scripture reference format.", 1)
    UNKNOWN_BOOK = ("Failed to recognize bible book given in the reference.", 2)
    CHAPTER_ORDER = ("The second chapter in a range must not be the same or lower.", 3)
    VERSE_ORDER = ("The second verse in a range must not be the same or lower.", 4)
    CHAPTER_VALUE = ("Chapter must not be 0 or lower", 5)
    VERSE_VALUE = ("Verse must not be 0 or lower", 6)


class BibleReferenceCounter:
    """Counter to easily increase a bible reference one verse at a time."""

    def __init__(self, chapter=1, verse=1):
        self._chapter = chapter
        self._verse = verse

    @property
    def chapter(self) -> int:
        return self._chapter

    @property
    def verse(self) -> int:
        return self._verse

    def increase_verse(self):
        self._verse += 1

    def increase_chapter(self):
        self._chapter += 1
        self._verse = 1


class BibleReference:
    """Representation of a bible reference with a range if necessary."""

    _DATA = json.loads(BOOKS)
    _BOOKS = _DATA[OLD_TESTAMENT] + _DATA[NEW_TESTAMENT]

    def __init__(self, book: str, chapter: int = 1, verse: int = 1, to_chapter: int = None, to_verse: int = None):
        self._book = book
        self._from_chapter = chapter
        self._from_verse = verse
        self._to_chapter = to_chapter
        self._to_verse = to_verse

    @property
    def book(self) -> str:
        return self._book

    @property
    def start(self) -> tuple:
        return self._book, self._from_chapter, self._from_verse

    @property
    def end(self) -> tuple:
        if self._to_chapter:
            return self._book, self._to_chapter, self._to_verse
        elif self._to_verse:
            return self._book, self._from_chapter, self._to_verse
        else:
            return self._book, self._from_chapter, self._from_verse

    def is_inside(self, counter: BibleReferenceCounter) -> bool:
        if self._to_chapter:
            return self._from_chapter <= counter.chapter <= self._to_chapter and self._from_verse <= counter.verse <= self._to_verse
        elif self._to_verse:
            return self._from_chapter == counter.chapter and self._from_verse <= counter.verse <= self._to_verse
        else:
            return self._from_chapter == counter.chapter and self._from_verse == counter.verse

    @classmethod
    def reference(cls, reference: str) -> "BibleReference":
        match = re.match(REFERENCE_REGEX, reference)
        if match:
            group = match.groupdict()
            if group["book"] not in cls._BOOKS:
                raise cls(*BibleReferenceError.UNKNOWN_BOOK)
            if group["chapter_lr1"] is not None:
                if int(group["chapter_lr1"]) < 1 or int(group["chapter_lr2"]) < 1:
                    raise BibleReferenceError(*BibleReferenceError.CHAPTER_VALUE)
                if int(group["chapter_lr1"]) >= int(group["chapter_lr2"]):
                    raise BibleReferenceError(*BibleReferenceError.CHAPTER_ORDER)
                if int(group["verse_lr1"]) < 1 or int(group["verse_lr2"]) < 1:
                    raise BibleReferenceError(*BibleReferenceError.VERSE_VALUE)

                return cls(
                    group["book"],
                    int(group["chapter_lr1"]), int(group["verse_lr1"]),
                    int(group["chapter_lr2"]), int(group["verse_lr2"])
                )
            elif group["chapter_r1"] is not None:
                if int(group["chapter_l1"]) < 1:
                    raise BibleReferenceError(*BibleReferenceError.CHAPTER_VALUE)
                if int(group["verse_lr"]) < 1 or int(group["verse_r2"]) < 1:
                    raise BibleReferenceError(*BibleReferenceError.VERSE_VALUE)
                if int(group["verse_r1"]) >= int(group["verse_r2"]):
                    raise BibleReferenceError(*BibleReferenceError.VERSE_ORDER)

                return cls(
                    group["book"],
                    int(group["chapter_r1"]), int(group["verse_r1"]),
                    to_verse=int(group["verse_r2"])
                )
            else:
                if int(group["chapter"]) < 1:
                    raise BibleReferenceError(*BibleReferenceError.CHAPTER_VALUE)
                if int(group["verse"]) < 1:
                    raise BibleReferenceError(*BibleReferenceError.VERSE_VALUE)

                return cls(group["book"], int(group["chapter"]), int(group["verse"]))
        else:
            raise BibleReferenceError(*BibleReferenceError.UNRECOGNIZABLE)

    def __str__(self):
        if self._to_chapter:
            return "{0} {1}:{2}-{3}:{4}".format(
                self._book, self._from_chapter, self._from_verse, self._to_chapter, self._to_verse)
        elif self._to_verse:
            return "{0} {1}:{2}-{3}".format(
                self._book, self._from_chapter, self._from_verse, self._to_verse)
        else:
            return "{0} {1}:{2}".format(
                self._book, self._from_chapter, self._from_verse)
