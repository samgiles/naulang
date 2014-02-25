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

    def send(self, activation_record, selector, arguments, vm_universe, interpreter):
        activation_record.push(self)

        invokable = self.get_class(object_space).lookup_invokable(selector)

        if not invokable:
            raise OperationNotFound()

        for arg in arguments:
            activation_record.push(arg)

        invokable(self, activation_record, interpreter)

    def get_as_string(self):
        return "Object"

    def get_class(self, space):
        pass