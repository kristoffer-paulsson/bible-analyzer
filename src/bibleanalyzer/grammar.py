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
"""Grammar representation of morphology.

Morphologies can be found at:
    https://wiki.logos.com/morphology_codes
    http://www.clavmon.cz/ultranet/bw/bwCodingBW.pdf
"""
from enum import Enum
from typing import List

from bibleanalyzer.model import WordToken


class GrammarWarning(RuntimeWarning):
    """"Warnings to be thrown because of grammatical invariants."""


class Word:
    """Base class for a word being analyzable."""

    def __init__(self, word: WordToken):
        self._word = word

    @property
    def word(self) -> WordToken:
        return self._word

    def __repr__(self) -> str:
        return "<{} {}@{}>".format(self.__class__.__name__, self._word.lexeme.title(), self._word.grammar)


class Morphology:
    """Base class for parsing morphology of said software."""
    pass


class Inflexion(str, Enum):
    """Base class representing one kind of inflexion on a given word."""

    @classmethod
    def is_enumerated(cls, value: str):
        if value not in cls.__members__.values():
            raise GrammarWarning("'{}' is not an inflexion of {}.".format(value, cls.__name__))
        return cls(value)


class InflexionBWG(Inflexion):
    """Represents a BibleWorks greek inflexion kind."""
    pass


class Speech(InflexionBWG):
    """Part of speech."""

    NOUN = "n"
    PRONOUN = "r"
    DEFINITE_ARTICLE = "d"
    VERB = "v"
    ADJECTIVE = "a"
    ADVERB = "b"
    CONJUNCTION = "c"
    PREPOSITION = "p"
    PARTICLE = "x"
    INDECLINABLE_NOUN = "t"
    INTERJECTION = "i"
    UNIDENTIFIED = "z"
    UNKNOWN = "-"


class Case(InflexionBWG):
    """Case collection."""


class CaseGeneric(Case):
    """Word case, generically."""

    NOMINATIVE = "n"
    GENITIVE = "g"
    DATIVE = "d"
    ACCUSATIVE = "a"
    VOCATIVE = "v"
    UNKNOWN = "-"


class CasePreposition(Case):
    """Preposition case, specifically."""

    GENITIVE = "g"
    DATIVE = "d"
    ACCUSATIVE = "a"
    INDETERMINATE = "p"
    UNKNOWN = "-"


class Gender(InflexionBWG):
    """Word gender."""

    MASCULINE = "m"
    FEMININE = "f"
    NEUTER = "n"
    UNKNOWN = "-"


class Number(InflexionBWG):
    """Word number."""

    SINGULAR = "s"
    PLURAL = "p"
    UNKNOWN = "-"


class Mood(InflexionBWG):
    """Word mood."""

    PARTICIPLE = "p"
    INFINITIVE = "n"
    INDICATIVE = "i"
    IMPERATIVE = "d"
    SUBJUNCTIVE = "s"
    OPTATIVE = "o"
    UNKNOWN = "-"


class Tense(InflexionBWG):
    """Word tense."""

    PRESENT = "p"
    FUTURE = "f"
    AORIST = "a"
    IMPERFECT = "i"
    PERFECT = "x"
    PLUPERFECT = "y"
    FUTURE_PERFECT = "z"
    UNKNOWN = "-"


class Voice(InflexionBWG):
    """Word voice."""

    ACTIVE = "a"
    MIDDLE = "m"
    PASSIVE = "p"
    MIDDLE_PASSIVE = "e"
    UNKNOWN = "-"


class Person(InflexionBWG):
    """Word person."""

    FIRST = "1"
    SECOND = "2"
    THIRD = "3"
    UNKNOWN = "-"


class Degree(InflexionBWG):
    """Word degree."""

    COMPARATIVE = "c"
    SUPERLATIVE = "s"
    NONE = "n"  # POSITIVE
    UNKNOWN = "-"


class Type(InflexionBWG):
    """Type collection."""


class TypeNoun(Type):
    """Noun type."""

    COMMON = "c"
    PROPER = "p"
    UNKNOWN = "-"


class TypePronoun(Type):
    """Pronoun type."""

    PERSONAL = "p"
    RELATIVE = "r"
    DEMONSTRATIVE = "d"
    INTERROGATIVE = "q"
    INDEFINITE = "i"
    INTENSIVE = "t"
    REFLEXIVE = "x"
    RECIPROCAL = "e"
    UNKNOWN = "-"


class TypeAdjective(Type):
    """Adjective type."""

    NORMAL = "n"
    POSSESSIVE = "s"
    DEMONSTRATIVE = "d"
    INTERROGATIVE = "q"
    INDEFINITE = "i"
    INTENSIVE = "t"
    CARDINAL = "c"  # Cardinal number
    ORDINAL = "o"  # Ordinal number
    NUMERAL = "n"
    RELATIVE = "r"
    UNKNOWN = "-"


