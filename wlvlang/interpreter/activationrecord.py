from wlvlang.interpreter.objectspace.object import Object

from rpython.rlib import jit

class ActivationRecord(Object):

    _virtualizable_ = ["_locals[*]", "_literals[*]", "_stack_pointer"]
    _immutable_fields_ = ["_literals", "_locals"]

    """
        Defines an Activation Record.
    """

    def __init__(self, locals, literals, temp_size, previous_record, access_link=None):
        """ The locals_count should include the parameters """
        self = jit.hint(self, access_directly=True, fresh_virtualizable=True)

        self._stack = [None] * (temp_size)
        self._stack_pointer = 0

        self.previous_record = previous_record
        self.access_link = access_link

        self._locals = locals
        self._literals = literals
        self._set_up_local_methods()

    def _set_up_local_methods(self):
        from wlvlang.interpreter.objectspace.method import Method
        for i in range(0, len(self._locals)):
            if isinstance(self._locals[i], Method):
                self._locals[i] = self._locals[i].copy()

                # Since literal methods exist in methods that have been
                # invoked we set the activation record
                self._locals[i].set_enclosing_arec(self)

    def get_previous_record(self):
        """ Get the previous activation record. """
        return self.previous_record;

    def get_access_link(self):
        """ Get the access link for this object (if it has one).  Returns None if it does not """
        return self.access_link;

    def get_element_at(self, index):
        """ Get the element at a specific index in the arec stack """
        assert index < len(self._stack) and index >= 0
        return  self._stack[index]

    def set_element_at(self, index, value):
        assert index < len(self._stack) and index >= 0
        self._stack[index] = value

    def is_root_record(self):
        return self.get_previous_record() == None

    def push(self, value):
        """ Push an object onto the stack """
        self._stack[self._stack_pointer] = value
        self._stack_pointer = self._stack_pointer + 1

    def pop(self):
        """ Pop an object off of the stack """
        assert self._stack_pointer > 0
        self._stack_pointer = self._stack_pointer - 1
        return self._stack[self._stack_pointer]

    def peek(self):
        """ Peek at the object on top of the stack. """
        return self._stack[self._stack_pointer - 1]

    def get_literal_at(self, index):
        assert index < len(self._literals) and index >= 0
        return self._literals[index]

    def get_local_at(self, index):
        assert index < len(self._locals) and index >= 0
        return self._locals[index]

    def set_local_at(self, index, value):
        assert index < len(self._locals) and index >= 0
        self._locals[index] = value

    def _get_arec_at_level(self, level):
        i = 1
        arec = self.get_access_link()
        while i is not level:
            arec = arec.get_access_link()
            i += 1

        return arec

    def get_dynamic_at(self, index, level):
        index = jit.hint(index, promote=True)
        level = jit.hint(level, promote=True)

        arec = self._get_arec_at_level(level)
        if arec:
            return arec.get_local_at(index)

        return None

    def set_dynamic_at(self, index, level, value):
        index = jit.hint(index, promote=True)
        level = jit.hint(level, promote=True)
        value = jit.hint(value, promote=True)

        i = 1
        arec = self._get_arec_at_level(level)
        return arec.set_local_at(index, value)
