from wlvlang.interpreter.objectspace.primitive_object import PrimitiveObject

class Integer(PrimitiveObject):

    _immutable_ = True
    _immutable_fields = ["value"]

    def __init__(self, value):
        self.value = value

    def get_integer_value(self):
        return self.value

    def get_as_string(self):
        return str(self.value)

    def get_class(self, space):
        return space.integerClass

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "int(%s)" % (self.get_as_string())

    def __eq__(self, other):
        return isinstance(other, Integer) and self.value == other.value

    def w_mul(self, activation_record, space):
        left = activation_record.pop()
        right = activation_record.pop()
        result = left.get_integer_value() * right.get_integer_value()
        activation_record.push(space.new_integer(result))

    def w_add(self, activation_record, space):
        left = activation_record.pop()
        right = activation_record.pop()

        result = left.get_integer_value() + right.get_integer_value()
        activation_record.push(space.new_integer(result))

    def w_sub(self, activation_record, space):
        left = activation_record.pop()
        right = activation_record.pop()

        result = left.get_integer_value() - right.get_integer_value()
        activation_record.push(space.new_integer(result))

    def w_div(self, activation_record, space):
        left = activation_record.pop()
        right = activation_record.pop()

        if (right.get_integer_value() == 0):
            pass
            #TODO: Division by zero, exception

        result = left.get_integer_value() / right.get_integer_value()
        activation_record.push(space.new_integer(result))

    def w_mod(self, activation_record, space):
        left  = activation_record.pop()
        right = activation_record.pop()

        result = int(left.get_integer_value()) % int(right.get_integer_value())
        activation_record.push(space.new_integer(result))

    def w_eq(self, activation_record, space):
        right = activation_record.pop()
        left = activation_record.pop()

        result = left.get_integer_value() == right.get_integer_value()

        activation_record.push(space.new_boolean(result))

    def w_neq(self, activation_record, space):
        right = activation_record.pop()
        left = activation_record.pop()

        result = left.get_integer_value() != right.get_integer_value()

        activation_record.push(space.new_boolean(result))

    def w_neg(self, activation_record, space):
        top = activation_record.pop()

        result = -top.get_integer_value()
        activation_record.push(space.new_integer(result))

    def w_lt(self, activation_record, space):
        right = activation_record.pop()
        left = activation_record.pop()
        assert left is not None
        assert right is not None

        result = left.get_integer_value() < right.get_integer_value()
        activation_record.push(space.new_boolean(result))


    def w_gt(self, activation_record, space):
        right = activation_record.pop()
        left  = activation_record.pop()

        result = left.get_integer_value() > right.get_integer_value()

        activation_record.push(space.new_boolean(result))

    def w_gteq(self, activation_record, space):
        right = activation_record.pop()
        left  = activation_record.pop()

        result = left.get_integer_value() >= right.get_integer_value()

        activation_record.push(space.new_boolean(result))

    def w_lteq(self, activation_record, space):
        right = activation_record.pop()
        left  = activation_record.pop()

        result = left.get_integer_value() <= right.get_integer_value()

        activation_record.push(space.new_boolean(result))

    def w_print(self, activation_record, space):
        top = activation_record.pop()
        print top.get_as_string()
