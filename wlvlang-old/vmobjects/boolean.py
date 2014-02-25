from wlvlang.vmobjects.object import Object

from rpython.rlib import jit

class Boolean(Object):
    """ Represents a Boolean object """

    _immutable_fields_ = ["_value"]

    def __init__(self, value):
        self._value = value

    @jit.elidable
    def get_boolean_value(self):
        return self._value

    @jit.elidable
    def get_as_string(self):
        return str(self)

    def __str__(self):
        return "true" if self._value else "false"

    def __eq__(self, other):
        return isinstance(other, Boolean) and other._value == self._value
