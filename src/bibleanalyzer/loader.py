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
"""Corpus loader. Loads and parses UTF-8 corpus files as generated by the BibleWorks 10 Report Generator,
saved as RTF and converted to TXT by TextEdit for macOS."""
import re
from pathlib import Path

from . import Processor, ProcessException
from .logging import Logger
from .model import DataEntry, GreekWord

VERSE_REGEX = r"""(?P<translation>\S+) (?P<book>\S+) (?P<chapter>\d+)\:(?P<verse>\d+) (?P<text>\S.*)"""
HLINE_REGEX = r"""^\.*\n(_+)\n.*$"""
GREEK_REGEX = r"""^(?:\d+)\. (?:\S+) (?:\S+) - (?:\S+) (?:\S+).*$"""
WHOLE_REGEX = r"""^(?:(?P<translation>\S+) (?P<book>(?:[1-3] )?[\S ]+) (?P<chapter>\d+)\:(?P<verse>\d+)(?: (?P<text>\S.*))?)|(?P<line>_+)|(?:(?P<index>\d+)\. (?P<word>\S+) (?P<lexeme>\S+) - (?P<grammar>\S+) (?P<inflexion>[\S ]+))$"""

TOKEN_REGEX = r"""([·.,;:]|[^[·\.,;: \(\)\[\]]\s]+)"""


class StateError(RuntimeWarning):
    """State machine throws this exception at wrongful attempt to change the state."""


class StateMachine:
    START = 1
    TEXT = 2
    LINE = 3
    WORD = 4
    END = 5

    def __init__(self):
        self._state = self.START
        self._states = {
            self.START: (self.TEXT,),
            self.TEXT: (self.LINE,),
            self.LINE: (self.WORD,),
            self.WORD: (self.END, self.TEXT),
            self.END: tuple(),
        }

    @property
    def state(self) -> int:
        return self._state

    def goto(self, state: int):
        if state not in self._states[self._state]:
            raise StateError("Couldn't go from state {} to {}".format(self._state, state))
        self._state = state

    def reset(self):
        self._state = self.START


class TextLoader(Processor):

    def __init__(self, logger: Logger, translation: str = None):
        self.logger = logger

        self._processor = (
            None,
            self.process_start,
            self.process_text,
            self.process_line,
            self.process_word,
            self.process_end
        )

        self._translation = translation

        self._machine = StateMachine()
        self._skip = False
        self._regex = VERSE_REGEX

        self._line_cnt = 0
        self._cur_file = None
        self._cur_book = None

        self._total_cnt = 0
        self._chapter_cnt = 1
        self._verse_cnt = 1
        self._word_cnt = 1

        self._data = list()
        self._entry = None
        self._verify = ""

        # All missing verses reported.
        self._missing = list()

    @property
    def data(self) -> list:
        return self._data

    @property
    def verify(self) -> str:
        return self._verify.strip()

    @property
    def stats(self) -> dict:
        data = list()
        for entry in self.data:
            if entry.words:
                data.append(len(entry.words))
        return {"max": max(data), "min": min(data), "avg": sum(data) / len(data)}

    @property
    def telemetry(self) -> dict:
        return {
            "missing": self._missing,
            **self.stats
        }

    def process(self, filename: Path):
        self.logger.info("Load corpus: {}".format(filename.name))

        self._cur_file = str(filename)

        try:
            for line in self.iterate(filename):
                if not line:
                    continue

                self.switch(line)
                try:
                    self._processor[self._machine.state](line)
                except ProcessException as e:
                    self.logger.error(Logger.file_format(e, self._cur_file, self._line_cnt))

            self._machine.goto(StateMachine.END)
            self._processor[self._machine.state]()
        except StateError as e:
            self.logger.error(Logger.file_format(
                "{} The parser suffered from a state machine error, skipping".format(e),
                self._cur_file, self._line_cnt
            ))

    def switch(self, line: dict):
        self.logger.debug(list(filter(None, line.values())))

        # In case a verse has been left out we reset the state machine and start over.
        if line["translation"] and self._machine.state is StateMachine.LINE:
            self._add_data()
            self._entry = None
            self._machine.reset()
            self._machine.goto(StateMachine.TEXT)

        elif line["translation"] and self._machine.state is not StateMachine.TEXT:
            if self._machine.state == StateMachine.WORD:
                self._add_data()
                self._entry = None
            self._machine.goto(StateMachine.TEXT)
        elif line["line"] and self._machine.state is not StateMachine.LINE:
            self._machine.goto(StateMachine.LINE)
        elif line["index"] and self._machine.state is not StateMachine.WORD:
            self._machine.goto(StateMachine.WORD)
            self._word_cnt = 1

    def process_start(self, line: dict):
        pass

    def process_word(self, line: dict):
        if not line["index"]:
            self.logger.error(Logger.file_format("Expected a greek word", self._cur_file, self._line_cnt))

        index = int(line["index"])

        if index != self._word_cnt:
            self.logger.error(
                Logger.file_format("Greek word not in order ({}, {})".format(
                    self._word_cnt, index), self._cur_file, self._line_cnt))

        self._entry.words.append(GreekWord(
            word=line["word"],
            lexeme=line["lexeme"],
            grammar=line["grammar"],
        ))
        self._word_cnt += 1
        self._total_cnt += 1

    def process_line(self, line: dict):
        if not line["line"]:
            self.logger.error(Logger.file_format("Expected a line", self._cur_file, self._line_cnt))

    def process_text(self, line: dict):
        if not line["translation"]:
            self.logger.error(Logger.file_format("Expected a translation", self._cur_file, self._line_cnt))
        elif line["translation"] != self._translation:
            return

        book = line["book"]
        chapter = int(line["chapter"])
        verse = int(line["verse"])

        if not line["text"]:
            self._skip = True
            self._missing.append({
                "book": book,
                "chapter": chapter,
                "verse": verse,
                "translation": line["translation"],
                "line": self._line_cnt
            })
            self.logger.warning(
                Logger.file_format("{book} {chapter}:{verse} ({translation}) is missing in".format(
                    book=book, chapter=chapter, verse=verse, translation=line["translation"]),
                    self._cur_file, self._line_cnt, "corpus"
                )
            )

        if book:
            self._cur_book = book

        if chapter == self._chapter_cnt + 1:
            self._chapter_cnt += 1
            self._verse_cnt = 1
        else:
            if chapter != self._chapter_cnt:
                self.logger.error(
                    Logger.file_format("Chapter is out of order ({}, {})".format(
                        self._chapter_cnt, chapter), self._cur_file, self._line_cnt))
            if verse != self._verse_cnt:
                self.logger.error(Logger.file_format(
                    "Verse is out of order ({}, {})".format(
                        self._verse_cnt, verse), self._cur_file, self._line_cnt))

        self._entry = DataEntry(
            index=self._total_cnt,
            book=book,
            chapter=chapter,
            verse=verse,
            text=line["text"],
            translation=line["translation"]
        )
        self._verse_cnt += 1

    def process_end(self):
        self._add_data()
        self._entry = None

    def iterate(self, filename: Path):
        with filename.open("r") as doc:
            for line in doc:
                self._line_cnt += 1
                match = re.match(WHOLE_REGEX, line)
                if match:
                    yield match.groupdict()

    def _add_data(self):
        if self._entry.text:
            self._verify += self._entry.text.strip() + "\n"
        self._data.append(self._entry)
