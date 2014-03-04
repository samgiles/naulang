import os
from wlvlang.compiler import compiler
from wlvlang.interpreter.interpreter import Interpreter
from wlvlang.interpreter.activationrecord import ActivationRecord
from wlvlang.interpreter.space import ObjectSpace

def main(args):

    if len(args) < 2:
        os.write(2, "No source file given\n")
        os.write(2, "    The first argument should be a wlvlang source code file\n")
        return 1

    space = ObjectSpace()

    # Trim command line arguments to pass into source parser
    # these are passed to the method that is created as an 'args'
    # argument
    arguments = args[1:]
    main_method, arg_local, arg_array = compiler.parse_file_with_arguments(args[1], space, arguments)
    interpreter = Interpreter(space)
    # Add file arguments into 'args' array parameter
    # Activation record is None

    new_arec = ActivationRecord([None] * len(main_method.locals), main_method.literals, main_method.stack_depth, None)
    new_arec.set_local_at(arg_local, arg_array)
    interpreter.interpret(main_method, new_arec)

    # TODO: Return value
    return 0
