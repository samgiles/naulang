from wlvlang.interpreter.objectspace.object import Object

class BuiltIn(Object):
    """ Defines a primitive invokable method """

    def __init__(self, identifier, invokable):
        self.identifier = identifier
        self.invokable = invokable

    def invoke(self, frame, interpreter):
        self.invokable(self, frame, interpreter)

    def get_class(self, space):
        return space.builtinClass
