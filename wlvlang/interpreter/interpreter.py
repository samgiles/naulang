from wlvlang.interpreter.bytecode import Bytecode, bytecode_names
from wlvlang.interpreter.activationrecord import ActivationRecord

from wlvlang.interpreter.objectspace.array import Array

from rpython.rlib import jit

def get_printable_location(pc, interp, method):
    return "%d: %s" % (pc, bytecode_names[method.get_bytecode(pc)])

jitdriver = jit.JitDriver(
        greens=['pc', 'interp', 'method'],
        reds=['running', 'frame'],
        virtualizables=['frame'],
        get_printable_location=get_printable_location
    )

class Interpreter(object):

    def __init__(self, space):
        self.space = space

    def _send(self, arec, signature):
        invokable = arec.peek().get_class(self.space).lookup_invokable(signature)
        invokable(None, arec, self)

    def pre_execute(self, pc, method, activation_record):
        """ Interpreter hooks, (used by the debugger) """
        pass

    def post_execute(self, pc, method, activation_record):
        """ Interpreter hooks, (used by the debugger) """
        pass

    def interpret(self, method, activation_record):
        """ Interpreter Main Loop """
        pc = 0
        running = True


        while running:
            jitdriver.jit_merge_point(
                    pc=pc,
                    interp=self,
                    running=running,
                    frame=activation_record,
                    method=method
                )

            bytecode = method.get_bytecode(pc)

            self.pre_execute(pc, method, activation_record)

            if bytecode == Bytecode.HALT:
                running = False
            elif bytecode == Bytecode.LOAD_CONST:
                pc += 1
                literal = method.get_bytecode(pc)
                pc += 1
                activation_record.push(activation_record.get_literal_at(literal))
            elif bytecode == Bytecode.LOAD:
                pc += 1
                local = method.get_bytecode(pc)
                pc += 1
                activation_record.push(activation_record.get_local_at(local))
            elif bytecode == Bytecode.STORE:
                pc += 1
                local = method.get_bytecode(pc)
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
            elif bytecode == Bytecode.GREATER_THAN_EQ:
                self._send(activation_record, ">=")
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
                self._send(activation_record, "_neg")
                pc += 1
            elif bytecode == Bytecode.MOD:
                self._send(activation_record, "%")
                pc += 1
            elif bytecode == Bytecode.JUMP_IF_FALSE:
                pc += 1
                jmp_to = method.get_bytecode(pc)
                condition = activation_record.pop()
                if condition.get_boolean_value() == False:
                    pc = jmp_to
                else:
                    pc += 1
            elif bytecode == Bytecode.JUMP_BACK:
                jmp_to = method.get_bytecode(pc + 1)
                pc = jmp_to
            elif bytecode == Bytecode.PRINT:
                self._send(activation_record, "print")
                pc += 1
            elif bytecode == Bytecode.INVOKE:
                pc += 1
                local = method.get_bytecode(pc)
                new_method = activation_record.get_local_at(local)
                new_method.invoke(activation_record, self)
                pc += 1
            elif bytecode == Bytecode.INVOKE_GLOBAL:
                pc += 1
                global_index = method.get_bytecode(pc)
                new_method = self.space.get_builtin_function(global_index)
                new_method.invoke(activation_record, self)
                pc += 1
            elif bytecode == Bytecode.RETURN:
                caller = activation_record.get_previous_record()
                if caller is None:
                    # TODO: Logic for root function exit and returning
                    running = False

                caller.push(activation_record.pop())
                running = False
            elif bytecode == Bytecode.ARRAY_LOAD:
                index = activation_record.pop()
                array = activation_record.pop()
                assert isinstance(array, Array)     # RPython
                activation_record.push(array.get_value_at(index.get_integer_value()))
                pc += 1
            elif bytecode == Bytecode.ARRAY_STORE:
                value = activation_record.pop()
                index = activation_record.pop()
                array = activation_record.pop()
                assert isinstance(array, Array)     # RPython
                array.set_value_at(index.get_integer_value(), value)
                pc += 1
            elif bytecode == Bytecode.LOAD_DYNAMIC:
                pc += 1
                local_slot = method.get_bytecode(pc)
                pc += 1
                level = method.get_bytecode(pc)
                pc += 1
                activation_record.push(activation_record.get_dynamic_at(local_slot, level))
            elif bytecode == Bytecode.STORE_DYNAMIC:
                pc += 1
                local_slot = method.get_bytecode(pc)
                pc += 1
                level = method.get_bytecode(pc)
                value = activation_record.pop()
                activation_record.set_dynamic_at(local_slot, level, value)
                pc += 1
            elif bytecode == Bytecode.COPY_LOCAL:
                """ Copy the top of the stack into a local, preserving the stack """
                pc += 1
                local = method.get_bytecode(pc)
                pc += 1
                activation_record.set_local_at(local, activation_record.peek())
            elif bytecode == Bytecode.DUP:
                activation_record.push(activation_record.peek())
                pc += 1
            else:
                raise TypeError("Bytecode is not implemented: %d" % bytecode)

            self.post_execute(pc, method, activation_record)
