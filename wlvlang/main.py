import os
from wlvlang.compiler import compiler
from wlvlang.interpreter.space import ObjectSpace
from wlvlang.runtime.executioncontext import  Universe

def _create_space():
    return ObjectSpace()

SPACE = _create_space()

def _main(args):

    if len(args) < 2:
        os.write(2, "No source file given\n")
        os.write(2, "    The first argument should be a wlvlang source code file\n")
        return 1

    # Trim command line arguments to pass into source parser
    # these are passed to the method that is created as an 'args'
    # argument
    arguments = args[1:]
    main_method, arg_local, arg_array = compiler.compile_file_with_arguments(args[1], SPACE, arguments)

    # Add file arguments into 'args' array parameter
    # Activation record is None

    thread_count = 0
    universe = Universe(thread_count, SPACE)
    universe.start(main_method, arg_local, arg_array)

    return 0

def _exception_wrapped(main_method):
    if not __debug__:
        def wrapped(args):
            try:
                return main_method(args)
            except:
                return -1
        return wrapped
    else:
        return main_method


main = _exception_wrapped(_main)
