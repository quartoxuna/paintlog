#!/usr/bin/env python

from setuptools import setup

setup(
	name="paintlog",
	version="1.1",
	description="Enables colored log messages for Python's default logging module",
	author="Kai Borowiak",
	author_email="kai.borowiak@secunet.de",
	packages=['paintlog'],
	long_description="""\
	Provides custom Formatter using the 'colorama' module
	to generate colored log messages in Python.
	""",
	classifiers=[
		"License :: OSI Approved :: GNU General Public License (GPL)",
		"Programming Language :: Python",
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
	],
	keywords='python logging colorama',
	license='GPL',
	install_requires=['colorama'],
	dependency_links=['http://sinaqs.secuent.de/pybasket/']
)
