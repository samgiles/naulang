from wlvlang.interpreter.bytecode import Bytecode, bytecode_names

from wlvlang.interpreter.objectspace.array import Array
from wlvlang.interpreter.objectspace.primitive_object import PrimitiveObject
from wlvlang.interpreter.objectspace.channel import ChannelInterface, YieldException, SuspendException
from wlvlang.interpreter.objectspace.method import Method
from wlvlang.interpreter.objectspace.builtin import BuiltIn

from rpython.rlib import jit

class Interpreter(object):

    _immutable_fields = ["space"]

    HALT     = 1
    CONTINUE = 2
    YIELD    = 4
    SUSPEND  = 8

    def __init__(self, space):
        self.space = space

    def _invoke_global(self, global_index, frame):
        new_method = self.space.get_builtin_function(global_index)
        assert isinstance(new_method, BuiltIn)
        new_method.invoke(frame, self)

    def _invoke_method(self, method, frame, task):
        assert isinstance(method, Method)
        method.invoke(frame, task)

    def _invoke_method_async(self, new_method, frame, task):
        assert isinstance(new_method, Method)
        new_method.async_invoke(task)

    def _restore_previous_frame_or_exit(self, task):
            # Restore the caller
            is_root_frame = task.get_top_frame().is_root_frame()
            if is_root_frame:
                task.set_state(Interpreter.HALT)
                return False

            task.restore_previous_frame()
            task.set_state(Interpreter.CONTINUE)
            return True

    def interpreter_step(self, pc, method, frame, task):
        bytecode = method.get_bytecode(pc)

        if bytecode == Bytecode.HALT:
            return self._restore_previous_frame_or_exit(task)
        elif bytecode == Bytecode.LOAD_CONST:
            pc += 2
            literal = jit.promote(method.get_bytecode(pc - 1))
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
            value = frame.peek()
            value.w_or(frame, self.space)
            pc += 1
        elif bytecode == Bytecode.AND:
            value = frame.peek()
            assert isinstance(value, PrimitiveObject)
            value.w_and(frame, self.space)
            pc += 1
        elif bytecode == Bytecode.EQUAL:
            value = frame.peek()
            assert isinstance(value, PrimitiveObject)
            value.w_eq(frame, self.space)
            pc += 1
        elif bytecode == Bytecode.NOT_EQUAL:
            value = frame.peek()
            assert isinstance(value, PrimitiveObject)
            value.w_neq(frame, self.space)
            pc += 1
        elif bytecode == Bytecode.LESS_THAN:
            value = frame.peek()
            assert isinstance(value, PrimitiveObject)
            value.w_lt(frame, self.space)
            pc += 1
        elif bytecode == Bytecode.LESS_THAN_EQ:
            value = frame.peek()
            assert isinstance(value, PrimitiveObject)
            value.w_lteq(frame, self.space)
            pc += 1
        elif bytecode == Bytecode.GREATER_THAN:
            value = frame.peek()
            assert isinstance(value, PrimitiveObject)
            value.w_gt(frame, self.space)
            pc += 1
        elif bytecode == Bytecode.GREATER_THAN_EQ:
            value = frame.peek()
            assert isinstance(value, PrimitiveObject)
            value.w_gteq(frame, self.space)
            pc += 1
        elif bytecode == Bytecode.ADD:
            value = frame.peek()
            assert isinstance(value, PrimitiveObject)
            value.w_add(frame, self.space)
            pc += 1
        elif bytecode == Bytecode.SUB:
            value = frame.peek()
            assert isinstance(value, PrimitiveObject)
            value.w_sub(frame, self.space)
            pc += 1
        elif bytecode == Bytecode.MUL:
            value = frame.peek()
            assert isinstance(value, PrimitiveObject)
            value.w_mul(frame, self.space)
            pc += 1
        elif bytecode == Bytecode.DIV:
            value = frame.peek()
            assert isinstance(value, PrimitiveObject)
            value.w_div(frame, self.space)
            pc += 1
        elif bytecode == Bytecode.NOT:
            value = frame.peek()
            assert isinstance(value, PrimitiveObject)
            value.w_not(frame, self.space)
            pc += 1
        elif bytecode == Bytecode.NEG:
            value = frame.peek()
            assert isinstance(value, PrimitiveObject)
            value.w_neg(frame, self.space)
            pc += 1
        elif bytecode == Bytecode.MOD:
            value = frame.peek()
            assert isinstance(value, PrimitiveObject)
            value.w_mod(frame, self.space)
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
            value = frame.peek()
            assert isinstance(value, PrimitiveObject)
            value.w_print(frame, self.space)
            pc += 1
        elif bytecode == Bytecode.INVOKE:
            new_method = frame.pop()
            assert isinstance(method, Method)

            # Unlike other bytecodes, the invoke method
            # alters the state of the task currently running,
            # therefore by the time _invoke_method has successfully
            # returned the frame will belong to the new method, advancing and
            # saving the stack pointer at that point makes no sense and would
            # result in some missed instructions in the new method
            # In order to restart the interpreter loop we return early after
            # this call to _invoke_method
            frame.set_pc(pc + 1)
            self._invoke_method(new_method, frame, task)
            return True

        elif bytecode == Bytecode.INVOKE_ASYNC:
            new_method = frame.pop()
            assert isinstance(new_method, Method)
            frame.set_pc(pc + 1)
            self._invoke_method_async(new_method, frame, task)
            return True
        elif bytecode == Bytecode.INVOKE_GLOBAL:
            pc += 1
            global_index = method.get_bytecode(pc)
            self._invoke_global(global_index, frame)
            pc += 1
        elif bytecode == Bytecode.RETURN:

            # Push the result onto the callers frame
            caller = frame.get_previous_frame()
            if caller is not None:
                caller.push(frame.pop())

            # Restore the caller
            return self._restore_previous_frame_or_exit(task)
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
                received = channel.receive(task)
                frame.pop()
                frame.push(received)
                pc += 1
            except YieldException:
                task.set_state(Interpreter.YIELD)
                return False
            except SuspendException:
                task.set_state(Interpreter.SUSPEND)
                return False

        elif bytecode == Bytecode.CHAN_IN:
            expression = frame.pop()
            channel = frame.pop()
            assert isinstance(channel, ChannelInterface)
            pc += 1
            try:
                channel.send(task, expression)
            except YieldException:
                # Can continue this process (but try yielding to another)
                task.set_state(Interpreter.YIELD)
                frame.set_pc(pc)
                return False
            except SuspendException:
                # Send blocked (at rendezvous)
                task.set_state(Interpreter.SUSPEND)
                frame.set_pc(pc)
                return False

            # send succeeded; continuing
        else:
            raise TypeError("Bytecode is not implemented: %d" % bytecode)

        frame.set_pc(pc)
        task.set_state(Interpreter.CONTINUE)
        return True
