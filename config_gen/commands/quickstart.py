"""
:author: samu
:created: 2/20/13 8:46 PM
"""

import os

from cool_logging import getLogger
logger = getLogger('config-gen')


MAKEFILE = """\
## Makefile for config-gen

.PHONY: all clean

all:
\tconfgen-render --root=.

clean:
\trm -f build/*

"""


def command():
    root_dir = os.getcwd()
    relfile = lambda name: os.path.join(root_dir, name)
    os.makedirs(relfile('templates'))
    os.makedirs(relfile('data'))
    os.makedirs(relfile('build'))
    os.makedirs(relfile('extra_templates'))
    with open(relfile('Makefile'), 'w') as f:
        f.write(MAKEFILE)
    with open(relfile('templates/example.html.jinja'), 'w') as f:
        f.write('<h1>{{ example.hello_msg }}</h1>\n')
    with open(relfile('data/example.json'), 'w') as f:
        f.write('{"hello_msg": "Hello, world!"}\n')
    print "Done. Now run 'make' to compile an example file."

if __name__ == '__main__':
    command()
