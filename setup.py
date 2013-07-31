#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='Config-gen',
    version=__import__('config_gen').__version__,
    description='Utility to generate configuration files',
    author='Samuele Santi',
    author_email='samuele@samuelesanti.com',
    url='https://github.com/rshk/config-gen',
    license='GNU General Public License v3 or later (GPLv3+)',
    packages=find_packages(exclude=('tests',)),
    #data_files=['README.rst', 'LICENSE'],
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: "
        "GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Utilities",
    ],
    install_requires=[
        "cool_logging",
        "jinja2",
    ],
    entry_points={
        'console_scripts': [
            'confgen-render = config_gen.commands.render:command',
            'confgen-quickstart = config_gen.commands.quickstart:command',
            'confgen-render-file = config_gen.commands.render_file:command',
        ],
    },
    test_suite='tests',
)
