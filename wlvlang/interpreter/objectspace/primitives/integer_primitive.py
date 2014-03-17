def _mul(activation_record, space):
    left = activation_record.pop()
    right = activation_record.pop()
    result = left.get_integer_value() * right.get_integer_value()
    activation_record.push(space.new_integer(result))

def _add(activation_record, space):
    left = activation_record.pop()
    right = activation_record.pop()

    result = left.get_integer_value() + right.get_integer_value()
    activation_record.push(space.new_integer(result))

def _sub(activation_record, space):
    left = activation_record.pop()
    right = activation_record.pop()

    result = left.get_integer_value() - right.get_integer_value()
    activation_record.push(space.new_integer(result))

def _div(activation_record, space):
    left = activation_record.pop()
    right = activation_record.pop()

    if (right.get_integer_value() == 0):
        pass
        #TODO: Division by zero, exception

    result = left.get_integer_value() / right.get_integer_value()
    activation_record.push(space.new_integer(result))

def _mod(activation_record, space):
    left  = activation_record.pop()
    right = activation_record.pop()

    result = int(left.get_integer_value()) % int(right.get_integer_value())
    activation_record.push(space.new_integer(result))

def _eq(activation_record, space):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_integer_value() == right.get_integer_value()

    activation_record.push(space.new_boolean(result))

def _neq(activation_record, space):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_integer_value() != right.get_integer_value()

    activation_record.push(space.new_boolean(result))

def _neg(activation_record, space):
    top = activation_record.pop()

    result = -top.get_integer_value()
    activation_record.push(space.new_integer(result))

def _lt(activation_record, space):
    right = activation_record.pop()
    left = activation_record.pop()
    assert left is not None
    assert right is not None

    result = left.get_integer_value() < right.get_integer_value()
    activation_record.push(space.new_boolean(result))


def _gt(activation_record, space):
    right = activation_record.pop()
    left  = activation_record.pop()

    result = left.get_integer_value() > right.get_integer_value()

    activation_record.push(space.new_boolean(result))

def _gteq(activation_record, space):
    right = activation_record.pop()
    left  = activation_record.pop()

    result = left.get_integer_value() >= right.get_integer_value()

    activation_record.push(space.new_boolean(result))

def _lteq(activation_record, space):
    right = activation_record.pop()
    left  = activation_record.pop()

    result = left.get_integer_value() <= right.get_integer_value()

    activation_record.push(space.new_boolean(result))

def _print(activation_record, space):
    top = activation_record.pop()
    print top.get_as_string()

def init_integer_prims(space):
    primitives = {
        "*": _mul,
        "+": _add,
        "-": _sub,
        "/": _div,
        "%": _mod,
        "==": _eq,
        "<": _lt,
        ">": _gt,
        "<=": _lteq,
        ">=": _gteq,
        "!=": _neq,
        "print": _print,
        "_neg": _neg
    }

    space.integerClass.add_primitives(primitives)
