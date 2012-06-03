#!/usr/bin/env python

from setuptools import setup

setup(
    name='Config-gen',
    version='0.1',
    description='Utility to generate configuration files',
    author='Samuele Santi',
    author_email='samuele@santi.co.it',
    url='https://github.com/rshk/config-gen',
    scripts=['gencfg.py'],
    #data_files=['README.rst'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Topic :: Utilities",
    ],
    install_requires=["jinja2", "demjson"],
)
