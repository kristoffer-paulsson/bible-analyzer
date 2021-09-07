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
"""Model for the BibleAnalyzer corpus."""
from dataclasses import dataclass, field
from typing import List


@dataclass
class GreekWord:
    word: str = None
    lexeme: str = None
    grammar: str = None


@dataclass
class DataEntry:
    index: int = 0
    book: str = 0
    chapter: int = 0
    verse: int = 0
    text: str = None
    translation: str = None
    words: List[GreekWord] = field(default_factory=list)


@dataclass
class WordToken:
    word: str = None
    lexeme: str = None
    grammar: str = None


@dataclass
class PunctuationToken:
    diacritic: str = None


@dataclass
class ChapterToken:
    number: int = 0


@dataclass
class VerseToken:
    number: int = 0


@dataclass
class SectionToken:
    level: int = 1
