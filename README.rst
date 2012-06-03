################################
Configuration generator
################################

This project was born to generate dhcp/dns configuration files on a machine
which resources are too limited to run an LDAP server.

What it basically does is:

* Load a bunch of files from a directory, and make them accessible in
  a dictionary.
* Render a bunch of files through some template engine, passing the context.


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
