def _concat(invokable, activation_record):
    left = activation_record.pop()
    right = activation_record.pop()

    result = invokable.space.new_string(left.get_as_string() + right.get_as_string())
    activation_record.push(result)

def _print(invokable, activation_record):
    top = activation_record.pop()

    print top.get_as_string()

def string_prims():
   return [
        _print,
        _concat,
    ]
