"""
:author: samu
:created: 2/20/13 8:28 PM
"""


class GenericRegister(dict):
    def register(self, name):
        def decorator(function):
            self[name] = function
            return function
        return decorator

    def __call__(self, name):
        return self.register(name)
