from wlvlang.interpreter.bytecode import Bytecode, bytecode_names

from wlvlang.interpreter.objectspace.array import Array
from wlvlang.interpreter.objectspace.channel import ChannelInterface, YieldException
from wlvlang.interpreter.objectspace.method import Method

from rpython.rlib import jit

def get_printable_location(pc, interp, method):
    return "%d: %s" % (pc, bytecode_names[method.get_bytecode(pc)])

jitdriver = jit.JitDriver(
        greens=['pc', 'interp', 'method'],
        reds=['frame', 'task'],
        virtualizables=['frame'],
        get_printable_location=get_printable_location
    )

class Interpreter(object):

    _immutable_fields = ["space"]

    HALT     = 1
    CONTINUE = 2
    YIELD    = 4

    def __init__(self, space):
        self.space = space

    def _invoke_primitive(self, task, signature):
        frame = task.get_top_frame()
        invokable = frame.peek().get_class(self.space).lookup_invokable(signature)
        invokable(None, frame, self)

    def _invoke_global(self, global_index, task):
        new_method = self.space.get_builtin_function(global_index)
        new_method.invoke(task, self)

    def _invoke_method(self, method_at_local, task):
        new_method = task.get_top_frame().get_local_at(method_at_local)
        new_method.invoke(task)

    @jit.unroll_safe
    def interpreter_step(self, task):
        frame = task.get_top_frame()

        if frame is None:
            task.set_state(Interpreter.HALT)
            return False

        pc = frame.get_pc()
        method = task.get_current_method()

        jitdriver.jit_merge_point(
                pc=pc,
                interp=self,
                frame=frame,
                method=method,
                task=task
            )

        bytecode = method.get_bytecode(pc)

        if bytecode == Bytecode.HALT:
            task.set_state(Interpreter.HALT)
            return False
        elif bytecode == Bytecode.LOAD_CONST:
            pc += 2
            literal = method.get_bytecode(pc - 1)
            frame.push(frame.get_literal_at(literal))
        elif bytecode == Bytecode.LOAD:
            pc += 2
            local = method.get_bytecode(pc - 1)
            frame.push(frame.get_local_at(local))
        elif bytecode == Bytecode.STORE:
            pc += 2
            local = method.get_bytecode(pc - 1)
            frame.set_local_at(local, frame.pop())
        elif bytecode == Bytecode.OR:
            self._invoke_primitive(task, "or")
            pc += 1
        elif bytecode == Bytecode.AND:
            self._invoke_primitive(task, "and")
            pc += 1
        elif bytecode == Bytecode.EQUAL:
            self._invoke_primitive(task, "==")
            pc += 1
        elif bytecode == Bytecode.NOT_EQUAL:
            self._invoke_primitive(task, "!=")
            pc += 1
        elif bytecode == Bytecode.LESS_THAN:
            self._invoke_primitive(task, "<")
            pc += 1
        elif bytecode == Bytecode.LESS_THAN_EQ:
            self._invoke_primitive(task, "<=")
            pc += 1
        elif bytecode == Bytecode.GREATER_THAN:
            self._invoke_primitive(task, ">")
            pc += 1
        elif bytecode == Bytecode.GREATER_THAN_EQ:
            self._invoke_primitive(task, ">=")
            pc += 1
        elif bytecode == Bytecode.ADD:
            self._invoke_primitive(task, "+")
            pc += 1
        elif bytecode == Bytecode.SUB:
            self._invoke_primitive(task, "-")
            pc += 1
        elif bytecode == Bytecode.MUL:
            self._invoke_primitive(task, "*")
            pc += 1
        elif bytecode == Bytecode.DIV:
            self._invoke_primitive(task, "/")
            pc += 1
        elif bytecode == Bytecode.NOT:
            self._invoke_primitive(task, "not")
            pc += 1
        elif bytecode == Bytecode.NEG:
            self._invoke_primitive(task, "_neg")
            pc += 1
        elif bytecode == Bytecode.MOD:
            self._invoke_primitive(task, "%")
            pc += 1
        elif bytecode == Bytecode.JUMP_IF_FALSE:
            pc += 1
            jmp_to = method.get_bytecode(pc)
            condition = frame.pop()
            if condition.get_boolean_value() == False:
                pc = jmp_to
            else:
                pc += 1
        elif bytecode == Bytecode.JUMP:
            jmp_to = method.get_bytecode(pc + 1)
            pc = jmp_to
        elif bytecode == Bytecode.PRINT:
            self._invoke_primitive(task, "print")
            pc += 1
        elif bytecode == Bytecode.INVOKE:
            pc += 2
            local = method.get_bytecode(pc - 1)

            # Unlike other bytecodes, the invoke method
            # alters the state of the task currently running,
            # therefore by the time _invoke_method has successfully
            # returned the frame will belong to the new method, advancing and
            # saving the stack pointer at that point makes no sense and would
            # result in some missed instructions in the new method
            # In order to restart the interpreter loop we return early after
            # this call to _invoke_method
            frame.set_pc(pc)
            self._invoke_method(local, task)
            return True

        elif bytecode == Bytecode.INVOKE_ASYNC:
            pc += 1
            local = method.get_bytecode(pc)
            new_method = frame.get_local_at(local)
            assert isinstance(new_method, Method)
            new_method.async_invoke(task, self)
            pc += 1
        elif bytecode == Bytecode.INVOKE_GLOBAL:
            pc += 1
            global_index = method.get_bytecode(pc)
            self._invoke_global(global_index, task)
            pc += 1
        elif bytecode == Bytecode.RETURN:

            # Push the result onto the callers frame
            caller = frame.get_previous_record()
            if caller is not None:
                caller.push(frame.pop())

            # Restore the caller
            task.restore_previous_frame()
            task.set_state(Interpreter.CONTINUE)
            return True
        elif bytecode == Bytecode.ARRAY_LOAD:
            index = frame.pop()
            array = frame.pop()
            assert isinstance(array, Array)     # RPython
            frame.push(array.get_value_at(index.get_integer_value()))
            pc += 1
        elif bytecode == Bytecode.ARRAY_STORE:
            value = frame.pop()
            index = frame.pop()
            array = frame.pop()
            assert isinstance(array, Array)     # RPython
            array.set_value_at(index.get_integer_value(), value)
            pc += 1
        elif bytecode == Bytecode.LOAD_DYNAMIC:
            pc += 1
            local_slot = method.get_bytecode(pc)
            pc += 1
            level = method.get_bytecode(pc)
            pc += 1
            frame.push(frame.get_dynamic_at(local_slot, level))
        elif bytecode == Bytecode.STORE_DYNAMIC:
            pc += 1
            local_slot = method.get_bytecode(pc)
            pc += 1
            level = method.get_bytecode(pc)
            value = frame.pop()
            frame.set_dynamic_at(local_slot, level, value)
            pc += 1
        elif bytecode == Bytecode.COPY_LOCAL:
            """ Copy the top of the stack into a local, preserving the stack """
            pc += 1
            local = method.get_bytecode(pc)
            pc += 1
            frame.set_local_at(local, frame.peek())
        elif bytecode == Bytecode.DUP:
            frame.push(frame.peek())
            pc += 1

        elif bytecode == Bytecode.CHAN_OUT:
            channel = frame.peek()
            assert isinstance(channel, ChannelInterface)
            try:
                received = channel.receive()
            except YieldException:
                task.set_state(Interpreter.YIELD)
                task.set_pc(pc)
                return False

            frame.pop()
            frame.push(received)
            pc += 1
        elif bytecode == Bytecode.CHAN_IN:
            expression = frame.pop()
            channel = frame.pop()
            assert isinstance(channel, ChannelInterface)
            channel.send(expression)
            pc += 1
        else:
            raise TypeError("Bytecode is not implemented: %d" % bytecode)

        frame.set_pc(pc)
        task.set_state(Interpreter.CONTINUE)
        return True
