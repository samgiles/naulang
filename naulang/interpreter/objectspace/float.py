from naulang.interpreter.objectspace.primitive_object import PrimitiveObject
from naulang.interpreter.error import NauRuntimeError

from rpython.rlib.rfloat import double_to_string


class Float(PrimitiveObject):

    _immutable_fields_ = ["value"]

    def __init__(self, value):
        self.value = value

    def get_float_value(self):
        return self.value

    def get_as_string(self):
        string, _ = double_to_string(self.value, 'G', 12, flags=0)
        return string

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "float(%s)" % (self.get_as_string())

    def __eq__(self, other):
        return isinstance(other, Float) and self.value == other.value

    def _get_left_and_right(self, activation_record):
        from naulang.interpreter.objectspace.integer import Integer
        from naulang.interpreter.objectspace.float import Float
        left = activation_record.pop()
        right = activation_record.pop()

        if isinstance(left, Integer):
            left_value = left.get_integer_value()
        elif isinstance(left, Float):
            left_value = left.get_float_value()
        else:
            raise Exception("TypeError")

        if isinstance(right, Integer):
            right_value = right.get_integer_value()
        elif isinstance(right, Float):
            right_value = right.get_float_value()
        else:
            raise Exception("TypeError")

        return float(left_value), float(right_value)

    def w_mul(self, activation_record, space):
        left_value, right_value = self._get_left_and_right(activation_record)
        result = left_value * right_value
        activation_record.push(space.new_float(result))

    def w_add(self, activation_record, space):
        left_value, right_value = self._get_left_and_right(activation_record)
        result = left_value + right_value
        activation_record.push(space.new_float(result))

    def w_sub(self, activation_record, space):
        left_value, right_value = self._get_left_and_right(activation_record)
        result = left_value - right_value
        activation_record.push(space.new_float(result))

    def w_div(self, activation_record, space):
        left_value, right_value = self._get_left_and_right(activation_record)

        if (right_value == 0):
            raise NauRuntimeError("Division By Zero")

        result = left_value / right_value
        activation_record.push(space.new_float(result))

    def w_mod(self, activation_record, space):
        left_value, right_value = self._get_left_and_right(activation_record)

        # floats are truncated to ints, mod'd and then floated
        result = int(left_value) % int(right_value)
        activation_record.push(space.new_float(result))

    def w_eq(self, activation_record, space):
        left_value, right_value = self._get_left_and_right(activation_record)
        result = left_value == right_value
        activation_record.push(space.new_boolean(result))

    def w_neq(self, activation_record, space):
        left_value, right_value = self._get_left_and_right(activation_record)
        result = left_value != right_value
        activation_record.push(space.new_boolean(result))

    def w_neg(self, activation_record, space):
        from naulang.interpreter.objectspace.float import Float
        top = activation_record.pop()

        if isinstance(top, Float):
            result = -top.get_float_value()
            activation_record.push(space.new_float(result))
        else:
            raise TypeError("Float.w_neg was invoked, yet the target was not a Float type")

    def w_lt(self, activation_record, space):
        right_value, left_value = self._get_left_and_right(activation_record)
        result = left_value < right_value
        activation_record.push(space.new_boolean(result))

    def w_gt(self, activation_record, space):
        right_value, left_value = self._get_left_and_right(activation_record)
        result = left_value > right_value
        activation_record.push(space.new_boolean(result))

    def w_gteq(self, activation_record, space):
        right_value, left_value = self._get_left_and_right(activation_record)
        result = left_value >= right_value
        activation_record.push(space.new_boolean(result))

    def w_lteq(self, activation_record, space):
        right_value, left_value = self._get_left_and_right(activation_record)
        result = left_value <= right_value
        activation_record.push(space.new_boolean(result))

    def w_print(self, activation_record, space):
        top = activation_record.pop()
        print top.get_as_string()
