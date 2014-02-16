from wlvlang.vmobjects.object import Object

class Array(Object):

    def __init__(self, initial_size):
        self._list = [None] * initial_size

    def get_value_at(self, index):
        return self._list[index]

    def set_value_at(self, index):
        self._list[index] = value

    def get_class(self, universe):
        return universe.arrayClass

    def __str__(self):
        return str(selt._list)

    def __repr__(self):
        return "vmobject.Array(%r)" % self._list

    def __eq__(self, other):
        return isinstance(other, Array) and self._list is other._list
