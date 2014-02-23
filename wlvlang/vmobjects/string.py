from wlvlang.vmobjects.object import Object

from rpython.rlib import jit

class String(Object):

    _immutable_fields_ = ["_string"]

    def __init__(self, value):
        self._string = value

    @jit.elidable
    def get_string_value(self):
        return self._string

    @jit.elidable
    def get_as_string(self):
        return self._string

    def __str__(self):
        return "\"" + self._string + "\""

    def get_class(self, universe):
        return universe.stringClass
