#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from setuptools import setup

exec(compile(open('./paintlog.py').read(), './paintlog.py', 'exec'))

setup(
    name="paintlog",
    version=__version__,
    description="Enables colored log messages for Python's default logging module",
    author="Kai Borowiak",
    author_email="kai.borowiak@secunet.de",
    py_modules=['paintlog'],
    keywords='python logging colorama',
    license='GPL',
    dependency_links=['http://sinaqs.secunet.de/pypi/'],
    install_requires=[
        'colorama',
    ],
    tests_require=[
        'mock',
    ],
    test_suite='test',
    zip_safe=False,
)
