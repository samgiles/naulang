class Node:
    def __eq__(self, other):
        pass

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
