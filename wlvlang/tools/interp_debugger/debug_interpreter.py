from wlvlang.interpreter.interpreter import Interpreter
from wlvlang.interpreter.bytecode import bytecode_names
import os

import sys
if sys.version_info[0] < 3:
    get_input = raw_input
else:
    get_input = input

class Debugger(object):

    def __init__(self):
        self._lastaction = "?"

    def get_next_action(self):
        return get_input(">>> ")

    def handle_command(self, interp, pc, method, activation_record):
        try:
            action = self.get_next_action()
        except EOFError:
            action = self._lastaction

        print action
        if action == "next" or action == "n":
            self._lastaction = "n"
            return
        elif action == "stack":
            i = 0
            for stack_item in activation_record._stack:
                if i == activation_record._local_offset:
                    os.write(1, "-------------------\n")
                elif i == activation_record._literal_offset:
                    os.write(1, "-------------------\n")
                elif i == activation_record._stack_base:
                    os.write(1, "-------------------\n")

                os.write(1, str(stack_item))

                if i == activation_record._stack_base:
                    os.write(1, "   <- STACK_BASE")

                if i == activation_record._literal_offset:
                    os.write(1, "   <- LITERALS")
                if i == activation_record._local_offset:
                    os.write(1, "   <- LOCALS")

                if i == activation_record._stack_pointer - 1:
                    os.write(1, "   <- HEAD")
                    os.write(1, "\n")
                    break

                os.write(1, "\n")
                i += 1
            self._lastaction = "stack"
            self.handle_command(interp, pc, method, activation_record)
        elif action == "?" or action == "help":
            print """
Commands:
    (n)ext    -- Perform next bytecode operation
    stack     -- Print the entire stack
    ? or help -- Print help information
            """
            self._lastaction = "?"
            self.handle_command(interp, pc, method, activation_record)
        else:
            self.handle_command(interp, pc, method, activation_record)



    def pre_execute(self, interp, pc, method, activation_record):
        current_bytecode = method.get_bytecode(pc)
        current_bytecode_name = bytecode_names[current_bytecode]
        print current_bytecode_name
        self.handle_command(interp, pc, method, activation_record)

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


