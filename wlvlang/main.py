import os
from wlvlang.compiler import compiler
from wlvlang.interpreter.activationrecord import ActivationRecord
from wlvlang.interpreter.space import ObjectSpace

from wlvlang.runtime.executioncontext import Task, ThreadLocalSched

def main(args):

    if len(args) < 2:
        os.write(2, "No source file given\n")
        os.write(2, "    The first argument should be a wlvlang source code file\n")
        return 1

    space = ObjectSpace()
    sched = ThreadLocalSched(space)

    # Trim command line arguments to pass into source parser
    # these are passed to the method that is created as an 'args'
    # argument
    arguments = args[1:]
    main_method, arg_local, arg_array = compiler.parse_file_with_arguments(args[1], space, arguments)
    # Add file arguments into 'args' array parameter
    # Activation record is None

    new_arec = ActivationRecord(method=main_method)
    new_arec.set_local_at(arg_local, arg_array)

    main_task = Task()
    main_task.set_top_frame(new_arec)

    sched.add_task(main_task)

    # Run main context...TODO: Sched
    sched.run_task(0)

    # TODO: Return value
    return 0
