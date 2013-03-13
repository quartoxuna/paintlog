#!/usr/bin/env python

from setuptools import setup

setup(
	name="paintlog",
	version="1.0",
	description="Enables colored log messages for Python's default logging module",
	author="Kai Borowiak",
	packages=['paintlog'],
	install_requires=[
		'colorama>=0.2.5'
	],
	dependency_links=[
		'http://192.168.2.20/basket/',
	],
)
