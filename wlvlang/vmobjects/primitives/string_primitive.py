from wlvlang.vmobjects.integer import Integer
from wlvlang.vmobjects.boolean import Boolean
from wlvlang.vmobjects.string import String

def _append(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left = activation_record.pop()

    result = String(str(left.get_value()) + str(right.get_value()))
    activation_record.push(result)

def _print(invokable, activation_record, interpreter):
    top = activation_record.pop()

    print top.get_value()

def init_string_prims(universe):
    primitives = {
        "print": _print,
        "+": _append,
    }

    universe.stringClass.add_primitives(primitives)
