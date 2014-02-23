from wlvlang.vmobjects.object import Object

class String(Object):

    _immutable_fields_ = ["_string"]

    def __init__(self, value):
        self._string = value

    def get_value(self):
        return self._string

    def __str__(self):
        return "\"" + self._string + "\""

    def get_class(self, universe):
        return universe.stringClass
