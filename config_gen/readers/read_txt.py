"""
:author: samu
:created: 2/20/13 8:33 PM
"""

from __future__ import absolute_import

from config_gen.readers import register


@register('txt')
def csv_reader(filename):
    with open(filename, 'r') as f:
        return f.read()
