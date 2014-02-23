from wlvlang.vmobjects.primitives.integer_primitive import init_integer_prims
from wlvlang.vmobjects.primitives.boolean_primitive import init_boolean_prims
from wlvlang.vmobjects.primitives.string_primitive import init_string_prims

from wlvlang.vmobjects.primitive import Primitive

import time

def initialise_primitives(universe):
    init_integer_prims(universe)
    init_boolean_prims(universe)
    init_string_prims(universe)

    prims = primitive_functions()
    universe.primitive_functions = [None] * len(prims)
    for name, value in prims.iteritems():
        universe.add_primitive_function(
                value[1], Primitive(name, universe, value[0])
            )

def primitive_functions():
    return {
        "list": (_list_primitive, 0),
        "time": (_time_primitive, 1),
        "int" : (_int_primitive,  2),
    }

def _time_primitive(primitive, activation_record, interpreter):
    # HACK: Return an integer until floats are implemented
    activation_record.push(interpreter.universe.new_integer(time.time() * 1000000))

def _int_primitive(primitive, activation_record, interpreter):
    string = activation_record.pop()
    activation_record.push(interpreter.universe.new_integer(int(string.get_as_string())))

def _list_primitive(primitive, activation_record, interpreter):
    """ Creates a new array/list object and pushes onto stack """
    size = activation_record.pop()
    activation_record.push(interpreter.universe.new_array((size.get_integer_value())))
