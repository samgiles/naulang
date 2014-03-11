from wlvlang.interpreter.bytecode import Bytecode, bytecode_names

from wlvlang.interpreter.objectspace.array import Array
from wlvlang.interpreter.objectspace.channel import ChannelInterface, YieldException
from wlvlang.interpreter.objectspace.method import Method

from rpython.rlib import jit

def get_printable_location(pc, interp, method):
    return "%d: %s" % (pc, bytecode_names[method.get_bytecode(pc)])

jitdriver = jit.JitDriver(
        greens=['pc', 'interp', 'method'],
        reds=['frame', 'context'],
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

    def _send(self, arec, signature):
        invokable = arec.peek().get_class(self.space).lookup_invokable(signature)
        invokable(None, arec, self)

    def pre_execute(self, pc, method, activation_record):
        """ Interpreter hooks, (used by the debugger) """
        pass

    def post_execute(self, pc, method, activation_record):
        """ Interpreter hooks, (used by the debugger) """
        pass


    @jit.unroll_safe
    def interpreter_step(self, context):
        pc = context.get_pc()
        method = context.get_current_method()
        frame = context.get_top_frame()

        self.pre_execute(pc, method, frame)

        #jitdriver.jit_merge_point(
        #        pc=pc,
        #        interp=self,
        #        frame=frame,
        #        method=method,
        #        context=context
        #    )

        bytecode = method.get_bytecode(pc)

        if bytecode == Bytecode.HALT:
            context.set_state(Interpreter.HALT)
            return False
        elif bytecode == Bytecode.LOAD_CONST:
            pc += 1
            literal = method.get_bytecode(pc)
            pc += 1
            frame.push(frame.get_literal_at(literal))
        elif bytecode == Bytecode.LOAD:
            pc += 1
            local = method.get_bytecode(pc)
            pc += 1
            frame.push(frame.get_local_at(local))
        elif bytecode == Bytecode.STORE:
            pc += 1
            local = method.get_bytecode(pc)
            pc += 1
            frame.set_local_at(local, frame.pop())
        elif bytecode == Bytecode.OR:
            self._send(frame, "or")
            pc += 1
        elif bytecode == Bytecode.AND:
            self._send(frame, "and")
            pc += 1
        elif bytecode == Bytecode.EQUAL:
            self._send(frame, "==")
            pc += 1
        elif bytecode == Bytecode.NOT_EQUAL:
            self._send(frame, "!=")
            pc += 1
        elif bytecode == Bytecode.LESS_THAN:
            self._send(frame, "<")
            pc += 1
        elif bytecode == Bytecode.LESS_THAN_EQ:
            self._send(frame, "<=")
            pc += 1
        elif bytecode == Bytecode.GREATER_THAN:
            self._send(frame, ">")
            pc += 1
        elif bytecode == Bytecode.GREATER_THAN_EQ:
            self._send(frame, ">=")
            pc += 1
        elif bytecode == Bytecode.ADD:
            self._send(frame, "+")
            pc += 1
        elif bytecode == Bytecode.SUB:
            self._send(frame, "-")
            pc += 1
        elif bytecode == Bytecode.MUL:
            self._send(frame, "*")
            pc += 1
        elif bytecode == Bytecode.DIV:
            self._send(frame, "/")
            pc += 1
        elif bytecode == Bytecode.NOT:
            self._send(frame, "not")
            pc += 1
        elif bytecode == Bytecode.NEG:
            self._send(frame, "_neg")
            pc += 1
        elif bytecode == Bytecode.MOD:
            self._send(frame, "%")
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
            self._send(frame, "print")
            pc += 1
        elif bytecode == Bytecode.INVOKE:
            pc += 1
            local = method.get_bytecode(pc)
            pc += 1
            context.set_pc(pc)
            new_method = frame.get_local_at(local)
            new_method.invoke(context, self)
            return True
        elif bytecode == Bytecode.INVOKE_ASYNC:
            pc += 1
            local = method.get_bytecode(pc)
            new_method = frame.get_local_at(local)
            assert isinstance(new_method, Method)
            new_method.async_invoke(context, self)
            pc += 1
        elif bytecode == Bytecode.INVOKE_GLOBAL:
            pc += 1
            global_index = method.get_bytecode(pc)
            new_method = self.space.get_builtin_function(global_index)
            new_method.invoke(context, self)
            pc += 1
        elif bytecode == Bytecode.RETURN:

            # Push the result onto the callers frame
            caller = frame.get_previous_record()
            if caller is not None:
                caller.push(frame.pop())

            # Restore the caller
            context.restore_previous_frame()
            context.set_state(Interpreter.CONTINUE)
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
                context.set_state(Interpreter.YIELD)
                context.set_pc(pc)
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

        context.set_pc(pc)
        context.set_state(Interpreter.CONTINUE)
        return True
