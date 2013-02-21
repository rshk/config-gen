"""
Config-gen: JSON reader
"""

from config_gen.readers import register

@register('json')
def json_reader(filename):
    """
    Reads a JSON file and returns it directly. It will then be accessible
    as usual from the template.
    """
    import json
    with open(filename, 'r') as f:
        return json.load(f)
