from wlvlang.interpreter.objectspace.object import Object

from rpython.rlib import jit

class Class(Object):

    _immutable_fields_ = ["invokeabletable"]

    def __init__(self):
        self.invokabletable = {}

    @jit.elidable
    def lookup_invokable(self, signature):
        invokable = self.invokabletable.get(signature, None)

        if invokable:
            return invokable

        raise NotImplementedError()

    def add_primitives(self, primitives):
        """ Primitives should be a dictionary
        keyed by signature """
        self.invokabletable.update(primitives)

    def add_method(self, method):
        """ Adds a new Method to this class
        definition """
        self.invokabletable.set(method.signature, method)

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_class(self, space):
        return self
