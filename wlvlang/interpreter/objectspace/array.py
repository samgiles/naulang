from wlvlang.interpreter.objectspace.object import Object

class Array(Object):

    _immutable_fields_ = ["_list", "size"]

    def __init__(self, initial_size):
        self.size = initial_size
        self._list = [None] * int(initial_size)

    def get_value_at(self, index):
        assert index >= 0 and index < self.size
        return self._list[int(index)]

    def set_value_at(self, index, value):
        assert index >= 0 and index < self.size
        self._list[int(index)] = value

    def __str__(self):
        return str(self._list)

    def __repr__(self):
        return "Array(%r)" % self._list

    def __eq__(self, other):
        return isinstance(other, Array) and self._list == other._list
