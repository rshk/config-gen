"""
:author: samu
:created: 2/20/13 8:36 PM
"""

from config_gen.readers import register

@register('json')
def json_reader(filename):
    import json
    with open(filename, 'r') as f:
        return json.load(f)
