def _eq(activation_record, space):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_boolean_value() == right.get_boolean_value()
    activation_record.push(space.new_boolean(result))

def _or(activation_record, space):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_boolean_value() or right.get_boolean_value()
    activation_record.push(space.new_boolean(result))

def _and(activation_record, space):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_boolean_value() and right.get_boolean_value()
    activation_record.push(space.new_boolean(result))

def _print(activation_record, space):
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
