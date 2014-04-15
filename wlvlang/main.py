import os
from wlvlang.compiler import compiler
from wlvlang.interpreter.space import ObjectSpace
from wlvlang.runtime.executioncontext import  Universe

from wlvlang.interpreter.error import ErrorDisplay, NauRuntimeError

def _create_space():
    return ObjectSpace()

SPACE = _create_space()

def _main(args):

    if len(args) < 2:
        os.write(2, "No source file given\n")
        os.write(2, "    The first argument should be a wlvlang source code file\n")
        return 1

    error_displayer = ErrorDisplay("")

    # Trim command line arguments to pass into source parser
    # these are passed to the method that is created as an 'args'
    # argument
    arguments = args[1:]
    main_method, arg_local, arg_array = compiler.compile_file_with_arguments(args[1], SPACE, error_displayer, command_line_arguments=arguments)

    thread_count = 0
    universe = Universe(thread_count, SPACE)
    try:
        universe.start(main_method, arg_local, arg_array)
    except NauRuntimeError, e:
        error_displayer.handle_runtimeerror(e)
        return -1

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
