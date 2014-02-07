#!/usr/bin/env python

"""
@author: Kai Borowiak
@version: 1.0
@since: 06.03.2013
@requires: logging>=2.7
@requires: colorama>=0.2.5
@summary: Colored string formatting for Python's default logging module
"""
try:
	from colorama import Fore
	from colorama import Back
	from colorama import Style
	from colorama import init as color_init
except ImportError,ie:
	raise RuntimeError("It seems, you don't have installed the colorama module (%s)" % str(ie))

import copy
import logging

color_init()

class Formatter(logging.Formatter):
	"""Colored formatter
	@cvar coloring: Default color rules for the default log levels
	@type coloring: dict
	"""
	coloring = {
	        'DEBUG': Fore.WHITE,
	        'INFO': Fore.WHITE,
	        'WARNING': Fore.WHITE,
	        'ERROR': Fore.WHITE,
	        'CRITICAL': Fore.WHITE
	}

	def __init__(self,fmt=None,datefmt=None,bright=True):
		logging.Formatter.__init__(self,fmt,datefmt)
		self.__rules = Formatter.coloring
		self.__bright = bright

	def setColor(self,level=None,color=None,**kwargs):
		"""Changes color definitions for log levels.
		@param level: The Level to change
		@type level: int
		@param color: The color for the level
		@type color: int
		@param kwargs: Multi rule setting
		@type kwargs: **kwargs
		"""
		if level and color:
			self.__rules[level] = color
			if self.__bright:
				self.__rules[level] += Style.BRIGHT
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
		msg = logging.Formatter.format(self,record)
		levelname = logging.getLevelName(record.levelno)
		
		# Insert colors
		msg = msg.replace("<color>",self.__rules[levelname]).replace("</color>",Style.RESET_ALL)
		
		# Insert styles
		msg = msg.replace("<b>",Style.DIM).replace("</b>",Style.RESET_ALL)
		
		# Return new formatted message
		return msg