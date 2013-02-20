"""
:author: samu
:created: 2/20/13 8:31 PM
"""

from UserDict import DictMixin


class BaseFileAccessor(object, DictMixin):
    def __init__(self, filename):
        self.filename = filename

    def __getitem__(self, item):
        pass

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    def keys(self):
        pass
