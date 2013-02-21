"""
Config-gen: CSV reader
"""

from __future__ import absolute_import

from config_gen.readers import register


@register('csv')
def csv_reader(filename):
    """
    Reads a Comma-Separated Values file into a list of tuples.

    The CSV file must be comma-separated (semicolons are not supported).
    Fields containing commas must be enclosed in double quotes.
    """
    import csv
    ## We have to preload everything in a list, otherwise we
    ## will not be able to iterate more than once..
    ## (todo: find a better solution for this?)
    with open(filename, 'r') as f:
        return list(csv.reader(f, delimiter=","))
