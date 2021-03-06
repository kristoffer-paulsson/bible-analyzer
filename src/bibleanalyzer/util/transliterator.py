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
"""Ancient Greek transliterator."""

"""Bellow you find an example of all koine and coptic greek characters found at Wikipedia:
https://en.wikipedia.org/wiki/Greek_alphabet"""

ALL = """
Ͱ	ͱ	Ͳ	ͳ	ʹ	͵	Ͷ	ͷ			ͺ	ͻ	ͼ	ͽ	;	Ϳ
				΄	΅	Ά	·	Έ	Ή	Ί		Ό		Ύ	Ώ
ΐ	Α	Β	Γ	Δ	Ε	Ζ	Η	Θ	Ι	Κ	Λ	Μ	Ν	Ξ	Ο
Π	Ρ		Σ	Τ	Υ	Φ	Χ	Ψ	Ω	Ϊ	Ϋ	ά	έ	ή	ί
ΰ	α	β	γ	δ	ε	ζ	η	θ	ι	κ	λ	μ	ν	ξ	ο
π	ρ	ς	σ	τ	υ	φ	χ	ψ	ω	ϊ	ϋ	ό	ύ	ώ	Ϗ
ϐ	ϑ	ϒ	ϓ	ϔ	ϕ	ϖ	ϗ	Ϙ	ϙ	Ϛ	ϛ	Ϝ	ϝ	Ϟ	ϟ
Ϡ	ϡ	Ϣ	ϣ	Ϥ	ϥ	Ϧ	ϧ	Ϩ	ϩ	Ϫ	ϫ	Ϭ	ϭ	Ϯ	ϯ
ϰ	ϱ	ϲ	ϳ	ϴ	ϵ	϶	Ϸ	ϸ	Ϲ	Ϻ	ϻ	ϼ	Ͻ	Ͼ	Ͽ
ἀ	ἁ	ἂ	ἃ	ἄ	ἅ	ἆ	ἇ	Ἀ	Ἁ	Ἂ	Ἃ	Ἄ	Ἅ	Ἆ	Ἇ
ἐ	ἑ	ἒ	ἓ	ἔ	ἕ			Ἐ	Ἑ	Ἒ	Ἓ	Ἔ	Ἕ		
ἠ	ἡ	ἢ	ἣ	ἤ	ἥ	ἦ	ἧ	Ἠ	Ἡ	Ἢ	Ἣ	Ἤ	Ἥ	Ἦ	Ἧ
ἰ	ἱ	ἲ	ἳ	ἴ	ἵ	ἶ	ἷ	Ἰ	Ἱ	Ἲ	Ἳ	Ἴ	Ἵ	Ἶ	Ἷ
ὀ	ὁ	ὂ	ὃ	ὄ	ὅ			Ὀ	Ὁ	Ὂ	Ὃ	Ὄ	Ὅ		
ὐ	ὑ	ὒ	ὓ	ὔ	ὕ	ὖ	ὗ		Ὑ		Ὓ		Ὕ		Ὗ
ὠ	ὡ	ὢ	ὣ	ὤ	ὥ	ὦ	ὧ	Ὠ	Ὡ	Ὢ	Ὣ	Ὤ	Ὥ	Ὦ	Ὧ
ὰ	ά	ὲ	έ	ὴ	ή	ὶ	ί	ὸ	ό	ὺ	ύ	ὼ	ώ		
ᾀ	ᾁ	ᾂ	ᾃ	ᾄ	ᾅ	ᾆ	ᾇ	ᾈ	ᾉ	ᾊ	ᾋ	ᾌ	ᾍ	ᾎ	ᾏ
ᾐ	ᾑ	ᾒ	ᾓ	ᾔ	ᾕ	ᾖ	ᾗ	ᾘ	ᾙ	ᾚ	ᾛ	ᾜ	ᾝ	ᾞ	ᾟ
ᾠ	ᾡ	ᾢ	ᾣ	ᾤ	ᾥ	ᾦ	ᾧ	ᾨ	ᾩ	ᾪ	ᾫ	ᾬ	ᾭ	ᾮ	ᾯ
ᾰ	ᾱ	ᾲ	ᾳ	ᾴ		ᾶ	ᾷ	Ᾰ	Ᾱ	Ὰ	Ά	ᾼ	᾽	ι	᾿
῀	῁	ῂ	ῃ	ῄ		ῆ	ῇ	Ὲ	Έ	Ὴ	Ή	ῌ	῍	῎	῏
ῐ	ῑ	ῒ	ΐ			ῖ	ῗ	Ῐ	Ῑ	Ὶ	Ί		῝	῞	῟
ῠ	ῡ	ῢ	ΰ	ῤ	ῥ	ῦ	ῧ	Ῠ	Ῡ	Ὺ	Ύ	Ῥ	῭	΅	`
		ῲ	ῳ	ῴ		ῶ	ῷ	Ὸ	Ό	Ὼ	Ώ	ῼ	´	῾	
"""

