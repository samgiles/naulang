def _eq(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_boolean_value() == right.get_boolean_value()
    activation_record.push(interpreter.space.new_boolean(result))

def _or(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_boolean_value() or right.get_boolean_value()
    activation_record.push(interpreter.space.new_boolean(result))

def _and(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_boolean_value() and right.get_boolean_value()
    activation_record.push(interpreter.space.new_boolean(result))

def _print(invokable, activation_record, interpreter):
    top = activation_record.pop()
    print top.get_as_string()

def init_boolean_prims(space):
    primitives = {
        "==": _eq,
        "or": _or,
        "and": _and,
        "print": _print
    }

    space.booleanClass.add_primitives(primitives)
