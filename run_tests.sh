#!/bin/sh

#python -m unittest discover -s tests -v
py.test -v --pep8 --cov=config_gen --cov-report=term-missing tests
