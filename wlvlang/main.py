import os
from wlvlang.compiler import compiler
from wlvlang.interpreter.interpreter import Interpreter
from wlvlang.interpreter.objectspace import ObjectSpace

def main(args):

    space = ObjectSpace()

    # Trim command line arguments to pass into source parser
    # these are passed to the method that is created as an 'args'
    # argument
    arguments = args[1:]
    main_method = compiler.parse_file(args[1], space, arguments)
    interpreter = Interpreter(space)

    # Activation record is None
    main_method.invoke(None, interpreter)

    # TODO: Return value
    return 0
