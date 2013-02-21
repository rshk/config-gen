"""
:author: samu
:created: 2/20/13 8:28 PM
"""

import os
from config_gen.exceptions import UnsupportedConfFile
from config_gen.utils import GenericRegister

## Warning! Never access to this one directly!
register = GenericRegister()
_register_imported = False


def get_readers():
    import pkgutil
    global _register_imported
    if not _register_imported:
        for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
            ## By loading this, its content will be registered
            ## in the above register.
            loader.find_module(module_name).load_module(module_name)
        _register_imported = True
    return register


def get_file_reader_class(filename):
    ext = os.path.splitext(filename)[1][1:]
    try:
        return get_readers()[ext]
    except KeyError:
        raise UnsupportedConfFile


def get_file_reader(filename):
    return get_file_reader_class(filename)(filename)