UPPER = {
    'Ἁ', 'Ἃ', 'Ἅ', 'Ἇ', 'Ἑ', 'Ἓ', 'Ἕ', 'Ἡ', 'Ἣ', 'Ἥ', 'Ἧ', 'Ἱ', 'Ἳ', 'Ἵ', 'Ἷ', 'Ὁ', 'Ὃ', 'Ὅ', 'Ὑ', 'Ὓ', 'Ὕ', 'Ὗ', 'Ὡ',
    'Ὣ', 'Ὥ', 'Ὧ', 'ᾉ', 'ᾋ', 'ᾍ', 'ᾏ', 'ᾙ', 'ᾛ', 'ᾝ', 'ᾟ', 'ᾩ', 'ᾫ', 'ᾭ', 'ᾯ', 'Ῥ', 'ᾈ', 'ᾉ', 'ᾊ', 'ᾋ', 'ᾌ', 'ᾍ', 'ᾎ',
    'ᾏ', 'ᾘ', 'ᾙ', 'ᾚ', 'ᾛ', 'ᾜ', 'ᾝ', 'ᾞ', 'ᾟ', 'ᾨ', 'ᾩ', 'ᾪ', 'ᾫ', 'ᾬ', 'ᾭ', 'ᾮ', 'ᾯ', 'ᾼ', 'ῌ', 'ῼ', 'Ͱ', 'Ͳ', 'Ͷ',
    'Ϳ', 'Ά', 'Έ', 'Ή', 'Ί', 'Ό', 'Ύ', 'Ώ', 'Α', 'Β', 'Γ', 'Δ', 'Ε', 'Ζ', 'Η', 'Θ', 'Ι', 'Κ', 'Λ', 'Μ', 'Ν', 'Ξ', 'Ο',
    'Π', 'Ρ', 'Σ', 'Τ', 'Υ', 'Φ', 'Χ', 'Ψ', 'Ω', 'Ϊ', 'Ϋ', 'ϒ', 'ϓ', 'ϔ', 'ϕ', 'ϖ', 'Ϙ', 'Ϛ', 'Ϝ', 'Ϟ', 'ϡ', 'ϰ', 'ϴ',
    'Ϸ', 'Ϲ', 'Ϻ', 'Ͻ', 'Ͼ', 'Ͽ', 'Ἀ', 'Ἁ', 'Ἂ', 'Ἃ', 'Ἄ', 'Ἅ', 'Ἆ', 'Ἇ', 'Ἐ', 'Ἑ', 'Ἒ', 'Ἓ', 'Ἔ', 'Ἕ', 'Ἠ', 'Ἡ', 'Ἢ',
    'Ἣ', 'Ἤ', 'Ἥ', 'Ἦ', 'Ἧ', 'Ἰ', 'Ἱ', 'Ἲ', 'Ἳ', 'Ἴ', 'Ἵ', 'Ἶ', 'Ἷ', 'Ὀ', 'Ὁ', 'Ὂ', 'Ὃ', 'Ὄ', 'Ὅ', 'Ὑ', 'Ὓ', 'Ὕ', 'Ὗ',
    'Ὠ', 'Ὡ', 'Ὢ', 'Ὣ', 'Ὤ', 'Ὥ', 'Ὦ', 'Ὧ', 'Ᾰ', 'Ᾱ', 'Ὰ', 'Ά', 'Ὲ', 'Έ', 'Ὴ', 'Ή', 'Ῐ', 'Ῑ', 'Ὶ', 'Ί', 'Ῠ', 'Ῡ', 'Ὺ',
    'Ύ', 'Ῥ', 'Ὸ', 'Ό', 'Ὼ', 'Ώ'
}

