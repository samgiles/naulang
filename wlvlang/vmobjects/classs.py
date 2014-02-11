from wlvlang.vmobjects.object import Object
from wlvlang.vm import exceptions
class Class(Object):

    def __init__(self, universe, parent=None):
        self._invokabletable = {}
        self._universe = universe
        self._parent = parent

    def lookup_invokable(self, signature):
        invokable = self._invokabletable.get(signature, None)

        if invokable:
            return invokable

        if self._parent is None:
            raise exceptions.MethodNotFoundException(signature, self)

        return self._parent.lookup_invokable(signature)

    def add_primitives(self, primitives):
        """ Primitives should be a dictionary
        keyed by signature """
        self._invokabletable.update(primitives)

    def add_method(self, method):
        """ Adds a new Method to this class
        definition """
        self._invokabletable.set(method.signature, method)

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_class(self, universe):
        return self
