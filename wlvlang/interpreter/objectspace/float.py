from wlvlang.interpreter.objectspace.primitive_object import PrimitiveObject
from wlvlang.interpreter.objectspace.number import Number

from rpython.rlib.rfloat import double_to_string

class Float(Number, PrimitiveObject):

    _immutable_ = True
    _immutable_fields = ["value"]

    def __init__(self, value):
        self.value = value

    def get_float_value(self):
        return self.value

    def get_as_string(self):
        string, _ = double_to_string(self.value, 'G', 12, flags=0)
        return string

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "float(%s)" % (self.get_as_string())

    def __eq__(self, other):
        return isinstance(other, Float) and self.value == other.value
