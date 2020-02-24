#!/usr/bin/env python

"""
UnitTests for paintlog module
-----------------------------
"""

# IMPORTS
import unittest

import re
import logging

from paintlog import ColoredFormatter


class TestColoredFormatter(unittest.TestCase):
    """Test Cases for ColoredFormatter"""

    def test_default(self):
        """Default behaviour"""
        fmt = ColoredFormatter('%(name)s %(levelname)s %(message)s')
        record = logging.LogRecord(name='logger', level=logging.INFO, pathname='/tmp',
                                   lineno=23, msg="Something", args=[], exc_info=None, func=None)
        output = fmt.format(record)
        self.assertEqual("logger INFO Something", output)

    def test_definition_level(self):
        """Test format definition for log level"""
        fmt = ColoredFormatter('%(name)s %(levelname)s %(message)s',
                               DEBUG={'levelname': ('GREEN', 'RESET')})
        record = logging.LogRecord(name='logger', level=logging.DEBUG, pathname='/tmp',
                                   lineno=23, msg="Something", args=[], exc_info=None, func=None)
        output = fmt.format(record)
        self.assertEqual("logger GREENDEBUGRESET Something", output)

    def test_full_redefinition(self):
        """Test format of whole output"""
        fmt = ColoredFormatter('%(name)s %(levelname)s %(message)s',
                               DEBUG={'FULL': ('GREEN', 'RESET')})
        record = logging.LogRecord(name='logger', level=logging.DEBUG, pathname='/tmp',
                                   lineno=23, msg="Something", args=[], exc_info=None, func=None)
        output = fmt.format(record)
        self.assertEqual("GREENlogger DEBUG SomethingRESET", output)


class TestFormatStringRegex(unittest.TestCase):
    """Test Cases for Format String Search"""

    def test_embedded(self):
        """Check String: 'XXX%(message)sXX'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'message')
        fmt = 'XXX%(message)sXX'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEqual(match.start(), 3)
        self.assertEqual(match.end(), 14)

    def test_embedded_whitespace(self):
        """Check String: '   %(message)s  '"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'message')
        fmt = '   %(message)s  '
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEqual(match.start(), 3)
        self.assertEqual(match.end(), 14)

    def test_embedded_d(self):
        """Check String: 'ddd%(message)sdd'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'message')
        fmt = 'ddd%(message)sdd'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEqual(match.start(), 3)
        self.assertEqual(match.end(), 14)

    def test_embedded_s(self):
        """Check String: 'sss%(message)sss'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'message')
        fmt = 'sss%(message)sss'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEqual(match.start(), 3)
        self.assertEqual(match.end(), 14)

    def test_embedded_f(self):
        """Check String: 'fff%(message)sff'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'message')
        fmt = 'fff%(message)sff'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEqual(match.start(), 3)
        self.assertEqual(match.end(), 14)

    def test_embedded_dot(self):
        """Check String: '...%(message)s..'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'message')
        fmt = '...%(message)s..'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEqual(match.start(), 3)
        self.assertEqual(match.end(), 14)

    def test_embedded_percent(self):
        """Check String: '%%%%(message)s%%'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'message')
        fmt = '%%%%(message)s%%'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEqual(match.start(), 3)
        self.assertEqual(match.end(), 14)

    def test_string(self):
        """Check String: '%(message)s'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'message')
        fmt = '%(message)s'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), len(fmt))

    def test_string_width(self):
        """Check String: '%(levelname)20s'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'levelname')
        fmt = '%(levelname)20s'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), len(fmt))

    def test_string_alignment(self):
        """Check String: '%(levelname)-20s'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'levelname')
        fmt = '%(levelname)-20s'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), len(fmt))

    def test_decimal(self):
        """Check Decimal: '%(levelno)d'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'levelno')
        fmt = '%(levelno)s'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), len(fmt))

    def test_decimal_width(self):
        """Check Decimal: '%(levelno)10d'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'levelno')
        fmt = '%(levelno)10d'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), len(fmt))

    def test_decimal_alignment(self):
        """Check Decimal: '%(levelno)-5d'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'levelno')
        fmt = '%(levelno)-5d'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), len(fmt))

    def test_float(self):
        """Check Float: '%(created)f'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'created')
        fmt = '%(created)f'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), len(fmt))

    def test_float_width(self):
        """Check Float: '%(created)10f'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'created')
        fmt = '%(created)10f'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), len(fmt))

    def test_float_alignment(self):
        """Check Float: '%(created)-5f'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'created')
        fmt = '%(created)-5f'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), len(fmt))

    def test_float_percision(self):
        """Check Float: '%(created)-10.2f'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'created')
        fmt = '%(created)-10.2f'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEqual(match.start(), 0)
        self.assertEqual(match.end(), len(fmt))
