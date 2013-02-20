"""
:author: samu
:created: 2/20/13 8:33 PM
"""

from __future__ import absolute_import

from config_gen.readers import register


@register('csv')
def csv_reader(filename):
    import csv
    with open(filename, 'r') as f:
        return csv.reader(f, delimiter=",")
