#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PaintLog
========

Colored Formatter for Python.

How to Use:
-----------

.. rubric:: Example:

.. code-block:: python

   import logging
   import paintlog

   logger = logging.getLogger()
   logger.setLevel(logging.DEBUG)

   ch = logging.StreamHandler()
   ch.setLevel(logging.DEBUG)#

   # Create Colored Formatter like normal formatter
   formatter = paintlog.ColoredFormatter('[%(levelname)s] %(message)s')

   ch.setFormatter(fmt)
   logger.addHandler(ch)

   # Log various messages
   logger.debug("Debug Message")
   logger.warning("Warning Message")
   logger.info("Info Message")
   logger.error("Error Message")
   logger.critical("Critical Message")

.. rubric:: Output:

.. raw:: html

    <div style='background-color:black;color:white;'>
        [<span style='color:green;font-family:Courier New;'>DEBUG</span>] Debug Message<br/>
        [<span style='color:magenta;font-family:Courier New;'>WARINING</span>] Warning Message<br/>
        [<span style='color:cyan;font-famiy:Courier New;'>INFO</span>] Info Message<br/>
        [<span style='color:red;font-family:Courier New;'>ERROR</span>] Error Message<br/>
        [<span style='background-color:red;color:white;font-family:Courier New;'>CRITICAL</span>] Critical Message
    </div>

|
|

Configuration
-------------

You can change the Coloring on the fly via the **__setitem__** method.

.. code-block:: python

   fmt['DEBUG']    = paintlog.Foreground.CYAN
   fmt['WARNING']  = paintlog.Background.MAGENTA + paintlog.Foreground.WHITE
   fmt['INFO']     = paintlog.Foreground.WHITE
   fmt['ERROR']    = paintlog.Background.RED + paintlog.Foreground.WHITE
   fmt['CRITICAL'] = paintlog.Foreground.RED

..  rubric:: Output:

.. raw:: html

   <div style='background-color:black;color:white;'>
       [<span style='color:cyan;font-family:Courier New;'>DEBUG</span>] Debug Message<br/>
       [<span style='background-color:magenta;color:white;font-family:Courier New;'>WARNING</span>] Warning Message<br/>
       [<span style='color:white;font-famiy:Courier New;'>INFO</span>] Info Message<br/>
       [<span style='background-color:red;color:white;font-family:Courier New;'>ERROR</span>] Error Message<br/>
       [<span style='color:red;font-family:Courier New;'>CRITICAL</span>] Critical Message
   </div>
"""

__all__ = ["ColoredFormatter","Foreground","Background","Style"]

__version__ = "2.1.1"

import re
import logging

from colorama import init as colorama_init
from colorama import Fore as Foreground
from colorama import Back as Background
from colorama import Style

# Initialize Colorama
colorama_init()

class ColoredFormatter(logging.Formatter):

    # Regex to identiy format string members
    FORMAT_STRING_ATTRIBUTE = '(%%\((%s)\)[0-9-.]*[dfs]{1})'

    # Blank Rule Set for a LogRecord
    BLANK_RULE_SET = {
        'asctime': Style.RESET_ALL,
        'created': Style.RESET_ALL,
        'filename': Style.RESET_ALL,
        'funcName': Style.RESET_ALL,
        'levelname': Style.RESET_ALL,
        'levelno': Style.RESET_ALL,
        'lineno': Style.RESET_ALL,
        'module': Style.RESET_ALL,
        'msecs': Style.RESET_ALL,
        'message': Style.RESET_ALL,
        'name': Style.RESET_ALL,
        'pathname': Style.RESET_ALL,
        'process': Style.RESET_ALL,
        'processName': Style.RESET_ALL,
        'relativeCreated': Style.RESET_ALL,
        'thread': Style.RESET_ALL,
        'threadName': Style.RESET_ALL
    }

    def __init__(self, *args, **kwargs):
        logging.Formatter.__init__(self, *args, **kwargs)

        # Store original format string
        self._original_fmt = self._fmt

        # Set default rules
        self._rules = {
            logging.DEBUG: self.BLANK_RULE_SET.copy(),
            logging.INFO: self.BLANK_RULE_SET.copy(),
            logging.WARNING: self.BLANK_RULE_SET.copy(),
            logging.ERROR: self.BLANK_RULE_SET.copy(),
            logging.CRITICAL: self.BLANK_RULE_SET.copy()
        }
        self._rules[logging.DEBUG]['levelname'] = Foreground.GREEN
        self._rules[logging.INFO]['levelname'] = Foreground.CYAN
        self._rules[logging.WARNING]['levelname'] = Foreground.MAGENTA
        self._rules[logging.ERROR]['levelname'] = Foreground.RED
        self._rules[logging.CRITICAL]['levelname'] = Foreground.WHITE + Background.RED

    def update(self, level, **attrs):
        """Change ruleset for specified log level.

        :param int level: Log level to change (according to `mod:logging` Module
        :param dict attrs: Attributes to change for specified log level
        """
        current_level = self._rules[level]
        for key, value in attrs.items():
            current_level[key] = value

    def __setitem__(self, level, color):
        """Changes color definitions for the levelname attribute of the log record.

        :param int level: The level to be changed
        :param int color: Color definition according to `mod:colorama` module
        """
        self._rules[level]['levelname'] = color

    def _get_colored_format_string(self, loglevel, reset_style=True):
        """Returns updated format string using color definitions for the specified loglevel

        :param int loglevel: Wanted Log Level
        :param bool reset_style: Reset all Styles at the end of format string attribute
        """
        fmt = self._original_fmt
        # Iterate over ruleset for the given log level
        # and set original attribute with color definition in front of it
        # Reset all styles at the end of the attribute
        for attr, color in self._rules[loglevel].items():
            # Find format string of attribute
            match = re.compile(self.FORMAT_STRING_ATTRIBUTE % attr).search(fmt)
            if match:
                # Replace in reverse order so that the end position
                # is not shifted to the right during the replacement
                # at the start position
                if reset_style:
                    fmt = fmt[:match.end()] + Style.RESET_ALL + fmt[match.end():]
                fmt = fmt[:match.start()] + color + fmt[match.start():]
        return fmt

    def format(self, record):
        """Changes the used format string according to relevant log level"""
        self._fmt = self._get_colored_format_string(record.levelno)
        return logging.Formatter.format(self, record)
