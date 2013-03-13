#!/usr/bin/env python

"""
@author: Kai Borowiak
@version: 1.0
@since: 06.03.2013
@requires: logging>=2.7
@requires: colorama>=0.2.5
@summary: Colored string formatting for Python's default logging module
"""

from colorama import Fore as foreground
from colorama import Back as background
from colorama import Style as style
from colorama import init as color_init
import copy
import logging

color_init()

class Formatter(logging.Formatter):
	"""Colored formatter
	@cvar coloring: Default color rules for the default log levels
	@type coloring: dict
	"""
	coloring = {
	        'DEBUG': foreground.WHITE,
	        'INFO': foreground.WHITE,
	        'WARNING': foreground.WHITE,
	        'ERROR': foreground.WHITE,
	        'CRITICAL': foreground.WHITE
	}

	def __init__(self,fmt=None,datefmt=None):
		super(Formatter,self).__init__(fmt,datefmt)
		self.__rules = Formatter.coloring

	def setColoring(self,level,color):
		"""Changes color definitions for log levels.
		@param level: The number of the loglevel to change
		@type level: int
		@param color: The ANSI sequence for the color, usually from the already imported 'foregorund' module
		@type color: str
		"""
		self.__rules[logging.getLevelName(level)] = color
		
	def format(self, record):
		"""Extends default formatting.
		@param record: The log record to format
		@type record: LogRecord
		@returns: Formatted and colored string
		@rtype: str
		"""
		msg = super(Formatter,self).format(record)
		levelname = logging.getLevelName(record.levelno)
		
		# Insert colors
		msg = msg.replace("<color>",self.__rules[levelname]).replace("</color>",foreground.RESET)
		
		# Insert styles
		msg = msg.replace("<b>",style.DIM).replace("</b>",style.RESET_ALL)
		
		# Return new formatted message
		return msg