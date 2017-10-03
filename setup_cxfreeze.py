# -*- coding:utf-8 -*-
# created by Toons on 01/05/2017
# try:
# 	from setuptools import setup
# 	import wheel
# except ImportError:
# from distutils.core import setup
from cx_Freeze import setup, Executable
import sys
import os

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ['os','requests','cffi','idna'], 
					# "excludes": [],
					# "include_files" : [('/usr/local/lib/python3.5/dist-packages/.libs_cffi_backend',
					# 				os.getenv('HOME').format('/python/oxycoin/build/exe.linux-x86_64-3.5/lib/python3.5')),
                    #                 ('/usr/local/lib/python3.5/dist-packages/_cffi_backend.cpython-35m-x86_64-linux-gnu.so',
					# 				os.getenv('HOME').format('/python/oxycoin/build/exe.linux-x86_64-3.5/lib/python3.5'))]
					}

base = None
if sys.platform == "win32":
	base = "Win32GUI"
kw = {}
f = open("VERSION", "r")
long_description = open("readme.rst", "r")
kw.update(**{
	"version": f.read().strip(),
	"name": "pyoxy",
	"keywords": ["api", "Oxycoin"],
	"author": "Toons",
	"author_email": "moustikitos@gmail.com",
	"maintainer": "Toons",
	"maintainer_email": "moustikitos@gmail.com",
	"url": "https://github.com/ArkEcosystem/pyoxy",
	"download_url": "https://github.com/ArkEcosystem/pyoxy.git",
	# "include_package_data": True,
	"description": ".",
	"long_description": long_description.read(),
	"packages": ["pyoxy", "pyoxy.cli"],
	"scripts": ["pyoxy-cli.py"],
	# "install_requires": ["requests", "pynacl", "pytz", "docopt"],
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
	'executables':[Executable("pyoxy-ui.py", base=base)]
})
long_description.close()
f.close()

setup(**kw)
