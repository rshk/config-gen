"""
:author: samu
:created: 6/3/12 7:44 PM
"""

import os, re, sys
from ConfigParser import RawConfigParser, NoSectionError, NoOptionError
from UserDict import DictMixin




PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
CONF_DIR = os.path.join(PROJECT_DIR, 'conf')
TEMPLATES_DIR = os.path.join(PROJECT_DIR, 'templates')
BUILD_DIR = os.path.join(PROJECT_DIR, 'build')
EXCLUDE_FILES = [
    r'.*~',
]


class GenCfgException(Exception): pass
class UnsupportedConfFile(GenCfgException): pass
class UnsupportedTemplate(GenCfgException): pass


## Accessors for configuration files ===========================================

class BaseFileAccessor(object):
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

class IniFileAccessor(BaseFileAccessor, DictMixin):
    def __init__(self, filename):
        super(IniFileAccessor, self).__init__(filename)
        self.parser = RawConfigParser()
        self.parser.read(filename)

    def __getitem__(self, item):
        return IniSectionProxy(self.parser, item)

    def keys(self):
        return self.parser.sections()

class CsvFileAccessor(BaseFileAccessor, DictMixin):
    def __init__(self, filename):
        super(CsvFileAccessor, self).__init__(filename)

    def __iter__(self):
        import csv
        reader = csv.reader(open(self.filename, 'r'), delimiter=",")
        #return reader.__iter__()
        return iter(reader)

class PyFileAccessor(BaseFileAccessor, DictMixin):
    def __init__(self, filename):
        super(PyFileAccessor, self).__init__(filename)
        import imp
        _file_base_name = os.path.splitext(os.path.basename(filename))[0]
        self._module = imp.load_module('cfgfile_%s' % _file_base_name, open(self.filename, 'r'), './mods/mymodule.py', ('.py', 'U', 1))

    def keys(self):
        return dir(self._module)

    def __getitem__(self, item):
        member = getattr(self._module, item)
        if callable(member):
            return member()
        else:
            return member

class JsonFileAccessor(BaseFileAccessor, DictMixin):
    def __init__(self, filename):
        super(JsonFileAccessor, self).__init__(filename)
        try:
            import demjson
            with open(self.filename, 'r') as f:
                self._parsed = demjson.decode(f.read())
        except ImportError:
            import json
            with open(self.filename, 'r') as f:
                self._parsed = json.load(f)


ACCESSORS = {
    'ini': IniFileAccessor,
    'json': JsonFileAccessor,
    'csv': CsvFileAccessor,
    'py': PyFileAccessor,
    'xml': None,
    'yaml': None,
}

def get_file_accessor(filename):
    ext = os.path.splitext(filename)[1][1:]
    return ACCESSORS[ext](filename)


## Renderers for template files ================================================

class BaseRenderer(object):
    def __init__(self, filename):
        self.filename = filename

    def render(self, context):
        raise NotImplementedError("The render() method is not implemented")

class Jinja2Renderer(BaseRenderer):
    def render(self, context):
        from jinja2 import Template
        with open(self.filename, 'r') as f:
            template_text = f.read()
        template = Template(template_text)
        return template.render(context)

RENDERERS = {
    'jinja2': Jinja2Renderer,
}

def get_file_renderer(filename):
    ext = os.path.splitext(filename)[1][1:]
    return RENDERERS[ext](filename)

def render_file(filename, context):
    return get_file_renderer(filename).render(context)


## Main ========================================================================

if __name__ == '__main__':
    ## Build context from configuration files
    CONTEXT = {}
    _exclude_re = list([re.compile(x) for x in EXCLUDE_FILES])
    for cfgfile in os.listdir(CONF_DIR):
        filename = os.path.join(CONF_DIR, cfgfile)
        _cff_basename = os.path.basename(filename)
        if any([xre.match(_cff_basename) for xre in _exclude_re]):
            continue
        try:
            accessor = get_file_accessor(filename)
        except UnsupportedConfFile:
            continue
        _cff_name = os.path.splitext(_cff_basename)[0]
        if CONTEXT.has_key(_cff_name):
            raise GenCfgException("Multiple files with base name '%s' were found" % _cff_name)
        CONTEXT[_cff_name] = accessor

    ## For each file in templates, render and write to build
    if not os.path.exists(BUILD_DIR):
        os.makedirs(BUILD_DIR)
    for template_file in os.listdir(TEMPLATES_DIR):
        print "RENDER %s" % template_file
        srcfile = os.path.join(TEMPLATES_DIR, template_file)
        dstfile = os.path.join(BUILD_DIR, os.path.splitext(template_file)[0])
        with open(dstfile, 'w') as f:
            f.write(render_file(srcfile, CONTEXT))
