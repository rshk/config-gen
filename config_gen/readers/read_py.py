"""
Config-gen: PY reader
"""

import imp
import os
from UserDict import DictMixin

from config_gen.readers import register
from config_gen.utils import lazy_property


@register('py')
class PyFileAccessor(object, DictMixin):
    """
    Loads and returns a Python module.

    The module content will then be fully accessible from the template.
    """

    def __init__(self, filename):
        self.filename = filename

    @lazy_property
    def _module(self):
        _file_base_name = os.path.splitext(os.path.basename(self.filename))[0]
        with open(self.filename, 'r') as module_file:
            modname = 'cfgfile_%s' % _file_base_name
            module = imp.load_module(
                modname, module_file, self.filename, ('.py', 'U', 1))
        return module

    def keys(self):
        return dir(self._module)

    def __getitem__(self, item):
        return getattr(self._module, item)
