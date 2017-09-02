# -*- coding:utf-8 -*-
# created by Toons on 01/05/2017
try:
	from setuptools import setup
	import wheel
except ImportError:
	from distutils.core import setup

kw = {}
f = open("VERSION", "r")
long_description = open("readme.rst", "r")
kw.update(**{
	"version": f.read().strip(),
	"name": "Oxypytus",
	"keywords": ["api", "Oxycoin"],
	"author": "Toons",
	"author_email": "moustikitos@gmail.com",
	"maintainer": "Toons",
	"maintainer_email": "moustikitos@gmail.com",
	"url": "https://github.com/ArkEcosystem/pyoxy",
	"download_url": "https://github.com/ArkEcosystem/pyoxy.git",
	"include_package_data": True,
	"description": ".",
	"long_description": long_description.read(),
	"packages": ["pyoxy"],
	"scripts": [],
	"install_requires": ["requests", "pynacl", "pytz", "docopt"],
	"license": "Copyright 2017 Toons, MIT licence",
	"classifiers": [
		'Development Status :: 4 - Beta',
		'Environment :: Console',
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'Intended Audience :: End Users/Desktop',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
	],
})
long_description.close()
f.close()

setup(**kw)
