################################
Configuration generator
################################


This project was born to generate dhcp/dns configuration files on a machine
which resources are too limited to run a LDAP server.

What it basically does is:

* Load a bunch of files from a directory, and make them accessible in
  a dictionary.
* Render a bunch of files through some template engine, passing the context.


.. image:: https://travis-ci.org/rshk/config-gen.png
    :alt: Build status
    :target: https://travis-ci.org/rshk/config-gen



Installation
============

Production version::

    $ pip install config-gen

Development version::

    $ pip install -e git+git@github.com:rshk/config-gen.git#egg=config-gen

Or just run ``python setup.py install`` from the source directory.


Trying out
==========

The fastest way to get started with config-gen is the quickstart script,
that takes care of creating all the needed directories plus a Makefile,
in the current directory::

    $ confgen-quickstart
    $ make
    $ cat build/example.html
    <h1>Hello, world!</h1>


How does it work?
=================

In a very simple way: all files in the ``templates`` directory are built
into files in ``build``, with the original extension stripped. Eg::

    templates/hello.jinja -> build/hello
    templates/hello.html.jinja -> build/hello.html
    templates/example.html.jinja -> build/example.html

The context for rendered files is built from files in the ``data`` directory.
To each file in that directory, a "reader" is associated, by reading the
file extension.

Then, a context variable with the same name of the file (without extension)
will be made available in the template.


Included readers
================

Readers are used to read data files and make them accessible
in the template context.

Their name (without extension) must be unique all around the ``data``
directory, to prevent conflicts.

**txt** (``config_gen.readers.read_txt.txt_reader``)
    Loads a plain text file, returning its raw content directly.


**py** (``config_gen.readers.read_py.PyFileAccessor``)
    Loads and returns a Python module.

    The module content will then be fully accessible from the template.


**json** (``config_gen.readers.read_json.json_reader``)
    Reads a JSON file and returns it directly. It will then be accessible as
    usual from the template.


**csv** (``config_gen.readers.read_csv.csv_reader``)
    Reads a Comma-Separated Values file into a list of tuples.

    The CSV file must be comma-separated (semicolons are not supported). Fields
    containing commas must be enclosed in double quotes.


**ini** (``config_gen.readers.read_ini.IniFileReader``)
    Reader for configuration/.ini files.

    Files will be accessible as::

        {{ filename.section.option }}

    Or, for sections/options containing dots::

        {{ filename["my.sect.ion"]["my.opt.ion"] }}


Template engines
================

To render the templates into configuration files, the awesome Jinja2_
template engine has been used.

I once thought about allowing pluggable template engines, but the
awesomeness of Jinja made me rethink that decision :)

(By the way, just let me know if you'd absolutely need support for
another template engine, and why..)

.. _Jinja2: http://jinja.pocoo.org/


Testing
=======

To run the complete test suite::

    $ python -m unittest discover -s tests

To run only tests in a specific sub-module::

    $ python -m unittest tests.test_something


TODO-List
=========

* Add support for XML/YAML files
* Add support for database connections (sqlite, mysql, postgres, mongo..)
* Add support for "custom cases", through some kind of configuration file
  * Eg. for semicolon-separated CSV files
* Add support for importing external readers (add a ``--load`` option?)
* Write the missing test cases
