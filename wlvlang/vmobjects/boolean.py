from wlvlang.vmobjects.object import Object

class Boolean(Object):
    """ Represents a Boolean object """

    _immutable_fields_ = ["_value"]

    def __init__(self, value):
        self._value = value

    def get_value(self):
        return self._value

    def __str__(self):
        return "true" if self._value else "false"
