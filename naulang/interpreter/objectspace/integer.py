from naulang.interpreter.objectspace.primitive_object import PrimitiveObject
from naulang.interpreter.error import NauRuntimeError


class Integer(PrimitiveObject):

    _immutable_fields_ = ["value"]

    def __init__(self, value):
        self.value = value

    def get_integer_value(self):
        return self.value

    def get_as_string(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "int(%s)" % (self.get_as_string())

    def __eq__(self, other):
        return isinstance(other, Integer) and self.value == other.value

    def _should_do_operation_as_float(self, activation_record):
        from naulang.interpreter.objectspace.float import Float
        left = activation_record.pop()
        right = activation_record.pop()
        as_float = False

        if isinstance(left, Float) or isinstance(right, Float):
            as_float = True

        activation_record.push(right)
        activation_record.push(left)

        return as_float

    def w_mul(self, activation_record, space):
        as_float = self._should_do_operation_as_float(activation_record)
        left_value = activation_record.pop()
        right_value = activation_record.pop()

        if as_float:
            result = float(left_value.get_integer_value()) * right_value.get_float_value()
            activation_record.push(space.new_float(result))
        else:
            result = left_value.get_integer_value() * right_value.get_integer_value()
            activation_record.push(space.new_integer(result))

    def w_add(self, activation_record, space):
        as_float = self._should_do_operation_as_float(activation_record)
        left_value = activation_record.pop()
        right_value = activation_record.pop()

        if as_float:
            result = float(left_value.get_integer_value()) + right_value.get_float_value()
            activation_record.push(space.new_float(result))
        else:
            result = left_value.get_integer_value() + right_value.get_integer_value()
            activation_record.push(space.new_integer(result))

    def w_sub(self, activation_record, space):
        as_float = self._should_do_operation_as_float(activation_record)
        left_value = activation_record.pop()
        right_value = activation_record.pop()

        if as_float:
            result = float(left_value.get_integer_value()) - right_value.get_float_value()
            activation_record.push(space.new_float(result))
        else:
            result = left_value.get_integer_value() - right_value.get_integer_value()
            activation_record.push(space.new_integer(result))

    def w_div(self, activation_record, space):
        as_float = self._should_do_operation_as_float(activation_record)
        left_value = activation_record.pop()
        right_value = activation_record.pop()

        if as_float:
            if (right_value.get_float_value() == 0):
                raise NauRuntimeError("Division By Zero")

            result = float(left_value.get_integer_value()) / right_value.get_float_value()
            activation_record.push(space.new_float(result))
        else:
            if (right_value.get_integer_value() == 0):
                raise NauRuntimeError("Division By Zero")
            result = left_value.get_integer_value() / right_value.get_integer_value()
            activation_record.push(space.new_integer(result))

    def w_mod(self, activation_record, space):
        as_float = self._should_do_operation_as_float(activation_record)
        left_value = activation_record.pop()
        right_value = activation_record.pop()

        # any float is truncated to int, mod'd and then re-floated
        if as_float:
            result = int(left_value.get_integer_value()) % int(right_value.get_float_value())
            activation_record.push(space.new_float(result))
        else:
            result = left_value.get_integer_value() % right_value.get_integer_value()
            activation_record.push(space.new_integer(result))

    def w_eq(self, activation_record, space):
        as_float = self._should_do_operation_as_float(activation_record)
        left_value = activation_record.pop()
        right_value = activation_record.pop()

        if as_float:
            result = float(left_value.get_integer_value()) == right_value.get_float_value()
        else:
            result = left_value.get_integer_value() == right_value.get_integer_value()

        activation_record.push(space.new_boolean(result))

    def w_neq(self, activation_record, space):
        as_float = self._should_do_operation_as_float(activation_record)
        left_value = activation_record.pop()
        right_value = activation_record.pop()

        if as_float:
            result = float(left_value.get_integer_value()) != right_value.get_float_value()
        else:
            result = left_value.get_integer_value() != right_value.get_integer_value()

        activation_record.push(space.new_boolean(result))

    def w_neg(self, activation_record, space):
        top = activation_record.pop()
        result = -top.get_integer_value()
        activation_record.push(space.new_integer(result))

    def w_lt(self, activation_record, space):
        as_float = self._should_do_operation_as_float(activation_record)
        right_value = activation_record.pop()
        left_value = activation_record.pop()

        if as_float:
            result = float(left_value.get_integer_value()) < right_value.get_float_value()
            activation_record.push(space.new_boolean(result))
        else:
            result = left_value.get_integer_value() < right_value.get_integer_value()
            activation_record.push(space.new_boolean(result))

    def w_gt(self, activation_record, space):
        as_float = self._should_do_operation_as_float(activation_record)
        right_value = activation_record.pop()
        left_value = activation_record.pop()

        if as_float:
            result = float(left_value.get_integer_value()) > right_value.get_float_value()
            activation_record.push(space.new_boolean(result))
        else:
            result = left_value.get_integer_value() > right_value.get_integer_value()
            activation_record.push(space.new_boolean(result))

    def w_gteq(self, activation_record, space):
        as_float = self._should_do_operation_as_float(activation_record)
        right_value = activation_record.pop()
        left_value = activation_record.pop()

        if as_float:
            result = float(left_value.get_integer_value()) >= right_value.get_float_value()
            activation_record.push(space.new_boolean(result))
        else:
            result = left_value.get_integer_value() >= right_value.get_integer_value()
            activation_record.push(space.new_boolean(result))

    def w_lteq(self, activation_record, space):
        as_float = self._should_do_operation_as_float(activation_record)
        right_value = activation_record.pop()
        left_value = activation_record.pop()

        if as_float:
            result = float(left_value.get_integer_value()) <= right_value.get_float_value()
            activation_record.push(space.new_boolean(result))
        else:
            result = left_value.get_integer_value() <= right_value.get_integer_value()
            activation_record.push(space.new_boolean(result))

    def w_print(self, activation_record, space):
        top = activation_record.pop()
        print top.get_as_string()
