from wlvlang.vmobjects.object import Object

class ActivationRecord(Object):
    """
        Defines an Activation Record.

        The shape of the stack is as follows, where the top of the stack is
        the lowest item in the diagram (keeping to the same convention as
        "The Dragon Book" (Compilers: Principles, Techniques and Tools -
        Aho, Lam Sethi and Ullman 2014 (International Ed.)

        --------------------
        | Caller Record    |
        | aka Control Link |
        |------------------|
        | Access Link      |
        |------------------|
        | Local Data       |
        |------------------|
        | Literal Data     |
        --------------------
        | Temporaries      |
        --------------------

        Parameters: refer to the parameters used by the calling procedure.
                    NOTE: In register based machines these are often placed
                    in registers for efficiency

        Return Values: Refers to the return value of the function (if there is one)
                        May be placed in a register for efficiency in some machines.

        Control Link:  Refers to the caller.

        Access Link:   Refers to Activation Records that may contain the nested procedure
                    for access to non-local data.

        Local Data:  Contains local constant data that is to be used during the execution of the
                    method.

        Temporaries: Contains any temporary variables that may need to be allocated and used
                     during the execution of the procedure.

    """

    def __init__(self, locals, local_size, literal_size, temp_size, previous_record, access_link=None):
        """ The locals_count should include the parameters """
        from wlvlang.vmobjects.method import Method
        stack_size = (len(locals) + 2)
        self._stack = [None] * (stack_size + temp_size)
        self._stack_pointer = 0
        self.push(previous_record)
        self.push(access_link)

        self._local_offset = 2
        self._literal_offset = 2 + local_size

        # This feels like a massive massive hack
        # Should find another way of setting up the scope
        # For each method
        for i, local in enumerate(locals):
            if isinstance(local, Method):
                local = local.copy()

                # Since literal methods exist in methods that have been
                # invoked we set the activation record
                local.set_enclosing_arec(self)

            self.push(local)


    def get_previous_record(self):
        """ Get the previous activation record.
            See Activation Record layout for
            explanation as to why the index is always 0
        """
        return self._stack[0];

    def get_access_link(self):
        """ Get the access link for this object (if it has one).  Returns None if it does not """
        return self._stack[1];

    def get_element_at(self, index):
        """ Get the element at a specific index in the arec stack """
        assert index < len(self._stack)
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
        self._stack_pointer = self._stack_pointer - 1
        return self._stack[self._stack_pointer]

    def peek(self):
        """ Peek at the object on top of the stack. """
        return self._stack[self._stack_pointer - 1]

    def get_literal_at(self, index):
        return self.get_element_at(index + self._literal_offset)

    def get_local_at(self, index):
        return self.get_element_at(index + self._local_offset)

    def set_local_at(self, index, value):
        return self.set_element_at(index + self._local_offset, value)

    def _get_arec_at_level(self, level):
        i = 1
        arec = self.get_access_link()
        while i is not level:
            arec = arec.get_access_link()
            i += 1

        return arec

    def get_dynamic_at(self, index, level):
        arec = self._get_arec_at_level(level)
        if arec:
            return arec.get_local_at(index)

        return None

    def set_dynamic_at(self, index, level, value):
        i = 1
        arec = self._get_arec_at_level(level)
        return arec.set_local_at(index, value)
