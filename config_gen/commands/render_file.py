"""
Config-gen: render a single file, taking context from arguments
"""

import sys

from jinja2 import Template

from config_gen.utils import LazyRegister
from config_gen.readers import get_readers


def command():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option(
        '--context', action='append', dest='context',
        help="Add a context line, in the form: <name>:<type>:<path>")
    options, args = parser.parse_args(sys.argv[1:])

    if len(args) < 1:
        raise ValueError("Usage: command [options] <filename>")

    ## Prepare build context
    template_context = LazyRegister()
    for context_line in options.context:
        c_name, c_type, c_path = context_line.split(':', 2)
        reader_class = get_readers()[c_type]
        if c_name in template_context:
            raise ValueError("Context file {0} is already defined!"
                             "".format(c_name))
        template_context.register(c_name, reader_class, c_path)

    ## Compile templates
    for template_file in args:
        file_data = open(template_file, 'r').read().decode('utf-8')
        template = Template(file_data)
        rendered = template.render(template_context)
        print(rendered.encode('utf-8'))