ROUGH_UPPER = {
    'Ἁ', 'Ἃ', 'Ἅ', 'Ἇ', 'Ἑ', 'Ἓ', 'Ἕ', 'Ἡ', 'Ἣ', 'Ἥ', 'Ἧ', 'Ἱ', 'Ἳ', 'Ἵ', 'Ἷ', 'Ὁ', 'Ὃ', 'Ὅ', 'Ὑ', 'Ὓ', 'Ὕ', 'Ὗ', 'Ὡ',
    'Ὣ', 'Ὥ', 'Ὧ', 'ᾉ', 'ᾋ', 'ᾍ', 'ᾏ', 'ᾙ', 'ᾛ', 'ᾝ', 'ᾟ', 'ᾩ', 'ᾫ', 'ᾭ', 'ᾯ', 'Ῥ'
}

ROUGH_LOWER = {
    'ἁ', 'ἃ', 'ἅ', 'ἇ', 'ἑ', 'ἓ', 'ἕ', 'ἡ', 'ἣ', 'ἥ', 'ἧ', 'ἱ', 'ἳ', 'ἵ', 'ἷ', 'ὁ', 'ὃ', 'ὅ', 'ὐ', 'ὓ', 'ὕ', 'ὗ', 'ὡ',
    'ὣ', 'ὥ', 'ὧ', 'ᾁ', 'ᾃ', 'ᾅ', 'ᾇ', 'ᾑ', 'ᾓ', 'ᾕ', 'ᾗ', 'ᾡ', 'ᾣ', 'ᾥ', 'ᾧ', 'ῥ'
}

ROUGH = ROUGH_UPPER | ROUGH_LOWER | {"῝", "῞", "῟", "῾"}

GAMMA_NASAL = {
    "γγ": "νγ",
    "γκ": "νκ",
    "γχ": "νχ",
    "γξ": "νξ",
}

