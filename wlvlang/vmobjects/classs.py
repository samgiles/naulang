from wlvlang.vmobjects.object import Object
class Class(Object):

    def __init__(self, universe):
        self._invokabletable = {}
        self._universe = universe

    def lookup_invokable(self, signature):
        invokable = self._invokabletable.get(signature, None)

        if invokable:
            return invokable

        # TODO: Super class chain
        return None

    def add_primitives(self, primitives):
        """ Primitives should be a dictionary
        keyed by signature """
        self._invokabletable.update(primitives)

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_class(self, universe):
        universe.objectClass
