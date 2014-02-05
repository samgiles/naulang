class Node:
    def __eq__(self, other):
        return (self.__class__ == other.__class__ and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self == other



class ConstantInteger(Node):

    def __init__(self, value):
        self._value = value

    def __eq__(self, other):
        return isinstance(other, ConstantInteger) and other._value == self._value

class ConstantFloat(Node):

    def __init__(self, value):
        self._value = value

    def __eq__(self, other):
        return isinstance(other, ConstantFloat) and other._value == self._value

class Send(Node):

    def __init__(self, primaryexpression, message, arguments=[]):
        self._primary = primaryexpression
        self._message = message
        self._arguments = arguments

    def __eq__(self, other):
        return isinstance(other, Send) and self._message == other._message and self._primary == other._primary and self._arguments == other._arguments
