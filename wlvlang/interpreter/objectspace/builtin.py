from wlvlang.interpreter.objectspace.object import Object

class BuiltIn(Object):
    """ Defines a primitive invokable method """

    def __init__(self, identifier, invokable, space):
        self.identifier = identifier
        self.invokable = invokable
        self.space = space

    def invoke(self, task):
        self.invokable(self, task.get_top_frame())

    def get_class(self, space):
        return space.builtinClass