NORMALIZE = {
    'Ͱ': "Ͱ", 'ͱ': "ͱ", 'Ͳ': "Ϡ", 'ͳ': "ϡ", 'ʹ': "ʹ", '͵': "͵", 'Ͷ': "Ϝ", 'ͷ': "ϝ", 'ͺ': "ͺ", 'ͻ': "σ", 'ͼ': "σ",
    'ͽ': "σ", ';': ";", 'Ϳ': "Ϳ", '΄': "΄", '΅': "΅", 'Ά': "Α", '·': "·", 'Έ': "Ε", 'Ή': "Η", 'Ί': "Ι", 'Ό': "Ο",
    'Ύ': "Υ", 'Ώ': "Ω", 'ΐ': "ι", 'Α': "Α", 'Β': "Β", 'Γ': "Γ", 'Δ': "Δ", 'Ε': "Ε", 'Ζ': "Ζ", 'Η': "Η", 'Θ': "Θ",
    'Ι': "Ι", 'Κ': "Κ", 'Λ': "Λ", 'Μ': "Μ", 'Ν': "Ν", 'Ξ': "Ξ", 'Ο': "Ο", 'Π': "Π", 'Ρ': "Ρ", 'Σ': "Σ", 'Τ': "Τ",
    'Υ': "Υ", 'Φ': "Φ", 'Χ': "Χ", 'Ψ': "Ψ", 'Ω': "Ω", 'Ϊ': "Ι", 'Ϋ': "Υ", 'ά': "α", 'έ': "ε", 'ή': "η", 'ί': "ι",
    'ΰ': "υ", 'α': "α", 'β': "β", 'γ': "γ", 'δ': "δ", 'ε': "ε", 'ζ': "ζ", 'η': "η", 'θ': "θ", 'ι': "ι", 'κ': "κ",
    'λ': "λ", 'μ': "μ", 'ν': "ν", 'ξ': "ξ", 'ο': "ο", 'π': "π", 'ρ': "ρ", 'ς': "ς", 'σ': "σ", 'τ': "τ", 'υ': "υ",
    'φ': "φ", 'χ': "χ", 'ψ': "ψ", 'ω': "ω", 'ϊ': "ι", 'ϋ': "υ", 'ό': "ο", 'ύ': "υ", 'ώ': "ω", 'Ϗ': "και", 'ϐ': "Β",
    'ϑ': "Θ", 'ϒ': "Υ", 'ϓ': "Υ", 'ϔ': "Υ", 'ϕ': "Φ", 'ϖ': "Π", 'ϗ': "και", 'Ϙ': "Ϟ", 'ϙ': "ϟ", 'Ϛ': "Ϛ", 'ϛ': "ϛ",
    'Ϝ': "Ϝ", 'ϝ': "ϝ", 'Ϟ': "Ϟ", 'ϟ': "ϟ", 'Ϡ': "Ϡ", 'ϡ': "ϡ", 'Ϣ': "Ϣ", 'ϣ': "ϣ", 'Ϥ': "Ϥ", 'ϥ': "ϥ", 'Ϧ': "Ϧ",
    'ϧ': "ϧ", 'Ϩ': "Ϩ", 'ϩ': "ϩ", 'Ϫ': "Ϫ", 'ϫ': "ϫ", 'Ϭ': "Ϭ", 'ϭ': "ϭ", 'Ϯ': "Ϯ", 'ϯ': "ϯ", 'ϰ': "Κ", 'ϱ': "ρ",
    'ϲ': "σ", 'ϳ': "ϳ", 'ϴ': "Θ", 'ϵ': "ε", '϶': "ε", 'Ϸ': "Ϸ", 'ϸ': "ϸ", 'Ϲ': "Σ", 'Ϻ': "Ϻ", 'ϻ': "ϻ", 'ϼ': "ρ",
    'Ͻ': "Σ", 'Ͼ': "Σ", 'Ͽ': "Σ", 'ἀ': "α", 'ἁ': "α", 'ἂ': "α", 'ἃ': "α", 'ἄ': "α", 'ἅ': "α", 'ἆ': "α", 'ἇ': "α",
    'Ἀ': "Α", 'Ἁ': "Α", 'Ἂ': "Α", 'Ἃ': "Α", 'Ἄ': "Α", 'Ἅ': "Α", 'Ἆ': "Α", 'Ἇ': "Α", 'ἐ': "ε", 'ἑ': "ε", 'ἒ': "ε",
    'ἓ': "ε", 'ἔ': "ε", 'ἕ': "ε", 'Ἐ': "Ε", 'Ἑ': "Ε", 'Ἒ': "Ε", 'Ἓ': "Ε", 'Ἔ': "Ε", 'Ἕ': "Ε", 'ἠ': "η", 'ἡ': "η",
    'ἢ': "η", 'ἣ': "η", 'ἤ': "η", 'ἥ': "η", 'ἦ': "η", 'ἧ': "η", 'Ἠ': "Η", 'Ἡ': "Η", 'Ἢ': "Η", 'Ἣ': "Η", 'Ἤ': "Η",
    'Ἥ': "Η", 'Ἦ': "Η", 'Ἧ': "Η", 'ἰ': "ι", 'ἱ': "ι", 'ἲ': "ι", 'ἳ': "ι", 'ἴ': "ι", 'ἵ': "ι", 'ἶ': "ι", 'ἷ': "ι",
    'Ἰ': "Ι", 'Ἱ': "Ι", 'Ἲ': "Ι", 'Ἳ': "Ι", 'Ἴ': "Ι", 'Ἵ': "Ι", 'Ἶ': "Ι", 'Ἷ': "Ι", 'ὀ': "ο", 'ὁ': "ο", 'ὂ': "ο",
    'ὃ': "ο", 'ὄ': "ο", 'ὅ': "ο", 'Ὀ': "Ο", 'Ὁ': "Ο", 'Ὂ': "Ο", 'Ὃ': "Ο", 'Ὄ': "Ο", 'Ὅ': "Ο", 'ὐ': "υ", 'ὑ': "υ",
    'ὒ': "υ", 'ὓ': "υ", 'ὔ': "υ", 'ὕ': "υ", 'ὖ': "υ", 'ὗ': "υ", 'Ὑ': "Υ", 'Ὓ': "Υ", 'Ὕ': "Υ", 'Ὗ': "Υ", 'ὠ': "ω",
    'ὡ': "ω", 'ὢ': "ω", 'ὣ': "ω", 'ὤ': "ω", 'ὥ': "ω", 'ὦ': "ω", 'ὧ': "ω", 'Ὠ': "Ω", 'Ὡ': "Ω", 'Ὢ': "Ω", 'Ὣ': "Ω",
    'Ὤ': "Ω", 'Ὥ': "Ω", 'Ὦ': "Ω", 'Ὧ': "Ω", 'ὰ': "α", 'ά': "α", 'ὲ': "ε", 'έ': "ε", 'ὴ': "η", 'ή': "η", 'ὶ': "ι",
    'ί': "ι", 'ὸ': "ο", 'ό': "ο", 'ὺ': "υ", 'ύ': "υ", 'ὼ': "ω", 'ώ': "ω", 'ᾰ': "α", 'ᾱ': "α", 'ᾶ': "α", 'Ᾰ': "Α",
    'Ᾱ': "Α", 'Ὰ': "Α", 'Ά': "Α", '᾽': "᾽", 'ι': "ι", '᾿': "᾿", '῀': "῀", '῁': "῁", 'ῆ': "η", 'Ὲ': "Ε", 'Έ': "Ε",
    'Ὴ': "Η", 'Ή': "Η", '῍': "῍", '῎': "῎", '῏': "῏", 'ῐ': "ι", 'ῑ': "ι", 'ῒ': "ι", 'ΐ': "ι", 'ῖ': "ι", 'ῗ': "ι",
    'Ῐ': "Ι", 'Ῑ': "Ι", 'Ὶ': "Ι", 'Ί': "Ι", '῝': "῝", '῞': "῞", '῟': "῟", 'ῠ': "υ", 'ῡ': "υ", 'ῢ': "υ", 'ΰ': "υ",
    'ῤ': "ρ", 'ῥ': "ρ", 'ῦ': "υ", 'ῧ': "υ", 'Ῠ': "Υ", 'Ῡ': "Υ", 'Ὺ': "Υ", 'Ύ': "Υ", 'Ῥ': "Ρ", '῭': "῭", '΅': "΅",
    '`': "`", 'ῶ': "ω", 'Ὸ': "Ο", 'Ό': "Ο", 'Ὼ': "Ω", 'Ώ': "Ω", '´': "´", '῾': "῾", 'ι': "ι"
}

