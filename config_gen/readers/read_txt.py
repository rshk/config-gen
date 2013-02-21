"""
Config-gen: TXT reader
"""

from __future__ import absolute_import

from config_gen.readers import register


@register('txt')
def txt_reader(filename):
    """
    Loads a plain text file, returning its raw content directly.
    """
    with open(filename, 'r') as f:
        return f.read()
