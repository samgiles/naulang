from wlvlang.interpreter.objectspace.primitives.boolean_primitive import init_boolean_prims
from wlvlang.interpreter.objectspace.primitives.integer_primitive import init_integer_prims
from wlvlang.interpreter.objectspace.primitives.string_primitive import init_string_prims
from wlvlang.interpreter.objectspace.primitives.builtin_definitions import builtin_functions

from wlvlang.interpreter.objectspace.builtin import BuiltIn

def initialise_primitives(space):
    init_integer_prims(space)
    init_boolean_prims(space)
    init_string_prims(space)

    bifs = builtin_functions()
    space.builtin_functions = [None] * len(bifs)

    for name, value in bifs.iteritems():
        space.add_builtin_function(value[1], BuiltIn(name, value[0]))


