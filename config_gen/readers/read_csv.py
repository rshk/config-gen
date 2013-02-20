"""
:author: samu
:created: 2/20/13 8:33 PM
"""

from __future__ import absolute_import

from config_gen.readers import register


@register('csv')
def csv_reader(filename):
    import csv
    return csv.reader(open(filename, 'r'), delimiter=",")
    ## If we use a with statement here, the file will be closed..
    # with open(filename, 'r') as f:
    #     reader = csv.reader(f, delimiter=",")
    # return reader
