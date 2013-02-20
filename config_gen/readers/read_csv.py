"""
:author: samu
:created: 2/20/13 8:33 PM
"""

from __future__ import absolute_import

from config_gen.readers import register
from config_gen.readers.base import BaseFileAccessor
import csv


@register('csv')
class CsvFileAccessor(BaseFileAccessor):
    def __init__(self, filename):
        super(CsvFileAccessor, self).__init__(filename)

    def __iter__(self):
        reader = csv.reader(open(self.filename, 'r'), delimiter=",")
        return iter(reader)
