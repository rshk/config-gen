"""
:author: samu
:created: 2/20/13 8:33 PM
"""

from __future__ import absolute_import

from config_gen.readers import register


@register('csv')
def csv_reader(filename):
    import csv
    ## We have to preload everything in a list, otherwise we
    ## will not be able to iterate more than once..
    ## (todo: find a better solution for this?)
    with open(filename, 'r') as f:
        return list(csv.reader(f, delimiter=","))
