from wlvlang.interpreter.interpreter import Interpreter
from wlvlang.interpreter.bytecode import bytecode_names
class Debugger(object):

    def pre_execute(self, interp, pc, method, activation_record):
        current_bytecode = method.get_bytecode(pc)
        current_bytecode_name = bytecode_names[current_bytecode]
        print current_bytecode_name

    def post_execute(self, interp, pc, method, activation_record):
        pass


DEBUGGER = Debugger()

def _pre_execute(interp, pc, method, activation_record):
    DEBUGGER.pre_execute(interp, pc, method, activation_record)

def _post_execute(interp, pc, method, activation_record):
    DEBUGGER.post_execute(interp, pc, method, activation_record)

Interpreter.pre_execute = _pre_execute
Interpreter.post_execute = _post_execute

def get_debugger():
    return DEBUGGER


