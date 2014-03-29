from wlvlang.interpreter.objectspace.object import Object

from rpython.rlib.rarithmetic import r_uint
from rpython.rlib import jit

class Frame(Object):
    """ Defines an Activation Record. """

    _virtualizable_ = ["_locals[*]", "_stack[*]", "_pc", "_stack_pointer"]
    _immutable_fields_ = ["_literals[*]"]

    def __init__(self, previous_frame=None, method=None, access_link=None):
        self = jit.hint(self, access_directly=True, fresh_virtualizable=True)

        self._stack = [None] * method.stack_depth
        self._stack_pointer = r_uint(0)

        self.previous_frame = previous_frame
        self.access_link = access_link

        self._locals = [None] * method.local_count
        self._literals = method.literals

        self._pc = 0
        self.method = method
        self._set_up_local_methods()

    def set_pc(self, pc):
        self._pc = pc

    def get_pc(self):
        return self._pc

    @jit.unroll_safe
    def _set_up_local_methods(self):
        from wlvlang.interpreter.objectspace.method import Method
        for i in range(0, len(self._literals)):
            if isinstance(self._literals[i], Method):
                self._literals[i] = self._literals[i].copy()

                # Since literal methods exist in methods that have been
                # invoked we set the activation record
                self._literals[i].set_enclosing_frame(self)

    def get_previous_frame(self):
        """ Get the previous activation record. """
        return self.previous_frame;

    def set_previous_frame(self, previous):
        self.previous_frame = previous

    def get_access_link(self):
        """ Get the access link for this object (if it has one).  Returns None if it does not """
        return self.access_link;

    def is_root_frame(self):
        return self.get_previous_frame() is None

    def push(self, value):
        """ Push an object onto the stack """
        stack_pointer = jit.promote(self._stack_pointer)
        self._stack[stack_pointer] = value
        self._stack_pointer = stack_pointer + 1

    def pop(self):
        """ Pop an object off of the stack """
        assert self._stack_pointer > 0
        self._stack_pointer = self._stack_pointer - 1
        return self._stack[self._stack_pointer]

    def peek(self):
        """ Peek at the object on top of the stack. """
        assert self._stack_pointer > 0
        return self._stack[self._stack_pointer - 1]

    def get_literal_at(self, index):
        assert index < len(self._literals) and index >= 0
        return self._literals[index]

    def get_local_at(self, index):
        index = jit.promote(index)
        assert index < len(self._locals) and index >= 0
        return self._locals[index]

    def set_local_at(self, index, value):
        index = jit.promote(index)
        assert index < len(self._locals) and index >= 0
        self._locals[index] = value

    def _get_frame_at_level(self, level):
        i = 1
        frame = self.get_access_link()
        while i is not level:
            frame = frame.get_access_link()
            i += 1

        return frame

    def get_dynamic_at(self, index, level):
        frame = self._get_frame_at_level(level)
        if frame: return frame.get_local_at(index)

        return None

    def set_dynamic_at(self, index, level, value):
        frame = self._get_frame_at_level(level)
        return frame.set_local_at(index, value)
