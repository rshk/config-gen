"""
:author: samu
:created: 2/20/13 11:43 PM
"""

from __future__ import absolute_import

import unittest
import os

from tests.utils import TestWithTmpdirMixin, run


class TestQuickstartAndRender(TestWithTmpdirMixin, unittest.TestCase):
    def assertIsFile(self, arg):
        arg = self._rp(arg)
        self.assertTrue(os.path.isfile(arg))

    def assertIsDir(self, arg):
        arg = self._rp(arg)
        self.assertTrue(os.path.isdir(arg))

    def _rp(self, *args):
        return os.path.join(self.tmpdir, *args)

    def test_quickstart_and_render(self):
        """Run quickstart and render"""

        os.chdir(self.tmpdir)

        run(('confgen-quickstart',))

        self.assertIsDir('templates')
        self.assertIsFile('templates/example.html.jinja')
        self.assertIsDir('data')
        self.assertIsFile('data/example.json')
        self.assertIsDir('build')
        self.assertIsFile('Makefile')

        run(('make',))

        self.assertIsFile('build/example.html')

        with open(self._rp('build/example.html'), 'r') as f:
            rendered_content = f.read()

        self.assertEqual(rendered_content.strip(), '<h1>Hello, world!</h1>')
