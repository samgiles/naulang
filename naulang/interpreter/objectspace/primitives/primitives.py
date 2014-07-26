from naulang.interpreter.objectspace.primitives.builtin_definitions import builtin_functions

from naulang.interpreter.objectspace.builtin import BuiltIn


def initialise_primitives(space):

    bifs = builtin_functions()
    space.builtin_functions = [None] * len(bifs)

    for name, value in bifs.iteritems():
        space.add_builtin_function(value[1], BuiltIn(name, value[0]))
