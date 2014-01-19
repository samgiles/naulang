from wlvlang.interpreter.bytecode import Bytecode

class Interpreter(object):


    def interpret(method, activation_record):
        """ Interpreter Main Loop """

        pc = 0

        while True:
            current_pc = pc

            bytecode = method.get_bytecode(current_pc)

            if bytecode == Bytecode.HALT:
                return
            elif bytecode == Bytecode.SEND:
                pass

            # Control Flow
            elif bytecode == Bytecode.BRANCH:
                # Unconditional Branch
                label_offset = method.get_bytecode(current_pc + 1)
                pc = current_pc + label_offset
            elif bytecode == Bytecode.BRANCH_EQ:
                # Condition branch
                # TODO: Send invoke _eq operation on type on top of
                # the stack, then test boolean condition on top of the
                # stack, and branch accordingly
                pass
            elif bytecode == Bytecode.IFEQ:

                pass
            elif bytecode == Bytecode.IFGT:
                pass
            elif bytecode == Bytecode.IFLT:
                pass
            elif bytecode == Bytecode.ADD:
                pass
            elif bytecode == Bytecode.SUB:
                pass
            elif bytecode == Bytecode.MUL:
                pass
            elif bytecode == Bytecode.DIV:
                pass
            elif bytecode == Bytecode.MOD:
                pass
            elif bytecode == Bytecode.PUSH:
                pass
            elif bytecode == Bytecode.POP:
                pass