EXPAND = {
    'ᾀ': "ἀι", 'ᾁ': "ἁι", 'ᾂ': "ἂι", 'ᾃ': "ἃι", 'ᾄ': "ἄι", 'ᾅ': "ἅι", 'ᾆ': "ἆι", 'ᾇ': "ἇι", 'ᾈ': "Ἀι", 'ᾉ': "Ἁι",
    'ᾊ': "Ἂι", 'ᾋ': "Ἃι", 'ᾌ': "Ἄι", 'ᾍ': "Ἅι", 'ᾎ': "Ἆι", 'ᾏ': "Ἇι", 'ᾐ': "ἠι", 'ᾑ': "ἡι", 'ᾒ': "ἢι", 'ᾓ': "ἣι",
    'ᾔ': "ἤι", 'ᾕ': "ἥι", 'ᾖ': "ἦι", 'ᾗ': "ἧι", 'ᾘ': "Ἠι", 'ᾙ': "Ἡι", 'ᾚ': "Ἢι", 'ᾛ': "Ἣι", 'ᾜ': "Ἤι", 'ᾝ': "Ἥι",
    'ᾞ': "Ἦι", 'ᾟ': "Ἧι", 'ᾠ': "ὠι", 'ᾡ': "ὡι", 'ᾢ': "ὢι", 'ᾣ': "ὣι", 'ᾤ': "ὤι", 'ᾥ': "ὥι", 'ᾦ': "ὦι", 'ᾧ': "ὧι",
    'ᾨ': "Ὠι", 'ᾩ': "Ὡι", 'ᾪ': "Ὢι", 'ᾫ': "Ὣι", 'ᾬ': "Ὤι", 'ᾭ': "Ὥι", 'ᾮ': "Ὦι", 'ᾯ': "Ὧι", 'ᾲ': "ὰι", 'ᾳ': "αι",
    'ᾴ': "άι", 'ᾷ': "ᾶι", 'ᾼ': "Αι", 'ῂ': "ὴι", 'ῃ': "ηι", 'ῄ': "ήι", 'ῇ': "ῆι", 'ῌ': "Ηι", 'ῲ': "ὼι", 'ῳ': "ωι",
    'ῴ': "ώι", 'ῷ': "ῶι", 'ῼ': "Ωι"
}

