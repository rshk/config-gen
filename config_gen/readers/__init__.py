"""
:author: samu
:created: 2/20/13 8:28 PM
"""

import os
from config_gen.utils import GenericRegister

register = GenericRegister()


def get_readers():
    from config_gen.readers import read_csv
    from config_gen.readers import read_ini
    from config_gen.readers import read_json
    from config_gen.readers import read_py
    return register


def get_file_reader(filename):
    ext = os.path.splitext(filename)[1][1:]
    return get_readers()[ext](filename)
