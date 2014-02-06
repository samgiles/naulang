from wlvlang.interpreter.bytecode import Bytecode

class Interpreter(object):


    def _send(self, arec, signature):
        invokable = arec.peek().get_class().lookup_invokable(signature)
        invokable.invoke(arec, self)

    def interpret(self, method, activation_record):
        """ Interpreter Main Loop """

        pc = 0

        while True:
            current_pc = pc

            bytecode = method.get_bytecode(current_pc)

            if bytecode == Bytecode.HALT:
                return
            elif bytecode == Bytecode.LOAD_CONST:
                pc += 1
                literal = ord(method.get_bytecode(pc))
                pc += 1
                activation_record.push(activation_record.get_literal_at(literal))
            elif bytecode == Bytecode.LOAD:
                pc += 1
                local = ord(method.get_bytecode(pc))
                pc += 1
                activation_record.push(activation_record.get_local_at(local))
            elif bytecode == Bytecode.STORE:
                pc += 1
                local = ord(method.get_bytecode(pc))
                pc += 1
                activation_record.set_local_at(local, activation_record.pop())
            elif bytecode == Bytecode.OR:
                self._send(activation_record, "or")
                pc += 1
            elif bytecode == Bytecode.AND:
                self._send(activation_record, "and")
                pc += 1
            elif bytecode == Bytecode.EQUAL:
                self._send(activation_record, "==")
                pc += 1
            elif bytecode == Bytecode.NOT_EQUAL:
                self._send(activation_record, "!=")
                pc += 1
            elif bytecode == Bytecode.LESS_THAN:
                self._send(activation_record, "<")
                pc += 1
            elif bytecode == Bytecode.LESS_THAN_EQ:
                self._send(activation_record, "<=")
                pc += 1
            elif bytecode == Bytecode.GREATER_THAN:
                self._send(activation_record, "")
                pc += 1
            elif bytecode == Bytecode.ADD:
                self._send(activation_record, "+")
                pc += 1
            elif bytecode == Bytecode.SUB:
                self._send(activation_record, "-")
                pc += 1
            elif bytecode == Bytecode.MUL:
                self._send(activation_record, "*")
                pc += 1
            elif bytecode == Bytecode.DIV:
                self._send(activation_record, "/")
                pc += 1
            elif bytecode == Bytecode.NOT:
                self._send(activation_record, "not")
                pc += 1
            elif bytecode == Bytecode.NEG:
                pc += 1
            elif bytecode == Bytecode.JUMP_IF_FALSE:
                pc += 1
                jmp_to = ord(activation_record.get_bytecode(pc))
                condition = activation_record.pop()
                if condition.get_value() == False:
                    pc = jmp_to
                else:
                    pc += 1
            elif bytecode == Bytecode.JUMP_BACK:
                jmp_to = ord(activation_record.get_bytecode(pc + 1))
                pc = jmp_to
            elif bytecode == Bytecode.PRINT:
                self._send(activation_record, "print")
                pc += 1
            elif bytecode == Bytecode.INVOKE:
                pass
            elif bytecode == Bytecode.RETURN:
                pc += 1
                pass
            else:
                raise TypeError("Bytecode is not implemented: " + str(bytecode))

            if pc == current_pc:
                pc = pc + 1
