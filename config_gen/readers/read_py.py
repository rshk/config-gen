"""
:author: samu
:created: 2/20/13 8:35 PM
"""

import imp
import os
from config_gen.readers import register
from config_gen.readers.base import BaseFileAccessor


@register('py')
class PyFileAccessor(BaseFileAccessor):
    def __init__(self, filename):
        super(PyFileAccessor, self).__init__(filename)
        _file_base_name = os.path.splitext(os.path.basename(filename))[0]
        with open(self.filename, 'r') as module_file:
            self._module = imp.load_module(
                'cfgfile_%s' % _file_base_name,
                module_file,
                './mods/mymodule.py',
                ('.py', 'U', 1))

    def keys(self):
        return dir(self._module)

    def __getitem__(self, item):
        member = getattr(self._module, item)
        if callable(member):
            return member()
        else:
            return member
