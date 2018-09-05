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
   formatter = paintlog.ColoredFormatter('%(asctime)s [%(levelname)s] %(message)s')

   ch.setFormatter(fmt)
   logger.addHandler(ch)

   # Log various messages
   logger.debug("Debug")
   logger.warning("Warning")
   logger.info("Info")
   logger.error("Error")
   logger.critical("Critical")

.. rubric:: Output:

.. raw:: html

   <div style='background-color:black;'>
       <div style='color:green;font-family:Courier New;'>Debug</div>
       <div style='color:magenta;font-family:Courier New;'>Warning</div>
       <div style='color:cyan;font-famiy:Courier New;'>Info</div>
       <div style='color:red;font-family:Courier New;'>Error</div>
       <div style='background-color:red;color:white;font-family:Courier New;'>Critical</div>
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

   <div style='background-color:black;'>
       <div style='color:cyan;font-family:Courier New;'>Debug</div>
       <div style='background-color:magenta;color:white;font-family:Courier New;'>Warning</div>
       <div style='color:white;font-famiy:Courier New;'>Info</div>
       <div style='background-color:red;color:white;font-family:Courier New;'>Error</div>
       <div style='color:red;font-family:Courier New;'>Critical</div>
   </div>
"""

__all__ = ["ColoredFormatter","Foreground","Background","Style"]

__version__ = "2.1.0"

import re
import copy
import logging

from colorama import init as colorama_init
from colorama import Fore as Foreground
from colorama import Back as Background
from colorama import Style

# Initialize Colorama
colorama_init()

ALIGNMENT_REGEX = re.compile("%\(levelname\)-?(?P<alignment>\d*)s")

class ColoredFormatter(logging.Formatter):

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
        styled_record = copy.copy(record)
        styled_record.levelname = self._rules[record.levelno] + record.levelname + Style.RESET_ALL + " " * alignment
        return logging.Formatter.format(self,styled_record)
