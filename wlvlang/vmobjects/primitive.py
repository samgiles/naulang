from wlvlang.vmobjects.object import Object

class Primitive(Object):
    """ Defines a primitive invokable method """

    def __init__(self, identifier, universe, invoke):
        self.identifier = identifier
        self._invoke = invoke

    def invoke(self, activation_record, interpreter):
        self._invoke(self, activation_record, interpreter)

    def get_class(self, universe):
        return universe.primitiveClass
