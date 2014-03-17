def _concat(activation_record, space):
    left = activation_record.pop()
    right = activation_record.pop()

    result = space.new_string(left.get_as_string() + right.get_as_string())
    activation_record.push(result)

def _print(activation_record, space):
    top = activation_record.pop()

    print top.get_as_string()

def init_string_prims(space):
    primitives = {
        "print": _print,
        "+": _concat,
    }

    space.stringClass.add_primitives(primitives)
