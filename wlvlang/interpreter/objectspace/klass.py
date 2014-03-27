from wlvlang.interpreter.objectspace.object import Object

def _not_implemented(cls, frame, space):
    raise NotImplementedError()

class Class(Object):

    _immutable_fields_ = ["invokeabletable"]

    def __init__(self):
        self.invokabletable = {}


    def get_class(self, space):
        return self
