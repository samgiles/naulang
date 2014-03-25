import os
from wlvlang.compiler import compiler
from wlvlang.interpreter.activationrecord import ActivationRecord
from wlvlang.interpreter.space import ObjectSpace

from wlvlang.runtime.executioncontext import Task, ThreadLocalSched, Universe


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
    main_method, arg_local, arg_array = compiler.compile_file_with_arguments(args[1], space, arguments)
    # Add file arguments into 'args' array parameter
    # Activation record is None

    thread_count = 0
    universe = Universe(thread_count, space)
    universe.start(main_method, arg_local, arg_array)

    # TODO: Return value
    return 0
