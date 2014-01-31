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
                # Branch if the value on the top of the stack is a boolean true
                val = activation_record.pop()
                new_pc = activation_record.pop().get_value()

                if val.get_value():
                    pc = new_pc

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
                # Push a literal from the arec at a predefined constant
                stack_position = activation_record.pop()
                activation_record.push(activation_record.get_element_at(stack_position.get_value()))
            elif bytecode == Bytecode.POP:
                activation_record.pop()
            else:
                raise TypeError("Bytecode is not implemented: " + str(bytecode))

            if pc == current_pc:
                pc = pc + 1
