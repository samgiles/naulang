class Object(object):
    """ The base object for all types of object that
    are handled or manipulated within the interpreter.

    All operations are invoked by sending a message to
    an object. The concrete implementation of the object
    will dispatch to a specific method implemented by the
    object.
    """

    def __init__(self):
        self.slots = {}
        self._class = None

    def send(self, activation_record, selector_string, arguments, vm_universe, interpreter):
        selector = vm_universe.symbol_for(selector_string)
        activation_record.push(self)

        for arg in arguments:
            activation_record.push(arg)

        invokable = self.get_class(vm_universe).lookup_invokable(selector)
        invokable.invoke(self, activation_record, interpreter)

    def get_class(self, universe):
        pass
