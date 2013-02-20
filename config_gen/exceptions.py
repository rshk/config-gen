"""
config_gen: exceptions
"""


class GenCfgException(Exception):
    pass


class UnsupportedConfFile(GenCfgException):
    pass


class UnsupportedTemplate(GenCfgException):
    pass
