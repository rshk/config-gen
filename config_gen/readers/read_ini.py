"""
Config-gen: INI reader
"""

from ConfigParser import NoOptionError, NoSectionError, RawConfigParser
from UserDict import DictMixin
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
class IniFileReader(object, DictMixin):
    """
    Reader for configuration/.ini files.

    Files will be accessible as::

        {{ filename.section.option }}

    Or, for sections/options containing dots::

        {{ filename["my.sect.ion"]["my.opt.ion"] }}
    """
    def __init__(self, filename):
        self.filename = filename
        self.parser = RawConfigParser()
        self.parser.read(filename)

    def __getitem__(self, item):
        return IniSectionProxy(self.parser, item)

    def keys(self):
        return self.parser.sections()
