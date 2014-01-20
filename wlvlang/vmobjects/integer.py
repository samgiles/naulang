from wlvlang.vmobjects.object import Object
from rpython.rlib import jit

class Integer(Object):

    # _value is an immutable field as the internal value of an Integer object
    # can never change
    _immutable_fields_ = ["_value"]

    def __init__(self, value):
        self._value = value

    # Does jit.elidable and the immutable field work together,
    # Or do I only require one?
    @jit.elidable
    def get_value(self):
        return self._value

    def __str__(self):
        return str(self.get_value())

    def __repr__(self):
        return "vmobjects.Integer: %s" % self.__str__()

    def get_class(self, universe):
        # Not keen on this coupling
        return universe.integerClass
