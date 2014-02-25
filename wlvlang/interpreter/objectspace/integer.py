from wlvlang.interpreter.objectspace.object import Object

class Integer(Object):

    def __init__(self, value):
        self.value = value

    def get_integer_value(self):
        return self.value

    def get_as_string(self):
        return str(self.value)

    def get_class(self, space):
        return space.integerClass

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "int(%s)" % (self.get_as_string())

    def __eq__(self, other):
        return isinstance(other, Integer) and self.value == other.value
