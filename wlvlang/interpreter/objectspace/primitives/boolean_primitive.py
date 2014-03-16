def _eq(invokable, activation_record):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_boolean_value() == right.get_boolean_value()
    activation_record.push(invokable.space.new_boolean(result))

def _or(invokable, activation_record):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_boolean_value() or right.get_boolean_value()
    activation_record.push(invokable.space.new_boolean(result))

def _and(invokable, activation_record):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_boolean_value() and right.get_boolean_value()
    activation_record.push(invokable.space.new_boolean(result))

def _print(invokable, activation_record):
    top = activation_record.pop()
    print top.get_as_string()

def boolean_prims():
    return [
        _eq,
        _or,
        _and,
        _print
    ]
