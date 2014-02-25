from wlvlang.interpreter.objectspace.primitives.boolean_primitive import init_boolean_prims
from wlvlang.interpreter.objectspace.primitives.integer_primitive import init_integer_prims
from wlvlang.interpreter.objectspace.primitives.string_primitive import init_string_prims
from wlvlang.interpreter.objectspace.primitives.builtin_definitions import builtin_functions

from wlvlang.interpreter.objectspace.builtin import BuiltIn

def initialise_primitives(universe):
    init_integer_prims(universe)
    init_boolean_prims(universe)
    init_string_prims(universe)

    bifs = builtin_functions()
    space.builtin_functions = [None] * len(bifs)

    for name, value in bifs.iteritems():
        space.add_builtin_function(value[1], BuiltIn(name, value[0]))


