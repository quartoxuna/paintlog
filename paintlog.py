# -*- coding: utf-8 -*-

"""
Paintlog
--------
"""

import re
import logging

import colorama
from colorama import Style
from colorama import Fore
from colorama import Back

__all__ = ['ColoredFormatter', 'Fore', 'Back', 'Style']

# Initialize colorama
colorama.init()

# Reset rule set
DEFAULT_RULE_SET = {
    'asctime': ('', ''),
    'created': ('', ''),
    'filename': ('', ''),
    'funcName': ('', ''),
    'levelname': ('', ''),
    'levelno': ('', ''),
    'lineno': ('', ''),
    'module': ('', ''),
    'msecs': ('', ''),
    'message': ('', ''),
    'name': ('', ''),
    'pathname': ('', ''),
    'process': ('', ''),
    'processName': ('', ''),
    'relativeCreated': ('', ''),
    'thread': ('', ''),
    'threadName': ('', '')
}


class ColoredFormatter(logging.Formatter):
    """Colored logging Formatter"""

    # Regex to identiy format string members
    FORMAT_STRING_ATTRIBUTE = r"(%%\((%s)\)[0-9-.]*[dfs]{1})"

    def __init__(self, fmt=None, datefmt=None, **kwargs):
        # Store original format
        self.__original_fmt = fmt

        # Store rule definitions per log level
        self.__rules = {}
        for lvl in range(0, 60, 10):
            # Load default rule set
            self.__rules[lvl] = DEFAULT_RULE_SET.copy()

            # Extend with specified values
            levelname = logging.getLevelName(lvl)
            self.__rules[lvl].update(kwargs.pop(levelname, DEFAULT_RULE_SET))

        super(ColoredFormatter, self).__init__(fmt, datefmt, **kwargs)

    @property
    def rules(self):
        """Returns the current rule definitions

        :rtype: dict
        """
        return self.__rules

    # pylint: disable=protected-access
    def format(self, record):
        # Python 3.x compatabiity
        if getattr(self, '_style', None):
            self._style._fmt = self.__original_fmt
        else:
            self._fmt = self.__original_fmt

        # Get the rule deifnition for the current log level
        rules = self.__rules[record.levelno]

        # Check if general rule is active
        if 'FULL' in rules:
            preformat, postformat = rules['FULL']

            # Reformat the whole string
            if getattr(self, '_style', None):
                self._style._fmt = preformat + self._fmt + postformat
            else:
                self._fmt = preformat + self._fmt + postformat
        else:
            # Iterate over ruleset for the given log level
            # and set original attribute with color definition in front of it
            # Reset all styles at the end of the attribute
            for attr, (preformat, postformat) in list(self.__rules[record.levelno].items()):
                # Check if we have any formatting information
                if not preformat and not postformat:
                    continue

                # Find format string of attribute
                match = re.search(self.FORMAT_STRING_ATTRIBUTE % attr, self._fmt)
                if match:
                    # Replace in reverse order so that the end position
                    # is not shifted to the right during the replacement
                    # at the start position]
                    if getattr(self, '_style', None):
                        self._style._fmt = self._style._fmt[:match.end()] +\
                                           postformat +\
                                           self._style._fmt[match.end():]
                        self._style._fmt = self._style._fmt[:match.start()] +\
                                           preformat +\
                                           self._style._fmt[match.start():]
                    else:
                        self._fmt = self._fmt[:match.end()] +\
                                    postformat +\
                                    self._fmt[match.end():]
                        self._fmt = self._fmt[:match.start()] +\
                                    preformat +\
                                    self._fmt[match.start():]

        return logging.Formatter.format(self, record)
