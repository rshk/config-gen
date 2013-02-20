"""
:author: samu
:created: 2/20/13 11:43 PM
"""

from __future__ import absolute_import

import os
import unittest
import json

from tests.utils import TestWithReadyTmpdirMixin, run

csv_data = """\
1,"Number One",First
2,"Number Two",Second
3,"Number Three",Third
4,"Number Four",Fourth
5,"Number Five",Fifth
"""

template_content = """\
<table>
{% for row in mydatabase %}
    <tr>
        <td>{{ row[0] }}</td>
        <td>{{ row[1] }}</td>
        <td>{{ row[2] }}</td>
    </tr>
{% endfor %}
</table>

Again: {% for row in mydatabase %}{{ row[0] }} {% endfor %}.
"""

expected_result = """\
<table>

    <tr>
        <td>1</td>
        <td>Number One</td>
        <td>First</td>
    </tr>

    <tr>
        <td>2</td>
        <td>Number Two</td>
        <td>Second</td>
    </tr>

    <tr>
        <td>3</td>
        <td>Number Three</td>
        <td>Third</td>
    </tr>

    <tr>
        <td>4</td>
        <td>Number Four</td>
        <td>Fourth</td>
    </tr>

    <tr>
        <td>5</td>
        <td>Number Five</td>
        <td>Fifth</td>
    </tr>

</table>

Again: 1 2 3 4 5 .
"""


class TestRenderCSV(TestWithReadyTmpdirMixin, unittest.TestCase):

    def test_render_csv(self):
        """Try to render file containing stuff from a CSV file"""

        with self._open('data/mydatabase.csv', 'w') as f:
            f.write(csv_data)

        with self._open('templates/myfile.jinja', 'w') as f:
            f.write(template_content)

        self.render()

        with self._open('build/myfile') as f:
            rendered = f.read()

        self.assertEqual(rendered, expected_result)
