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
"""Grammar representation of morphology."""
from bibleanalyzer.model import WordToken


class WordClass:
    NOUN = b"n"
    VERB = b"v"
    ADJECTIVE = b"a"
    DEFINITE_ARTICLE = b"d"
    PREPOSITION = b"p"
    CONJUNCTION = b"c"
    PARTICLE = b"x"
    INTERJECTION = b"i"
    ADVERB = b"b"
    PRONOUN = b"r"
    INDECLINABLE = b"t"
    UNIDENTIFIED = b"z"


class WordCase:
    NOMINATIVE = b"n"
    GENITIVE = b"g"
    DATIVE = b"d"
    ACCUSATIVE = b"a"
    VOCATIVE = b"v"


class WordGender:
    MASCULINE = b"m"
    FEMININE = b"f"
    NEUTER = b"n"


class WordNumber:
    SINGULAR = b"s"
    PLURAL = b"p"
    DUAL = b"d"


class WordProperNoun:
    PROPER = b"p"
    COMMON = b"c"


class WordMood:
    INDICATIVE = b"i"
    SUBJUNCTIVE = b"s"
    OPTATIVE = b"o"
    IMPERATIVE = b"d"
    INFINITIVE = b"n"
    PARTICIPLE = b"p"


class WordTense:
    PRESENT = b"p"
    IMPERFECT = b"i"
    FUTURE = b"f"
    AORIST = b"a"
    PERFECT = b"x"
    PLUPERFECT = b"y"
    FUTURE_PERFECT = b"z"


class WordVoice:
    ACTIVE = b"a"
    MIDDLE = b"m"
    PASSIVE = b"p"
    MIDDLE_PASSIVE = b"e"


class WordPerson:
    FIRST = b"1"
    SECOND = b"2"
    THIRD = b"3"


class WordPositionAdjective:
    NORMAL = b"n"
    POSSESSIVE = b"s"
    DEMONSTRATIVE = b"d"
    INTERROGATIVE = b"q"
    INDEFINITE = b"i"
    INTENSIVE = b"t"
    CARDINAL = b"c"
    ORDINAL = b"o"
    NUMERAL = b"m"
    RELATIVE = b"r"


class WordDegree:
    POSITIVE = b"p"
    COMPARATIVE = b"c"
    SUPERLATIVE = b"s"
    NO_DEGREE = b"n"


class WordConjunction:
    COORDINATING = b"c"
    SUBORDINATING = b"s"


class WordPositionPronoun:
    PERSONAL = b"p"
    RELATIVE = b"r"
    DEMONSTRATIVE = b"d"
    INTERROGATIVE = b"q"
    INDEFINITE = b"i"
    INTENSIVE = b"t"
    REFLEXIVE = b"x"
    RECIPROCAL = b"e"
    INDEFINITE_RELATIVE = b"f"
    CORRELATIVE = b"g"


class Grammar:

    WORD_CLASS_OPTS = tuple(list(filter(lambda x: isinstance(x, bytes), vars(WordClass).values())))

    def _noun(self, inflections: bytes):
        pass

    def _verb(self, inflections: bytes):
        pass

    def _adjective(self, inflections: bytes):
        pass

    def _definite_article(self, inflections: bytes):
        pass

    def _preposition(self, inflections: bytes):
        pass

    def _conjunction(self, inflections: bytes):
        pass

    def _particle(self, inflections: bytes):
        pass

    def _interjection(self, inflections: bytes):
        pass

    def _adverb(self, inflections: bytes):
        pass

    def _pronoun(self, inflections: bytes):
        pass

    def _indeclinable(self, inflections: bytes):
        pass

    INFLECTORS = {
        WordClass.NOUN: _noun,
        WordClass.VERB: _verb,
        WordClass.ADJECTIVE: _adjective,
        WordClass.DEFINITE_ARTICLE: _definite_article,
        WordClass.PREPOSITION: _preposition,
        WordClass.CONJUNCTION: _conjunction,
        WordClass.PARTICLE: _particle,
        WordClass.INTERJECTION: _interjection,
        WordClass.ADVERB: _adverb,
        WordClass.PRONOUN: _pronoun,
        WordClass.INDECLINABLE: _indeclinable,
    }

    def __init__(self, word: WordToken):
        self._word = word
        self._class = self._classify(word.grammar.encode())

    @property
    def wcls(self) -> bytes:
        """Wordclass by representation"""
        return self._class

    def _classify(self, grammar: bytes):
        wcls = grammar[0]
        if wcls in self.INFLECTORS.keys():
            self._class = wcls
            self.INFLECTORS[wcls](grammar[1:])
