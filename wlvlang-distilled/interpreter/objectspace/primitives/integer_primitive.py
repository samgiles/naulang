def _mul(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left = activation_record.pop()
    result = left.get_integer_value() * right.get_integer_value()
    activation_record.push(interpreter.space.new_integer(result))

def _add(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_integer_value() + right.get_integer_value()
    activation_record.push(interpreter.space.new_integer(result))

def _sub(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_integer_value() - right.get_integer_value()
    activation_record.push(interpreter.space.new_integer(result))

def _div(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left = activation_record.pop()

    if (right.get_integer_value() == 0):
        pass
        #TODO: Division by zero, exception

    result = left.get_integer_value() / right.get_integer_value()
    activation_record.push(interpreter.space.new_integer(result))

def _mod(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left  = activation_record.pop()

    result = int(left.get_integer_value()) % int(right.get_integer_value())
    activation_record.push(interpreter.space.new_integer(result))

def _eq(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_integer_value() == right.get_integer_value()

    activation_record.push(interpreter.space.new_boolean(result))

def _neq(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_integer_value() != right.get_integer_value()

    activation_record.push(interpreter.space.new_boolean(result))

def _neg(invokable, activation_record, interpreter):
    top = activation_record.pop()

    result = -top.get_integer_value()
    activation_record.push(interpreter.space.new_integer(result))

def _lt(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_integer_value() < right.get_integer_value()
    activation_record.push(interpreter.space.new_boolean(result))


def _gt(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left  = activation_record.pop()

    result = left.get_integer_value() > right.get_integer_value()

    activation_record.push(interpreter.space.new_boolean(result))

def _gteq(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left  = activation_record.pop()

    result = left.get_integer_value() >= right.get_integer_value()

    activation_record.push(interpreter.space.new_boolean(result))

def _lteq(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left  = activation_record.pop()

    result = left.get_integer_value() <= right.get_integer_value()

    activation_record.push(interpreter.space.new_boolean(result))

def _print(invokable, activation_record, interpreter):
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
