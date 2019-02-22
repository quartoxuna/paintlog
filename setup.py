#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from setuptools import setup

exec(compile(open('./paintlog.py').read(), './paintlog.py', 'exec'))

setup(
    # Summary
    name="paintlog",
    version=__version__,
    description="Enables colored log messages for Python's default logging module",
    author="Kai Borowiak",
    author_email="kai.borowiak@secunet.de",
    keywords='python logging colorama',
    license='GPLv3',
    classifiers = [
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],

    # Contents
    py_modules=['paintlog'],
    test_suite='test',

    # Dependencies
    dependency_links=['http://sinaqs.secunet.de/pypi/'],

    install_requires=[
        'colorama',
    ],

    tests_require=[
        'mock',
    ]
)
