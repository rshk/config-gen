"""
:author: samu
:created: 2/20/13 11:43 PM
"""

from __future__ import absolute_import

import unittest
import json

from tests.utils import TestWithReadyTmpdirMixin

json_data = {
    'key1': 'val1',
    'key2': 'val2',
    'key3': 12345,
    'key4': ['AAA', 'BBB', 'CCC'],
    'key5': {
        'a': 'A',
        'b': 'B',
        'c': 'C',
    },
}

template_content = """\
Key1: {{ mydatabase.key1 }}
Key2: {{ mydatabase.key2 }}
Key3: {{ mydatabase.key3 }}
Key4: {{ mydatabase.key4 }}
Key5.a: {{ mydatabase.key5.a }}
Key5.b: {{ mydatabase.key5.b }}
Key5.c: {{ mydatabase.key5.c }}

{% for item in mydatabase.key4 -%}
* {{ item }}
{% endfor %}
"""

expected_result = """\
Key1: val1
Key2: val2
Key3: 12345
Key4: [u'AAA', u'BBB', u'CCC']
Key5.a: A
Key5.b: B
Key5.c: C

* AAA
* BBB
* CCC
"""


class TestRenderJson(TestWithReadyTmpdirMixin, unittest.TestCase):

    def test_render_json(self):
        """Try to render file containing stuff from a JSON file"""

        with self._open('data/mydatabase.json', 'w') as f:
            json.dump(json_data, f)

        with self._open('templates/myfile.jinja', 'w') as f:
            f.write(template_content)

        self.render()

        with self._open('build/myfile') as f:
            rendered = f.read()

        self.assertEqual(rendered, expected_result)
