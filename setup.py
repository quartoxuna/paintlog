#!/usr/bin/env python

from setuptools import setup

setup(
	name="colored-logging",
	version="1.0",
	description="Enables colored log messages for Python's default logging module",
	author="Kai Borowiak",
	packages=['colored_logging'],
	install_requires=[
		'colorama>=0.2.5'
	],
)
