"""
:author: samu
:created: 2/20/13 8:28 PM
"""
from UserDict import DictMixin


class GenericRegister(dict):
    def register(self, name):
        def decorator(function):
            self[name] = function
            return function
        return decorator

    def __call__(self, name):
        return self.register(name)


class LazyRegister(object, DictMixin):
    def __init__(self):
        self._register = {}

    def __getitem__(self, item):
        record = self._register[item]
        return record[0](*record[1], **record[2])

    def keys(self):
        return self._register.keys()

    def register(self, name, obj, *args, **kwargs):
        self._register[name] = (obj, args, kwargs)


def lazy_property(fn):
    attr_name = '_lazy_' + fn.__name__

    def decorated(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return property(decorated)
