from naulang.interpreter.error import NauRuntimeError


class Number(object):
    _mixin_ = True

    def _get_left_and_right(self, activation_record):
        from naulang.interpreter.objectspace.integer import Integer
        from naulang.interpreter.objectspace.float import Float
        left = activation_record.pop()
        right = activation_record.pop()
        as_float = False

        if isinstance(left, Integer):
            left_value = left.get_integer_value()
        elif isinstance(left, Float):
            as_float = True
            left_value = left.get_float_value()
        else:
            raise Exception("TypeError")

        if isinstance(right, Integer):
            right_value = right.get_integer_value()
        elif isinstance(right, Float):
            as_float = True
            right_value = right.get_float_value()
        else:
            raise Exception("TypeError")

        return left_value, right_value, as_float

    def w_mul(self, activation_record, space):
        left_value, right_value, as_float = self._get_left_and_right(activation_record)
        result = left_value * right_value
        if as_float:
            activation_record.push(space.new_float(result))
        else:
            activation_record.push(space.new_integer(result))

    def w_add(self, activation_record, space):
        left_value, right_value, as_float = self._get_left_and_right(activation_record)
        result = left_value + right_value
        if as_float:
            activation_record.push(space.new_float(result))
        else:
            activation_record.push(space.new_integer(result))

    def w_sub(self, activation_record, space):
        left_value, right_value, as_float = self._get_left_and_right(activation_record)
        result = left_value - right_value
        if as_float:
            activation_record.push(space.new_float(result))
        else:
            activation_record.push(space.new_integer(result))

    def w_div(self, activation_record, space):
        left_value, right_value, as_float = self._get_left_and_right(activation_record)

        if (right_value == 0):
            raise NauRuntimeError("Division By Zero")

        result = left_value / right_value
        if as_float:
            activation_record.push(space.new_float(result))
        else:
            activation_record.push(space.new_integer(result))

    def w_mod(self, activation_record, space):
        left_value, right_value, as_float = self._get_left_and_right(activation_record)

        # floats are truncated to ints, mod'd and then floated
        result = int(left_value) % int(right_value)
        if as_float:
            activation_record.push(space.new_float(result))
        else:
            activation_record.push(space.new_integer(result))

    def w_eq(self, activation_record, space):
        left_value, right_value, as_float = self._get_left_and_right(activation_record)
        result = left_value == right_value
        activation_record.push(space.new_boolean(result))

    def w_neq(self, activation_record, space):
        left_value, right_value, as_float = self._get_left_and_right(activation_record)
        result = left_value != right_value
        activation_record.push(space.new_boolean(result))

    def w_neg(self, activation_record, space):
        from naulang.interpreter.objectspace.integer import Integer
        from naulang.interpreter.objectspace.float import Float
        top = activation_record.pop()

        if isinstance(top, Float):
            result = -top.get_float_value()
            activation_record.push(space.new_float(result))
        else:
            result = -top.get_integer_value()
            activation_record.push(space.new_integer(result))

    def w_lt(self, activation_record, space):
        right_value, left_value, as_float = self._get_left_and_right(activation_record)
        result = left_value < right_value
        activation_record.push(space.new_boolean(result))

    def w_gt(self, activation_record, space):
        right_value, left_value, as_float = self._get_left_and_right(activation_record)
        result = left_value > right_value
        activation_record.push(space.new_boolean(result))

    def w_gteq(self, activation_record, space):
        right_value, left_value, as_float = self._get_left_and_right(activation_record)
        result = left_value >= right_value
        activation_record.push(space.new_boolean(result))

    def w_lteq(self, activation_record, space):
        right_value, left_value, as_float = self._get_left_and_right(activation_record)
        result = left_value <= right_value
        activation_record.push(space.new_boolean(result))

    def w_print(self, activation_record, space):
        top = activation_record.pop()
        print top.get_as_string()
