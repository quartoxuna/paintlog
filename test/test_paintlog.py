#!/usr/bin/env python

# IMPORTS
import re
import mock
import unittest

import logging
from paintlog import ColoredFormatter

class Test_ColoredFormatter(unittest.TestCase):
    """Test Cases for ColoredFormatter"""

    def test_rule_update(self):
        """Update of Color Definition"""
        fmt = ColoredFormatter()
        fmt.update(logging.INFO, message='RED', levelname='GREEN')
        self.assertEquals(fmt._rules[logging.INFO]['message'], 'RED')
        self.assertEquals(fmt._rules[logging.INFO]['levelname'], 'GREEN')

    def test_setitem_compatabilty(self):
        """Backwards compatability for __setitem__ method"""
        fmt = ColoredFormatter()
        fmt[logging.INFO] = 'RED'
        self.assertEquals(fmt._rules[logging.INFO]['levelname'], 'RED')

    def test_color_formatting_no_reset(self):
        """Replacement of format string without style reset"""
        fmt = ColoredFormatter('%(message)s')
        level = logging.INFO
        fmt.update(level, message='RED')
        string = fmt._get_colored_format_string(level, reset_style=False)
        self.assertEquals(string, 'RED%(message)s')

    def test_color_formatting_reset(self):
        """Replacement of format string with style reset"""
        fmt = ColoredFormatter('%(message)s')
        level = logging.INFO
        fmt.update(level, message='RED')
        string = fmt._get_colored_format_string(level)
        reset_string = '\x1b[0m'
        self.assertEquals(string, 'RED' + '%(message)s' + reset_string)

class Test_FormatStringRegex(unittest.TestCase):
    """Test Cases for Format String Search"""

    def test_embedded(self):
        """Check String: 'XXX%(message)sXX'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'message')
        fmt = 'XXX%(message)sXX'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEquals(match.start(), 3)
        self.assertEquals(match.end(), 14)

    def test_embedded_whitespace(self):
        """Check String: '   %(message)s  '"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'message')
        fmt = '   %(message)s  '
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEquals(match.start(), 3)
        self.assertEquals(match.end(), 14)

    def test_embedded_d(self):
        """Check String: 'ddd%(message)sdd'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'message')
        fmt = 'ddd%(message)sdd'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEquals(match.start(), 3)
        self.assertEquals(match.end(), 14)

    def test_embedded_s(self):
        """Check String: 'sss%(message)sss'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'message')
        fmt = 'sss%(message)sss'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEquals(match.start(), 3)
        self.assertEquals(match.end(), 14)

    def test_embedded_f(self):
        """Check String: 'fff%(message)sff'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'message')
        fmt = 'fff%(message)sff'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEquals(match.start(), 3)
        self.assertEquals(match.end(), 14)

    def test_embedded_dot(self):
        """Check String: '...%(message)s..'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'message')
        fmt = '...%(message)s..'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEquals(match.start(), 3)
        self.assertEquals(match.end(), 14)

    def test_embedded_percent(self):
        """Check String: '%%%%(message)s%%'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'message')
        fmt = '%%%%(message)s%%'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEquals(match.start(), 3)
        self.assertEquals(match.end(), 14)

    def test_string(self):
        """Check String: '%(message)s'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'message')
        fmt = '%(message)s'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEquals(match.start(), 0)
        self.assertEquals(match.end(), len(fmt))

    def test_string_width(self):
        """Check String: '%(levelname)20s'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'levelname')
        fmt = '%(levelname)20s'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEquals(match.start(), 0)
        self.assertEquals(match.end(), len(fmt))

    def test_string_alignment(self):
        """Check String: '%(levelname)-20s'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'levelname')
        fmt = '%(levelname)-20s'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEquals(match.start(), 0)
        self.assertEquals(match.end(), len(fmt))

    def test_decimal(self):
        """Check Decimal: '%(levelno)d'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'levelno')
        fmt = '%(levelno)s'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEquals(match.start(), 0)
        self.assertEquals(match.end(), len(fmt))

    def test_decimal_width(self):
        """Check Decimal: '%(levelno)10d'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'levelno')
        fmt = '%(levelno)10d'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEquals(match.start(), 0)
        self.assertEquals(match.end(), len(fmt))

    def test_decimal_alignment(self):
        """Check Decimal: '%(levelno)-5d'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'levelno')
        fmt = '%(levelno)-5d'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEquals(match.start(), 0)
        self.assertEquals(match.end(), len(fmt))

    def test_float(self):
        """Check Float: '%(created)f'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'created')
        fmt = '%(created)f'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEquals(match.start(), 0)
        self.assertEquals(match.end(), len(fmt))

    def test_float_width(self):
        """Check Float: '%(created)10f'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'created')
        fmt = '%(created)10f'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEquals(match.start(), 0)
        self.assertEquals(match.end(), len(fmt))

    def test_float_alignment(self):
        """Check Float: '%(created)-5f'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'created')
        fmt = '%(created)-5f'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEquals(match.start(), 0)
        self.assertEquals(match.end(), len(fmt))

    def test_float_percision(self):
        """Check Float: '%(created)-10.2f'"""
        regex = re.compile(ColoredFormatter.FORMAT_STRING_ATTRIBUTE % 'created')
        fmt = '%(created)-10.2f'
        match = regex.search(fmt)
        self.assertIsNotNone(match)
        self.assertEquals(match.start(), 0)
        self.assertEquals(match.end(), len(fmt))

if __name__ == "__main__":
    unittest.main()
