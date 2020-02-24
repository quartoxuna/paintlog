#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=missing-module-docstring,exec-used

# IMPORTS
import setuptools

# Get version
VERSION = {}
with open("./version.py") as fp:
    exec(fp.read(), VERSION)

# Get long description from README.md
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="paintlog",
    version=VERSION['__version__'],
    author="Kai Borowiak",
    author_email="borowiak.kai@gmail.com",
    description="Colored log messages for Python's default logging module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/quartoxuna/paintlog",
    py_modules=['paintlog'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent"
    ],

    test_suite='tests',
    install_requires=[
        'colorama',
    ],
)
