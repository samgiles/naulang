from wlvlang.vmobjects.boolean import Boolean

def _eq(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_boolean_value() == right.get_boolean_value()
    activation_record.push(Boolean(result))

def _or(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_boolean_value() or right.get_boolean_value()
    activation_record.push(Boolean(result))

def _and(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_boolean_value() and right.get_boolean_value()
    activation_record.push(Boolean(result))

def _print(activation_record, interpreter):
    pass

def init_boolean_prims(universe):
    primitives = {
        "==": _eq,
        "or": _or,
        "and": _and,
        "print": _print
    }
