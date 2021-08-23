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
"""Setup for the Bible Analyzer project."""
import sys
from pathlib import Path, PurePath

from setuptools import setup

here = PurePath(__file__)
sys.path.append(here.parents[0].joinpath("src"))

from bibleanalyzer.data import NAME, VERSION

AUTHOR = "Kristoffer Paulsson"
EMAIL = "kristoffer.paulsson@talenten.se"
DESCRIPTION = """Bible text analyzer of the greek new and old testament."""
LONG_DESCRIPTION = Path("README.md").read_text()

setup(
    name=NAME,
    version=VERSION,
    license="ISC",
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    entry_points={"console_scripts": ["bible-analyzer = bibleanalyzer.main:main"]},
    classifiers=[
        "Intended Audience :: Religion",
        "License :: OSI Approved :: ISC License (ISCL)"
    ],
    package_dir={"": "src"},
    packages=["bibleanalyzer"],
    python_requires=">=3.8, <4"
)
