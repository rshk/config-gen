################################
Configuration generator
################################

This project was born to generate dhcp/dns configuration files on a machine
which resources are too limited to run an LDAP server.

What it basically does is:

* Load a bunch of files from a directory, and make them accessible in
  a dictionary.
* Render a bunch of files through some template engine, passing the context.


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


Supported configuration files
=============================

Configuration files are the ones used to build the context.
Their name (without extension) must be unique all around the ``conf`` directory.

* ``ini`` - Parsed through a ``ConfigParser.RawConfigParser`` as
  ``{{ file.section.option }}``
* ``csv`` - Parsed using the ``csv`` module, as an iterable of lists.
* ``json`` - Parsed using ``demjson`` or, as fallback, the ``json`` module
  from standard library.
* ``py`` - Python modules are supported too. The content of the module is
  extracted; if a member is a function, its return value is used.


Supported template engines
==========================

Only ``jinja2`` is supported at the moment (``.jinja2`` files).

Download it from http://jinja.pocoo.org/ or via ``pip install jinja2``.


TODO
====

* Add support for XML/YAML files
* Write some ``unittest`` test cases
