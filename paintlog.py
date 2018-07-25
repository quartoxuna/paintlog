#!/usr/bin/env python

"""
@author: Kai Borowiak
@requires: logging>=2.7
@requires: colorama>=0.2.5
@summary: Colored string formatting for Python's default logging module
"""

__all__ = ["ColoredFormatter","Foreground","Background","Style"]

import re
import logging

from colorama import init as colorama_init
from colorama import Fore as Foreground
from colorama import Back as Background
from colorama import Style

# Initialize Colorama
colorama_init()

ALIGNMENT_REGEX = re.compile("%\(levelname\)-?(?P<alignment>\d*)s")

class ColoredFormatter(logging.Formatter):
    """Colored formatter
    @cvar coloring: Default color rules for the default log levels
    @type coloring: dict
    """


    def __init__(self, *args, **kwargs):
        logging.Formatter.__init__(self, *args, **kwargs)
        # Set default rules
        self._rules = {
                          logging.DEBUG: Foreground.GREEN,
                          logging.INFO: Foreground.CYAN,
                          logging.WARNING: Foreground.MAGENTA,
                          logging.ERROR: Foreground.RED,
                          logging.CRITICAL: Foreground.WHITE + Background.RED
                      }

    def __setitem__(self, level, color):
        """Changes color definitions for log levels.
        @param level: The Level to change
        @type level: int
        @param color: The color for the level
        @type color: int
        @param kwargs: Multi rule setting
        @type kwargs: **kwargs
        """
        self._rules[level] = color

    def format(self, record):
        """Extends default formatting.
        @param record: The log record to format
        @type record: LogRecord
        @returns: Formatted and colored string
        @rtype: str
        """
        # Fix alignment issue when formatting ANSI codes
        # Get the wanted length of the 'levelname' in our format string
        # and the pad the length of the real levelname (e.g. 'INFO')
        # to that size
        # This has to be done, since python formatting does not handle
        # ANSI reset codes well and strips backspaces after it.
        try:
            alignment = int(ALIGNMENT_REGEX.search(self._fmt).groups("alignment")[0])
        except:
            alignment = 0
        alignment -= len(record.levelname)
        if alignment < 0:
            alignment = 0
        record.levelname = self._rules[record.levelno] + record.levelname + Style.RESET_ALL + " " * alignment
        return logging.Formatter.format(self,record)
