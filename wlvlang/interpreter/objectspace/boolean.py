from wlvlang.interpreter.objectspace.primitive_object import PrimitiveObject

class Boolean(PrimitiveObject):
    """ Represents a Boolean object """

    _immutable_fields_ = ["value"]

    def __init__(self, value):
        self.value = value

    def get_boolean_value(self):
        return self.value

    def get_as_string(self):
        return str(self)

    def __str__(self):
        return "true" if self.value else "false"

    def __eq__(self, other):
        return isinstance(other, Boolean) and other.value == self.value

    def w_eq(self, activation_record, space):
        right = activation_record.pop()
        left = activation_record.pop()

        result = left.get_boolean_value() == right.get_boolean_value()
        activation_record.push(space.new_boolean(result))

    def w_or(self, activation_record, space):
        right = activation_record.pop()
        left = activation_record.pop()

        result = left.get_boolean_value() or right.get_boolean_value()
        activation_record.push(space.new_boolean(result))

    def w_and(self, activation_record, space):
        right = activation_record.pop()
        left = activation_record.pop()

        result = left.get_boolean_value() and right.get_boolean_value()
        activation_record.push(space.new_boolean(result))

    def w_print(self, activation_record, space):
        top = activation_record.pop()
        print top.get_as_string()