CLEAN = {
    'ᾀ': "ἀ", 'ᾁ': "ἁ", 'ᾂ': "ἂ", 'ᾃ': "ἃ", 'ᾄ': "ἄ", 'ᾅ': "ἅ", 'ᾆ': "ἆ", 'ᾇ': "ἇ", 'ᾈ': "Ἀ", 'ᾉ': "Ἁ",
    'ᾊ': "Ἂ", 'ᾋ': "Ἃ", 'ᾌ': "Ἄ", 'ᾍ': "Ἅ", 'ᾎ': "Ἆ", 'ᾏ': "Ἇ", 'ᾐ': "ἠ", 'ᾑ': "ἡ", 'ᾒ': "ἢ", 'ᾓ': "ἣ",
    'ᾔ': "ἤ", 'ᾕ': "ἥ", 'ᾖ': "ἦ", 'ᾗ': "ἧ", 'ᾘ': "Ἠ", 'ᾙ': "Ἡ", 'ᾚ': "Ἢ", 'ᾛ': "Ἣ", 'ᾜ': "Ἤ", 'ᾝ': "Ἥ",
    'ᾞ': "Ἦ", 'ᾟ': "Ἧ", 'ᾠ': "ὠ", 'ᾡ': "ὡ", 'ᾢ': "ὢ", 'ᾣ': "ὣ", 'ᾤ': "ὤ", 'ᾥ': "ὥ", 'ᾦ': "ὦ", 'ᾧ': "ὧ",
    'ᾨ': "Ὠ", 'ᾩ': "Ὡ", 'ᾪ': "Ὢ", 'ᾫ': "Ὣ", 'ᾬ': "Ὤ", 'ᾭ': "Ὥ", 'ᾮ': "Ὦ", 'ᾯ': "Ὧ", 'ᾲ': "ὰ", 'ᾳ': "α",
    'ᾴ': "ά", 'ᾷ': "ᾶ", 'ᾼ': "Α", 'ῂ': "ὴ", 'ῃ': "η", 'ῄ': "ή", 'ῇ': "ῆ", 'ῌ': "Η", 'ῲ': "ὼ", 'ῳ': "ω",
    'ῴ': "ώ", 'ῷ': "ῶ", 'ῼ': "Ω"
}

LETTERS = set(NORMALIZE.keys()) | set(EXPAND.keys())

SBL_DIPHTONGS = {
    "ay": "au",
    "ey": "eu",
    "ey": "ēu",
    "oy": "ou",
    "yi": "ui"
}

