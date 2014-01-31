from wlvlang.interpreter.bytecode import Bytecode

class Interpreter(object):


    def _send(self, arec, signature, classs, bytecode_index):
        invokable = classs.lookup_invokable(signature)
        invokable.invoke(arec, self)

    def interpret(method, activation_record):
        """ Interpreter Main Loop """

        pc = 0

        while True:
            current_pc = pc

            bytecode = method.get_bytecode(current_pc)

            if bytecode == Bytecode.HALT:
                return
            elif bytecode == Bytecode.SEND:
                signature_index = method.get_bytecode(current_pc + 1)
                signature = method.get_literal(literal_index)
                pass
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
                self._send(activation_record, "+", activation_record.peek().get_class())
            elif bytecode == Bytecode.SUB:
                self._send(activation_record, "-", activation_record.peek().get_class())
            elif bytecode == Bytecode.MUL:
                self._send(activation_record, "*", activation_record.peek().get_class())
            elif bytecode == Bytecode.DIV:
                self._send(activation_record, "/", activation_record.peek().get_class())
            elif bytecode == Bytecode.MOD:
                self._send(activation_record, "%", activation_record.peek().get_class())
            elif bytecode == Bytecode.PUSH:
                pass
            elif bytecode == Bytecode.POP:
                pass