class TypeConjunction(Type):
    """Conjunction type."""

    SUBORDINATE = "s"
    COORDINATE = "c"
    UNKNOWN = "-"


class WordBWG(Word):
    """Represents a BibleWorks greek word."""

    def __init__(
            self, word: WordToken,
            speech: Speech,
            case: Case = None,
            gender: Gender = None,
            number: Number = None,
            i_type: Type = None,
            mood: Mood = None,
            tense: Tense = None,
            voice: Voice = None,
            person: Person = None,
            degree: Degree = None,
    ):
        Word.__init__(self, word)
        self._speech = speech
        self._case = case
        self._gender = gender
        self._number = number
        self._mood = mood
        self._tense = tense
        self._voice = voice
        self._person = person
        self._degree = degree
        self._type = i_type

    @property
    def speech(self) -> Speech:
        return self._speech

    @property
    def case(self) -> Case:
        return self._case

    @property
    def gender(self) -> Gender:
        return self._gender

    @property
    def number(self) -> Number:
        return self._number

    @property
    def mood(self) -> Mood:
        return self._mood

    @property
    def tense(self) -> Tense:
        return self._tense

    @property
    def voice(self) -> Voice:
        return self._voice

    @property
    def person(self) -> Person:
        return self._person

    @property
    def degree(self) -> Degree:
        return self._degree

    @property
    def type(self) -> Type:
        return self._type


class Combined(WordBWG):

    def __init__(self, word: WordToken, every: List[Word]):
        WordBWG.__init__(self, word, Speech.UNIDENTIFIED)
        self._every = every


class Compound(Combined):
    """Represents compound words with separate grammars."""

    @property
    def all(self) -> List[Word]:
        return self._every


class Split(Combined):
    """Represents words with alternative grammars."""

    @property
    def alternatives(self) -> List[Word]:
        return self._every


class Several(Combined):
    """Represents words with several grammars."""

    @property
    def multiple(self) -> List[Word]:
        return self._every


class Noun(WordBWG):

    def __init__(self, word: WordToken, case: CaseGeneric, gender: Gender, number: Number, i_type: TypeNoun):
        WordBWG.__init__(self, word, Speech.NOUN, case=case, gender=gender, number=number, i_type=i_type)


class Verb(WordBWG):

    def __init__(
            self, word: WordToken, case: CaseGeneric, gender: Gender, number: Number,
            mood: Mood, tense: Tense, voice: Voice, person: Person
    ):
        WordBWG.__init__(
            self, word, Speech.VERB, case=case, gender=gender,
            number=number, mood=mood, tense=tense, voice=voice, person=person
        )


class Adjective(WordBWG):

    def __init__(
            self, word: WordToken, case: CaseGeneric, gender: Gender,
            number: Number, i_type: TypeAdjective, degree: Degree
    ):
        WordBWG.__init__(
            self, word, Speech.ADJECTIVE, case=case, gender=gender,
            number=number, i_type=i_type, degree=degree
        )


class DefiniteArticle(WordBWG):

    def __init__(self, word: WordToken, case: CaseGeneric, gender: Gender, number: Number):
        WordBWG.__init__(self, word, Speech.DEFINITE_ARTICLE, case=case, gender=gender, number=number)


class Preposition(WordBWG):

    def __init__(self, word: WordToken, case: CasePreposition):
        WordBWG.__init__(self, word, Speech.PREPOSITION, case=case)


class Conjunction(WordBWG):

    def __init__(self, word: WordToken, i_type: TypeConjunction):
        WordBWG.__init__(self, word, Speech.CONJUNCTION, i_type=i_type)


class Particle(WordBWG):

    def __init__(self, word: WordToken):
        WordBWG.__init__(self, word, Speech.PARTICLE)


class Interjection(WordBWG):

    def __init__(self, word: WordToken):
        WordBWG.__init__(self, word, Speech.INTERJECTION)


class Adverb(WordBWG):

    def __init__(self, word: WordToken):
        WordBWG.__init__(self, word, Speech.ADVERB)


class Pronoun(WordBWG):

    def __init__(self, word: WordToken, case: CaseGeneric, gender: Gender, number: Number, i_type: TypePronoun):
        WordBWG.__init__(self, word, Speech.PRONOUN, case=case, gender=gender, number=number, i_type=i_type)


class Indeclinable(WordBWG):

    def __init__(self, word: WordToken):
        WordBWG.__init__(self, word, Speech.INDECLINABLE_NOUN)