# Letters
CHAR = (
    "ALPHA", "BETA", "GAMMA", "DELTA", "EPSILON", "ZETA", "ETA", "THETA", "IOTA", "KAPPA", "LAMBDA", "MU", "NU", "XI",
    "OMICRON", "PI", "RHO", "SIGMA", "TAU", "UPSILON", "PHI", "CHI", "PSI", "OMEGA")

GREEK_LATIN = {
    'α': "a",
    'β': "b",
    'γ': "g",
    'δ': "d",
    'ε': "e",
    'ζ': "dz",
    'η': "ē",
    'θ': "th",
    'ι': "i",
    'κ': "k",
    'λ': "l",
    'μ': "m",
    'ν': "n",
    'ξ': "x",
    'ο': "o",
    'π': "p",
    'ρ': "r",
    'σ': "s",
    'ς': "s",
    'τ': "t",
    'υ': "u",
    'φ': "ph",
    'χ': "kh",
    'ψ': "ps",
    'ω': "ō",
}

SBL_GREEK_LATIN = {
    'α': "a",
    'β': "b",
    'γ': "g",
    'δ': "d",
    'ε': "e",
    'ζ': "z",
    'η': "ē",
    'θ': "th",
    'ι': "i",
    'κ': "k",
    'λ': "l",
    'μ': "m",
    'ν': "n",
    'ξ': "x",
    'ο': "o",
    'π': "p",
    'ρ': "r",  # "rh"
    'σ': "s",
    'ς': "s",
    'τ': "t",
    'υ': "y",
    'φ': "ph",
    'χ': "ch",
    'ψ': "ps",
    'ω': "ō",
}


class KoineTransliterator:
    """Transliterates ancient greek into exact transliteration."""

    @classmethod
    def latinize(cls, word: str) -> str:
        bits = list(cls.gamma_nasal(cls.normalize(word)))
        upper = bits[0].isupper()
        transliterated = "h" if cls.has_rough(word) else ""

        for char in bits:
            char = char.lower()
            transliterated += GREEK_LATIN[char] if char in GREEK_LATIN else char

        return transliterated.title() if upper else transliterated

    @classmethod
    def transliterate(cls, word: str) -> str:
        bits = list(cls.gamma_nasal(cls.normalize2(word)))
        upper = bits[0].isupper()
        transliterated = "h" if cls.has_rough(word) else ""

        for char in bits:
            char = char.lower()
            transliterated += SBL_GREEK_LATIN[char] if char in SBL_GREEK_LATIN else char

        transliterated = cls.diphthongs(transliterated)

        return transliterated.title() if upper else transliterated

    @classmethod
    def diphthongs(cls, word: str) -> str:
        for i, j in SBL_DIPHTONGS.items():
            word = word.replace(i, j)
        return word

    @classmethod
    def normalize(cls, word: str) -> str:
        bits = list(cls.expand(word))
        normal = ""

        for char in bits:
            normal += NORMALIZE[char] if char in NORMALIZE else char

        return normal

    @classmethod
    def normalize2(cls, word: str) -> str:
        bits = list(cls.clean(word))
        normal = ""

        for char in bits:
            normal += NORMALIZE[char] if char in NORMALIZE else char

        return normal

    @classmethod
    def expand(cls, word: str) -> str:
        bits = list(word)
        expand = ""

        for char in bits:
            expand += EXPAND[char] if char in EXPAND.keys() else char

        return expand

    @classmethod
    def clean(cls, word: str) -> str:
        bits = list(word)
        expand = ""

        for char in bits:
            expand += CLEAN[char] if char in CLEAN.keys() else char

        return expand

    @classmethod
    def gamma_nasal(cls, word: str) -> str:
        for i, j in GAMMA_NASAL.items():
            word = word.replace(i, j)
        return word

    @classmethod
    def contains_upper(cls, word: str) -> bool:
        return bool(UPPER.intersection(set(word)))

    @classmethod
    def has_rough(cls, word: str) -> bool:
        return bool(ROUGH.intersection(set(word)))

    @classmethod
    def koine_only(cls, word: str) -> bool:
        return bool(LETTERS.intersection(set(word)) == set(word))
