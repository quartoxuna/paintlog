#!/usr/bin/env python
# -*- coding: utf-8 -*-

r"""
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
   formatter = paintlog.ColoredFormatter(
                   '%(asctime)s [%(levelname)-8s] %(message)s', '%Y-%m-%dT%H:%M:%S'
               )

   ch.setFormatter(formatter)
   logger.addHandler(ch)

   # Log various messages
   logger.debug("Debug Message")
   logger.warning("Warning Message")
   logger.info("Info Message")
   logger.error("Error Message")
   logger.critical("Critical Message")

.. rubric:: Output:

.. raw:: html

    <div style='background-color:black;color:white;font-family:Courier New;'>
        2018-12-04T12:02:43 [<span style='color:green;'>DEBUG</span>] Debug Message<br/>
        2018-12-04T12:02:44 [<span style='color:magenta;'>WARINING</span>] Warning Message<br/>
        2018-12-04T12:02:45 [<span style='color:cyan;'>INFO</span>] Info Message<br/>
        2018-12-04T12:02:46 [<span style='color:red;'>ERROR</span>] Error Message<br/>
        2018-12-04T12:02:47 [<span style='background-color:red;color:white;'>CRITICAL
    </span>] Critical Message
    </div>

|
|

Configuration
-------------

You can change the Coloring of all attribute on the fly via the **update()** method.

The first parameter ist the *loglevel* that you want to change, while the other arguments are
passed as *\*\*kwargs* and represent all attributes, which are avaialable for a default LogRecord,
according to Python's internal *logging* module.

.. code-block:: python

   formatter.update(logging.DEBUG, levelname=paintlog.Foreground.CYAN,
                    message=paintlog.Background.CYAN)
   formatter.update(logging.WARNING,
                    levelname=paintlog.Foreground.MAGENTA + paintlog.Foreground.White)
   formatter.update(logging.INFO, levelname=paintlog.Foreground.WHITE,
                    message=paintlog.Foreground.GREEN)
   formatter.update(logging.ERROR, levelname=paintlog.Background.RED + paintlog.Foreground.WHITE)
   formatter.update(logging.CRITICAL, levelname=paintlog.Foreground.RED)

..  rubric:: Output:

.. raw:: html

   <div style='background-color:black;color:white;font-family:Courier New;'>
       2018-12-04T12:03:40 [<span style='color:cyan;'>DEBUG</span>]
   <span style='background-color:cyan;'>Debug Message</span><br/>
       2018-12-04T12:03:41 [<span style='background-color:magenta;color:white;'>WARNING</span>]
   Warning Message<br/>
       2018-12-04T12:03:42 [<span style='color:white;'>INFO</span>]
   <span style='color:green;'>Info Message</span><br/>
       2018-12-04T12:03:43 [<span style='background-color:red;color:white;'>ERROR</span>]
   Error Message<br/>
       2018-12-04T12:03:44 [<span style='color:red;'>CRITICAL</span>] Critical Message
   </div>


|
|

General Log Level Coloring
--------------------------

In addition to configuring each attribute, there's also the possibility to color the whole message,
also using the **update()** method and the special *general* keyword argument.

.. code-block:: python

   formatter.update(logging.CRITICAL, general=paintlog.Background.RED + paintlog.Foreground.WHITE)

..  rubric:: Output:

.. raw:: html

   <div style='background-color:black;color:white;font-family:Courier New;'>
       2018-12-04T12:04:43 [<span style='color:cyan;'>DEBUG</span>]
   <span style='background-color:cyan;'>Debug Message</span><br/>
       2018-12-04T12:04:44 [<span style='background-color:magenta;color:white;'>WARNING</span>]
   Warning Message<br/>
       2018-12-04T12:04:45 [<span style='color:white;'>INFO</span>]
   <span style='color:green;'>Info Message</span><br/>
       2018-12-04T12:04:46 [<span style='background-color:red;color:white;'>ERROR</span>]
   Error Message<br/>
       <span style='color:white;background-color:red;'>2018-12-04T12:04:47 [CRITICAL]
   Critical Message</span>
   </div>
"""

__all__ = ["ColoredFormatter", "Foreground", "Background", "Style"]

import re
import logging

from colorama import init as colorama_init
from colorama import Fore as Foreground
from colorama import Back as Background
from colorama import Style

# Initialize Colorama
colorama_init()

class ColoredFormatter(logging.Formatter):
    """Colored logging Formatter"""

    # Regex to identiy format string members
    FORMAT_STRING_ATTRIBUTE = r"(%%\((%s)\)[0-9-.]*[dfs]{1})"

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
        self._rules[logging.INFO]['levelname'] = Foreground.BLUE
        self._rules[logging.WARNING]['levelname'] = Foreground.MAGENTA
        self._rules[logging.ERROR]['levelname'] = Foreground.RED
        self._rules[logging.CRITICAL]['levelname'] = Foreground.WHITE + Background.RED

    def update(self, level, general=None, **attrs):
        """Change ruleset for specified log level.

        :param int level: Log level to change (according to `mod:logging` Module
        ;param int general: General color definition for all attributes of the specified log level
        :param dict attrs: Attributes to change for specified log level
        """
        current_level = self._rules[level]
        if general:
            for key in list(self.BLANK_RULE_SET.keys()):
                current_level[key] = general
        else:
            for key, value in list(attrs.items()):
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

        # Check if general rule is active
        # Check if all rules have the same color definition
        if len(set(self._rules[loglevel].values())) == 1:
            color = list(self._rules[loglevel].values()).pop()
            # Style the complete string
            fmt = color + fmt + Style.RESET_ALL
        else:
            # Iterate over ruleset for the given log level
            # and set original attribute with color definition in front of it
            # Reset all styles at the end of the attribute
            for attr, color in list(self._rules[loglevel].items()):
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
