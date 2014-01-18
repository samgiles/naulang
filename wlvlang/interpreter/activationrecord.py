
class ActivationRecord(object):

    _immutable_fields_ = ["_stack"]

    def __init__(self, locals_count, previous_record):

        # TODO: Not sure this stack will be useful initialised like this
        # pretty sure I'll need to initialise with an object type from the
        # runtime's object space.
        self._stack = [None] * locals_count
        self._stack_pointer = 0
        self.previous_record = previous_record

    def get_previous_record(self):
        return self.previous_record

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