class MorphologyBWG(Morphology):
    """Represents BibleWorks greek morphology."""

    @classmethod
    def parse(cls, token: WordToken) -> Word:
        morphology = list(token.grammar)
        speech = morphology.pop(0)

        if "/" in morphology:
            morphology = list()
            grammars = token.grammar.split("/")
            alts = list()

            for alt in grammars:
                alts.append(cls.parse(WordToken(word=token.word, lexeme=token.lexeme, grammar=alt)))

            word = Split(token, alts)
        elif "&" in morphology:
            morphology = list()
            grammars = token.grammar.split("&")

            if "+" in token.lexeme:
                every = list()
                lexemes = token.lexeme.split("+")

                for index in range(max(len(lexemes), len(grammars))):
                    every.append(cls.parse(
                        WordToken(word=lexemes[index], lexeme=lexemes[index], grammar=grammars[index])))

                word = Compound(token, every=every)
            else:
                several = list()

                for multi in grammars:
                    several.append(cls.parse(WordToken(word=token.word, lexeme=token.lexeme, grammar=multi)))

                word = Several(token, several)
        elif speech == Speech.NOUN:
            case = CaseGeneric.is_enumerated(morphology.pop(0))
            gender = Gender.is_enumerated(morphology.pop(0))
            number = Number.is_enumerated(morphology.pop(0))
            i_type = TypeNoun.is_enumerated(morphology.pop(0))

            word = Noun(word=token, case=case, gender=gender, number=number, i_type=i_type)
        elif speech == Speech.PRONOUN:
            i_type = TypePronoun.is_enumerated(morphology.pop(0))
            case = CaseGeneric.is_enumerated(morphology.pop(0))
            gender = Gender.is_enumerated(morphology.pop(0))
            number = Number.is_enumerated(morphology.pop(0))

            word = Pronoun(word=token, case=case, gender=gender, number=number, i_type=i_type)
        elif speech == Speech.DEFINITE_ARTICLE:
            case = CaseGeneric.is_enumerated(morphology.pop(0))
            gender = Gender.is_enumerated(morphology.pop(0))
            number = Number.is_enumerated(morphology.pop(0))

            word = DefiniteArticle(word=token, case=case, gender=gender, number=number)
        elif speech == Speech.VERB:
            mood = Mood.is_enumerated(morphology.pop(0))
            if mood == Mood.PARTICIPLE:
                tense = Tense.is_enumerated(morphology.pop(0))
                voice = Voice.is_enumerated(morphology.pop(0))
                case = CaseGeneric.is_enumerated(morphology.pop(0))
                gender = Gender.is_enumerated(morphology.pop(0))
                number = Number.is_enumerated(morphology.pop(0))
                person = None
            elif mood == Mood.INFINITIVE:
                tense = Tense.is_enumerated(morphology.pop(0))
                voice = Voice.is_enumerated(morphology.pop(0))
                case = None
                gender = None
                number = None
                person = None
            else:
                tense = Tense.is_enumerated(morphology.pop(0))
                voice = Voice.is_enumerated(morphology.pop(0))
                person = Person.is_enumerated(morphology.pop(0))
                number = Number.is_enumerated(morphology.pop(0))
                case = None
                gender = None

            word = Verb(
                word=token, case=case, gender=gender, number=number,
                mood=mood, tense=tense, voice=voice, person=person
            )
        elif speech == Speech.ADJECTIVE:
            i_type = TypeAdjective.is_enumerated(morphology.pop(0))
            case = CaseGeneric.is_enumerated(morphology.pop(0))
            gender = Gender.is_enumerated(morphology.pop(0))
            number = Number.is_enumerated(morphology.pop(0))
            degree = Degree.is_enumerated(morphology.pop(0))

            word = Adjective(word=token, case=case, gender=gender, number=number, i_type=i_type, degree=degree)
        elif speech == Speech.ADVERB:

            word = Adverb(word=token)
        elif speech == Speech.CONJUNCTION:
            i_type = TypeConjunction.is_enumerated(morphology.pop(0))

            word = Conjunction(word=token, i_type=i_type)
        elif speech == Speech.PREPOSITION:
            case = CasePreposition.is_enumerated(morphology.pop(0))

            word = Preposition(word=token, case=case)
        elif speech == Speech.PARTICLE:

            word = Particle(word=token)
        elif speech == Speech.INDECLINABLE_NOUN:

            word = Indeclinable(word=token)
        elif speech == Speech.INTERJECTION:

            word = Interjection(word=token)
        else:
            raise GrammarWarning("The current word token {} is of unknown class. {}".format(token.grammar, token))

        if len(morphology):
            raise GrammarWarning("Morphological grammatical incoherency in word: {}".format(token))

        return word


class Grammar:

    @classmethod
    def classify(cls, word: WordToken) -> Word:
        return MorphologyBWG.parse(word)
