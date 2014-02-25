def _concat(invokable, activation_record, interpreter):
    left = activation_record.pop()
    right = activation_record.pop()

    result = interpreter.space.new_string(left.get_as_string() + right.get_as_string())
    activation_record.push(result)

def _print(invokable, activation_record, interpreter):
    top = activation_record.pop()

    print top.get_as_string()

def init_string_prims(space):
    primitives = {
        "print": _print,
        "+": _concat,
    }

    space.stringClass.add_primitives(primitives)
