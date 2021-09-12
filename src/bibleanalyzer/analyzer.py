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
"""Context analyzer and meaning builder."""
from bibleanalyzer.grammar import Grammar, Word, Speech, Mood
from bibleanalyzer.model import WordToken, Token, PunctuationToken, SectionToken, ChapterToken, VerseToken
from bibleanalyzer.structor import Clause


class GrammarRule:
    LINK_NOUN = 1
    NOUN_TO_VERB = 2


class Analyzer:
    def __init__(self):
        pass

    @classmethod
    def analyze(cls, clause: Clause) -> list:
        grammar = dict()
        for index, token in enumerate(clause.line):
            if isinstance(token, WordToken):
                word = Grammar.classify(token)
                if word.speech in (Speech.NOUN, Speech.PRONOUN, Speech.DEFINITE_ARTICLE, Speech.ADJECTIVE):
                    cls._add_rule(grammar, cls.link_noun(word), index)
                # if word.speech in (Speech.VERB,) and word.mood == Mood.PARTICIPLE:
                #    cls._add_rule(grammar, cls.link_verb(word), index)

        terms = set()
        for value in grammar.values():
            subs = ""
            for index in value:
                subs += " " + clause.line[index].lexeme

            terms.add(subs.strip())
        return terms

    @classmethod
    def link_noun(cls, word: Word):
        return GrammarRule.LINK_NOUN, word.case, word.gender, word.number

    @classmethod
    def link_verb(cls, word: Word):
        return GrammarRule.NOUN_TO_VERB, word.case, word.gender, word.number

    @classmethod
    def _add_rule(cls, grammar: dict, rule: tuple, index: int):
        if rule not in grammar:
            grammar[rule] = list()
        grammar[rule].append(index)

