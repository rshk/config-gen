"""
:author: samu
:created: 2/20/13 8:31 PM
"""

from ConfigParser import NoOptionError, NoSectionError, RawConfigParser
from UserDict import DictMixin
from config_gen.readers.base import BaseFileAccessor
from config_gen.readers import register


class IniSectionProxy(object, DictMixin):
    def __init__(self, parser, section):
        self.parser = parser
        self.section = section

    def __getitem__(self, item):
        try:
            return self.parser.get(self.section, item)
        except (NoSectionError, NoOptionError):
            return None

    def keys(self):
        try:
            return self.parser.options(self.section)
        except NoSectionError:
            return []


@register('ini')
class IniFileAccessor(BaseFileAccessor):
    def __init__(self, filename):
        super(IniFileAccessor, self).__init__(filename)
        self.parser = RawConfigParser()
        self.parser.read(filename)

    def __getitem__(self, item):
        return IniSectionProxy(self.parser, item)

    def keys(self):
        return self.parser.sections()
