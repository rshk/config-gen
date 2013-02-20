"""
:author: samu
:created: 2/20/13 8:36 PM
"""

from config_gen.readers import register
from config_gen.readers.base import BaseFileAccessor


@register('json')
class JsonFileAccessor(BaseFileAccessor):
    def __init__(self, filename):
        super(JsonFileAccessor, self).__init__(filename)
        import json
        with open(self.filename, 'r') as f:
            self._parsed = json.load(f)
