from wlvlang.interpreter.interpreter import Interpreter
from wlvlang.interpreter.bytecode import bytecode_names, Bytecode
import os

import sys
if sys.version_info[0] < 3:
    get_input = raw_input
else:
    get_input = input

class Debugger(object):

    def __init__(self, view=None):
        self._view = view
        self._lastaction = "?"

    def set_view(self, view):
        self._view = view

    def get_next_action(self):
        return self._view.get_key_press()

    def get_stack_info(self, activation_record):
            info = ""
            i = 0
            for stack_item in activation_record._stack:
                if i == activation_record._local_offset:
                    info += "-------------------\n"
                elif i == activation_record._literal_offset:
                    info += "-------------------\n"
                elif i == activation_record._stack_base:
                    info += "-------------------\n"

                info += str(stack_item)

                if i == activation_record._stack_base:
                    info += "   <- STACK_BASE"

                if i == activation_record._literal_offset:
                    info += "   <- LITERALS"
                if i == activation_record._local_offset:
                    info += "   <- LOCALS"

                if i == activation_record._stack_pointer - 1:
                    info += "   <- HEAD\n"
                    break

                info += "\n"
                i += 1

            return info


    def handle_command(self, interp, pc, method, activation_record):

        while True:
            action = self.get_next_action()
            if action == ord("n"):
                return


    def interpret(self, interpret, method, activation_record):
        self._view.load_method_bytecode(method, interpret)

    def pre_execute(self, interp, pc, method, activation_record):
        stack_info = self.get_stack_info(activation_record)
        self._view.update_stack_value(stack_info)
        self._view.update_bytecode_position(pc, method, interp)
        self.handle_command(interp, pc, method, activation_record)

    def handle_bytecode(self, pc, method, activation_record):
        pass
    def post_execute(self, interp, pc, method, activation_record):
        pass


DEBUGGER = Debugger()

def _pre_execute(interp, pc, method, activation_record):
    DEBUGGER.pre_execute(interp, pc, method, activation_record)

def _post_execute(interp, pc, method, activation_record):
    DEBUGGER.post_execute(interp, pc, method, activation_record)

def _interp(interp, method, activation_record):
    DEBUGGER.interpret(interp, method, activation_record)
    Interpreter.interp(interp, method, activation_record)

Interpreter.interp = Interpreter.interpret
Interpreter.interpret = _interp
Interpreter.pre_execute = _pre_execute
Interpreter.post_execute = _post_execute

def get_debugger():
    return DEBUGGER


