from wlvlang.interpreter.objectspace.object import Object

class String(Object):

    def __init__(self, value):
        self.string = value

    def get_string_value(self):
        return self.string

    def get_as_string(self):
        return self.string

    def __str__(self):
        return "\"" + self.string + "\""

    def get_class(self, space):
        return space.stringClass
