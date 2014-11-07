#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from setuptools import setup

setup(
	name="paintlog",
	version="1.2",
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
)
