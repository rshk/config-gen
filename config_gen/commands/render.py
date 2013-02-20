"""
:author: samu
:created: 2/20/13 8:45 PM
"""

import sys
import os
import re

from jinja2 import Environment, FileSystemLoader
from cool_logging import getLogger
from config_gen.utils import LazyRegister

logger = getLogger('config-gen')

from config_gen.exceptions import GenCfgException, UnsupportedConfFile
from config_gen.readers import get_file_reader, get_file_reader_class


def command():

    ## Parse command-line options
    from optparse import OptionParser

    exclude_files = [r'.*~']

    parser = OptionParser()
    parser.add_option(
        "--root",
        dest="root_dir",
        metavar="DIR",
        help="Root directory for a quickstart-generated project (can be used "
             "in place of --data-dir, --templates-dir, --build-dir, ...)")
    parser.add_option(
        "--data-dir",
        dest="data_dir",
        metavar="DIR",
        help="Directory from which to load context/data files")
    parser.add_option(
        "--templates-dir",
        dest="templates_dir",
        metavar="DIR",
        help="Directory from which to load files to be compiled")
    parser.add_option(
        "--extra-templates-dir",
        action="append",
        dest="extra_templates_dirs",
        metavar="DIR",
        help="Directory from which to load files to be compiled")
    parser.add_option(
        "--build-dir",
        dest="build_dir",
        metavar="DIR",
        help="Destination directory for built files")
    parser.add_option(
        "--list-readers",
        dest="action",
        action="store_const",
        const="list-readers",
        help="List available file readers and exits")
    (options, args) = parser.parse_args(sys.argv[1:])

    if options.action == 'list-readers':
        sys.stdout.write("AVAILABLE READERS\n\n")
        from config_gen.readers import get_readers
        for reader_name, reader_class in get_readers().iteritems():
            sys.stdout.write('    ' + reader_name + ' - ')
            sys.stdout.write(reader_class.__doc__ or
                             'No documentation available')
            sys.stdout.write('\n')
        return

    DATA_DIR = options.data_dir
    TEMPLATES_DIR = options.templates_dir
    EXTRA_TEMPLATES_DIRS = options.extra_templates_dirs or []
    BUILD_DIR = options.build_dir

    if options.root_dir:
        if not DATA_DIR:
            DATA_DIR = os.path.join(options.root_dir, 'data')
        if not TEMPLATES_DIR:
            TEMPLATES_DIR = os.path.join(options.root_dir, 'templates')
        if not BUILD_DIR:
            BUILD_DIR = os.path.join(options.root_dir, 'build')
        EXTRA_TEMPLATES_DIRS.append(
            os.path.join(options.root_dir, 'extra_templates'))

    if not DATA_DIR:
        raise ValueError("You must specify a --root or --data-dir")

    if not TEMPLATES_DIR:
        raise ValueError("You must specify a --root or --templates-dir")

    if not BUILD_DIR:
        raise ValueError("You must specify a --root or --build-dir")

    logger.debug("Root dir: {}".format(options.root_dir))
    logger.debug("Data dir: {}".format(options.root_dir))
    logger.debug("Templates dir: {}".format(options.root_dir))
    logger.debug("Build dir: {}".format(options.root_dir))

    ## Build context from configuration files
    template_context = LazyRegister()
    _exclude_re = list([re.compile(x) for x in exclude_files])

    for conf_file in os.listdir(DATA_DIR):
        filename = os.path.join(DATA_DIR, conf_file)
        base_name = os.path.splitext(conf_file)[0]

        ## Check whether this is an excluded file
        if any([xre.match(conf_file) for xre in _exclude_re]):
            continue

        try:
            reader_class = get_file_reader_class(filename)
        except UnsupportedConfFile:
            continue

        if base_name in template_context:
            raise GenCfgException(
                "Multiple files with base name '%s' were found" % base_name)

        logger.debug("Data file: {} (from {})".format(base_name, filename))

        ## Register in the lazy context
        template_context.register(base_name, reader_class, filename)

    ## For each file in templates, render and write to build
    if not os.path.exists(BUILD_DIR):
        os.makedirs(BUILD_DIR)

    template_env = Environment(loader=FileSystemLoader(
        [TEMPLATES_DIR] + EXTRA_TEMPLATES_DIRS,
    ))

    for template_file in os.listdir(TEMPLATES_DIR):
        if any([xre.match(template_file) for xre in _exclude_re]):
            continue
        dstfile = os.path.join(BUILD_DIR, os.path.splitext(template_file)[0])
        logger.info("RENDER {} -> {}".format(template_file, dstfile))
        template = template_env.get_template(template_file)
        rendered = template.render(template_context)
        with open(dstfile, 'w') as f:
            f.write(rendered.encode('utf-8'))


if __name__ == '__main__':
    command()
