#!/usr/bin/env python

"""
@author: Kai Borowiak
@requires: logging>=2.7
@requires: colorama>=0.2.5
@summary: Colored string formatting for Python's default logging module
"""

__all__ = ["ColoredFormatter","Foreground","Background","Style"]

import colorama
import logging

import colorama
colorama.init()

from colorama import Fore as Foreground
from colorama import Back as Background
from colorama import Style

class ColoredFormatter(logging.Formatter):
    """Colored formatter
    @cvar coloring: Default color rules for the default log levels
    @type coloring: dict
    """

    DEFAULT_RULES = {\
                        logging.DEBUG: Foreground.GREEN,\
                        logging.INFO: Foreground.CYAN,\
                        logging.WARNING: Foreground.MAGENTA,\
                        logging.ERROR: Foreground.RED,\
                        logging.CRITICAL: Foreground.WHITE + Background.RED\
                    }

    def __init__(self, *args, **kwargs):
        logging.Formatter.__init__(self, *args, **kwargs)
        # Set default rules
        self._rules = ColoredFormatter.DEFAULT_RULES

    def setRule(self,level=None,color=None,**kwargs):
        """Changes color definitions for log levels.
        @param level: The Level to change
        @type level: int
        @param color: The color for the level
        @type color: int
        @param kwargs: Multi rule setting
        @type kwargs: **kwargs
        """
        if level and color:
            self._rules[level] = color
        elif len(kwargs)>0:
            for level,color in kwargs.items():
                self.setColor(level,color)

    def format(self, record):
        """Extends default formatting.
        @param record: The log record to format
        @type record: LogRecord
        @returns: Formatted and colored string
        @rtype: str
        """
        levelno = record.levelno
        record.levelname = self._rules[levelno] + record.levelname
        # Reset coloring
        record.levelname += Style.RESET_ALL
        return logging.Formatter.format(self,record)
