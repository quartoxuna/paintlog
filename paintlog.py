# -*- coding: utf-8 -*-

__version__ = '2.0.0'

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

__all__ = ['ColoredFormatter', 'Fore', 'Back', 'Style']

import re
import logging

import colorama
from colorama import Style
from colorama import Fore as Fore
from colorama import Back as Back

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
        return self.__rules

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
