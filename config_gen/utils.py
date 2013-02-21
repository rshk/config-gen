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
        self._cache = {}

    def __getitem__(self, item):
        if item not in self._cache:
            record = self._register[item]
            self._cache[item] = record[0](*record[1], **record[2])
        return self._cache[item]

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


def wrap_text(text, width=70, indent='', dedent=True):
    width -= len(indent)
    text = text.strip("\n")
    import textwrap
    if dedent:
        text = textwrap.dedent(text)
    lines = []
    for line in text.split("\n\n"):
        for line1 in textwrap.wrap(line, width):
            lines.append(line1.rstrip())
        lines.append("")  # Leave a blank line at the end
    lines.pop(-1)
    return "\n".join([indent + line for line in lines]) + "\n"
