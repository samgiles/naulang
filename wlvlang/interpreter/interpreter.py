from wlvlang.interpreter.bytecode import Bytecode
from wlvlang.interpreter.activationrecord import ActivationRecord
from rpython.rlib import jit
from rpython.rlib.jit import JitDriver

jitdriver = JitDriver(greens=[], reds=[])

class Interpreter(object):

    _immutable_fields_ = ['universe']

    def __init__(self, universe):
        self.universe = universe

    def _send(self, arec, signature):
        invokable = arec.peek().get_class(self.universe).lookup_invokable(signature)
        invokable(None, arec, self)


    def interpret(self, method, activation_record):
        """ Interpreter Main Loop """
        pc = 0
        running = True

        jitdriver.can_enter_jit(bytecode_index=pc, interp=self, method=method, arec=activation_record)

        while running:

            jitdriver.jit_merge_point(bytecode_index=pc, interp=self, method=method, arec=activation_record)
            bytecode = method.get_bytecode(pc)

            if bytecode == Bytecode.HALT:
                running = False
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
                self._send(activation_record, ">")
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
                jmp_to = ord(method.get_bytecode(pc))
                condition = activation_record.pop()
                if condition.get_value() == False:
                    pc = jmp_to
                else:
                    pc += 1
            elif bytecode == Bytecode.JUMP_BACK:
                jmp_to = ord(method.get_bytecode(pc + 1))
                pc = jmp_to
            elif bytecode == Bytecode.PRINT:
                self._send(activation_record, "print")
                pc += 1
            elif bytecode == Bytecode.INVOKE:
                pc += 1
                local = ord(method.get_bytecode(pc))
                new_method = activation_record.get_local_at(local)
                new_method.invoke(activation_record, self, parent=method)
            elif bytecode == Bytecode.RETURN:
                pc += 1
            else:
                raise TypeError("Bytecode is not implemented: " + str(bytecode))

jitdriver = jit.JitDriver(
    greens=['bytecode_index', 'interp', 'method'],
    reds=['arec'])

def jitpolicy(driver):
    from rpython.jit.codewriter.policy import JitPolicy
    return JitPolicy()
