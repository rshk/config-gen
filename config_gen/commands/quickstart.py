"""
:author: samu
:created: 2/20/13 8:46 PM
"""

import os

from cool_logging import getLogger
logger = getLogger('config-gen')


STANDARD_DIRS = [
    'templates',
    'extra_templates',
    'data',
    'build',  # No real need..
]

STANDARD_FILES = {}

STANDARD_FILES['templates/example.html.jinja'] = \
    '<h1>{{ example.hello_msg }}</h1>\n'
STANDARD_FILES['data/example.json'] = \
    '{"hello_msg": "Hello, world!"}\n'


STANDARD_FILES['Makefile'] = """\
## Makefile for config-gen

.PHONY: all clean

all:
\tconfgen-render --root=.

clean:
\trm -f build
"""

STANDARD_FILES['.gitignore'] = """\
## Config-gen ignored files
*~
*.pyc
/build/*
"""


def command():
    root_dir = os.getcwd()

    for dirname in STANDARD_DIRS:
        os.makedirs(os.path.join(root_dir, dirname))

    for file_name, file_content in STANDARD_FILES.iteritems():
        with open(file_name, 'w') as f:
            f.write(file_content)

    print "Done. Now run 'make' to compile an example file."

if __name__ == '__main__':
    command()
