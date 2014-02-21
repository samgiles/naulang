from wlvlang.vmobjects.primitives.integer_primitive import init_integer_prims
from wlvlang.vmobjects.primitives.boolean_primitive import init_boolean_prims

from wlvlang.vmobjects.primitive import Primitive

def initialise_primitives(universe):
    init_integer_prims(universe)
    init_boolean_prims(universe)

    prims = primitive_functions()
    universe.primitive_functions = [None] * len(prims)
    for name, value in prims.iteritems():
        print value
        universe.add_primitive_function(
                value[1], Primitive(name, universe, value[0])
            )

def primitive_functions():
    return {
        "list": (_list_primitive, 0)
    }

def _list_primitive(primitive, activation_record, interpreter):
    """ Creates a new array/list object and pushes onto stack """
    size = activation_record.pop()
    activation_record.push(interpreter.universe.new_array((size.get_value())))

