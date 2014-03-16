from wlvlang.interpreter.objectspace.object import Object

from wlvlang.interpreter.objectspace.primitives.string_primitive import string_prims

class String(Object):

    def __init__(self, value):
        self.string = value

    def get_string_value(self):
        return self.string

    def get_as_string(self):
        return self.string

    def __str__(self):
        return "\"" + self.string + "\""

    def get_class(self, space):
        return space.stringClass

# Initialise primitive methods at bootstrap time
def _setup_prims():
    """ NOT_RPYTHON """
    prims = string_prims()

    for function in prims:
        setattr(String, function.__name__, function)

_setup_prims()
