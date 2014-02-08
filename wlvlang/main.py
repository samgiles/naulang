import os
from wlvlang.compiler import compiler
from wlvlang.interpreter.interpreter import Interpreter
from wlvlang.interpreter.activationrecord import ActivationRecord
from wlvlang.vm.vm_universe import VM_Universe

def main(args):

    vm_universe = VM_Universe()

    # TODO: handle arguments from the cmdline
    path = os.getcwd()
    main_method = compiler.compile_source_from_file(path, args[1], vm_universe)
    interpreter = Interpreter(vm_universe)

    # Set up an activation record for the new method *Uses an arbitrarily large stack depth (200) as stack depth calculation has not been considered yet
    root_arec = ActivationRecord(main_method._locals + main_method._literals, len(main_method._locals), len(main_method._literals), 200, None)

    interpreter.interpret(main_method, root_arec)
