
class ActivationRecord(object):
    """
        Defines an Activation Record.

        The shape of the stack is as follows, where the top of the stack is
        the lowest item in the diagram (keeping to the same convention as
        "The Dragon Book" (Compilers: Principles, Techniques and Tools -
        Aho, Lam Sethi and Ullman 2014 (International Ed.)

        |------------------|
        | Caller Record    |
        | aka Control Link |
        --------------------
        | Parameters       |
        |------------------|
        | Return Vals      |
        |------------------|
        | Access Link      |
        |------------------|
        | Machine Status   |
        |------------------|
        | Local Data       |
        |------------------|
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

        Machine Status: Contains machine state that may need to be restored after
                        a method has completed.

        Local Data:  Contains local constant data that is to be used during the execution of the
                    method.

        Temporaries: Contains any temporary variables that may need to be allocated and used
                     during the execution of the procedure.

    """

    _immutable_fields_ = ["_stack"]

    def __init__(self, locals_count, previous_record):
        """ The locals_count should include the parameters """

        # TODO: Not sure this stack will be useful initialised like this
        # pretty sure I'll need to initialise with an object type from the
        # runtime's object space.
        self._stack = [None] * (locals_count + 1)
        self._stack_pointer = 0
        self.push(previous_record)

    def get_previous_record(self):
        """ Get the previous activation record.
            See Activation Recrord layout for
            explanation as to why the index is always 0
        """
        return self._stack[0];

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
