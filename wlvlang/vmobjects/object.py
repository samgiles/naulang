class Object(object):
    """ The base object for all types of object that
    are handled or manipulated within the interpreter.

    All operations are invoked by sending a message to
    an object. The concrete implementation of the object
    will dispatch to a specific method implemented by the
    object.
    """

    def __init__(self):
        pass

    def send(self, message_selector, arguments):
        pass
