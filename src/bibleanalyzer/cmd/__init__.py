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
"""The CMD (command) package stores all executable commands of the BibleAnalyzer.
The init also contains the Command baseclass."""
import importlib
from argparse import Namespace

from ..config import Config
from ..data import NAME, VERSION
from ..logging import Logger


class Command:
    logger = None

    def __init__(self, config: Config, args: Namespace):
        self.logger.info("Running command: {}".format(self.__class__.__name__))
        self.logger.info("using parameters: {}.".format(args))

        self._args = args
        self._validate(config)
        self._config = config

    @classmethod
    def execute(cls, args):
        config = Config()
        cls.logger = Logger.create(config, args.command)

        try:
            klass = getattr(
                importlib.import_module("bibleanalyzer.cmd.{}".format(args.command)),
                "{}Command".format(args.command.capitalize())
            )

            cmd = klass(config, args)
            cmd()
        except Exception as e:
            cls.logger.critical("There was a bug in {} {}.".format(NAME, VERSION), exc_info=e)

    def _validate(self, config):
        if not config.get("corpus").is_dir():
            raise RuntimeError("Corpus directory not found, {}".format(config.get("corpus")))
        self.logger.info("Corpus directory: {}".format(config.get("corpus")))
        if not config.get("cache").is_dir():
            raise RuntimeError("Cache directory not found, {}".format(config.get("logs")))
        self.logger.info("Cache directory: {}".format(config.get("cache")))

    def __call__(self):
        raise NotImplementedError()


__all__ = [
    "Command"
]
