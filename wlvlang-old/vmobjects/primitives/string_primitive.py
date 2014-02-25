from wlvlang.vmobjects.integer import Integer
from wlvlang.vmobjects.boolean import Boolean
from wlvlang.vmobjects.string import String

def _append(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left = activation_record.pop()

    result = String(left.get_as_string() + right.get_as_string())
    activation_record.push(result)

def _print(invokable, activation_record, interpreter):
    top = activation_record.pop()

    print top.get_as_string()

def init_string_prims(universe):
    primitives = {
        "print": _print,
        "+": _append,
    }

    universe.stringClass.add_primitives(primitives)
