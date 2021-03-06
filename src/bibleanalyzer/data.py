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
"""Data used in the application for several reasons."""

NAME = """BibleAnlyzer"""
VERSION = """1.0b1"""
DESCRIPTION = f"""{NAME} {VERSION} is used to analyze The Bible's corpus grammatically and statistically."""

BOOKS = """
{
  "ot": [
    "genesis",
    "exodus",
    "leviticus",
    "numbers",
    "deuteronomy",
    "joshua",
    "judges",
    "ruth",
    "1_samuel",
    "2_samuel",
    "1_kings",
    "2_kings",
    "1_chronicles",
    "2_chronicles",
    "ezra",
    "nehemiah",
    "esther",
    "job",
    "psalm",
    "proverbs",
    "ecclesiastes",
    "song_of_solomon",
    "isaiah",
    "jeremiah",
    "lamentations",
    "ezekiel",
    "daniel",
    "hosea",
    "joel",
    "amos",
    "obadiah",
    "jonah",
    "micah",
    "nahum",
    "habakkuk",
    "zephaniah",
    "haggai",
    "zechariah",
    "malachi",
    "wisdom",
    "sirach",
    "letter_of_jeremiah",
    "tobit",
    "judith"
  ],
  "nt": [
    "matthew",
    "mark",
    "luke",
    "john",
    "acts",
    "romans",
    "1_corinthians",
    "2_corinthians",
    "galatians",
    "ephesians",
    "philippians",
    "colossians",
    "1_thessalonians",
    "2_thessalonians",
    "1_timothy",
    "2_timothy",
    "titus",
    "philemon",
    "hebrews",
    "james",
    "1_peter",
    "2_peter",
    "1_john",
    "2_john",
    "3_john",
    "jude",
    "revelation"
  ]
}
"""

OLD_TESTAMENT = "ot"
NEW_TESTAMENT = "nt"
BOTH_TESTAMENTS = "all"

CORPUS = {
    "ot": "LXT",
    "nt": "NA28",
}
