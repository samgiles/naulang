from naulang.interpreter.objectspace.object import Object
from naulang.interpreter.error import NauRuntimeError


class Array(Object):

    _immutable_fields_ = ["_list", "size"]

    def __init__(self, initial_size):
        self.size = initial_size
        self._list = [None] * int(initial_size)

    def get_value_at(self, index):
        if index >= 0 and index < self.size:
            return self._list[int(index)]
        raise NauRuntimeError("Index %d not in bounds of array" % index)

    def set_value_at(self, index, value):
        if index >= 0 and index < self.size:
            self._list[int(index)] = value
            return

        raise NauRuntimeError("Index %d not in bounds of array" % index)

    def __str__(self):
        return str(self._list)

    def __repr__(self):
        return "Array(%r)" % self._list

    def __eq__(self, other):
        return isinstance(other, Array) and self._list == other._list
