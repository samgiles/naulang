from wlvlang.vmobjects.method import Method
from wlvlang.interpreter.bytecode import Bytecode
class MethodCompilerContext(object):

    REGISTER_DYNAMIC_FAILED = -1

    def __init__(self, vm_universe, outer=None):
        self._universe = vm_universe
        self._literals = []
        self._locals = []
        self._parameter_count = 0
        self.bytecode = []
        self._outer = outer
        self._signature = None
        self._id_to_number = {}
        self._inner_contexts = []

        self._labels = []

        # A stack, the top contains a 2-tuple of current labels for the
        # current loop value 1 being the label for the top of the loop (pre-condition)
        # value 2 being the label for the block after the loop.
        self._loop_control = []

    def get_top_position(self):
        """ Returns:
            The position of the last operation, 0 if none
        """
        return len(self.bytecode) - 1

    def add_label(self, initial_value=-1):
        """ Returns:
            A new label.
            Labels are represented by integers.

            Keyword Arguments:
            initial_value -- Set an initial value for this label, default is -1 representing an unassigned label
        """
        self._labels.append(initial_value)
        return len(self._labels) - 1

    def set_label(self, label, value):
        """
            Updates the value of a label

            Arguments:
            label -- The label number to update (should be an integer)
            value -- The value to assign to this label (should be an integer)
        """
        self._labels[label] = value

    def get_label_value(self, label):
        """
            Returns the value of a label

            Arguments:
            label -- The label number to retrieve (expects an integer)
        """
        return self._labels[label]

    def push_loop_control(self, label_start, label_end):
        """
            Pushes the label representing the top of the loop and the tail of the loop to the loop control stack.

            This is useful for implementing statements such as 'break' and 'continue'

            Arguments:
            label_start -- The Label representing the start of the loop
            label_end   -- The label representing the end of the loop
        """
        self._loop_control.append((label_start, label_end))

    def peek_loop_control(self):
        """
            Returns the current loop control 2-tuple
        """
        return self._loop_control[len(self._loop_control) - 1]

    def pop_loop_control(self):
        """
            Returns the current loop control 2-tuple and removes it from the stack.
        """
        return self._loop_control.pop()

    def add_inner_context(self, context):
        self._inner_contexts.append(context)

    def get_inner_contexts(self):
        return self._inner_contexts

    def get_outer_context(self):
        return self._outer

    def universe(self):
        return self._universe

    def generate_method(self):
        # First replace bytecode labels with actual values

        return Method(self._signature, self._literals, self._locals, self.get_bytecode(), argument_count=self._parameter_count)

    def get_bytecode(self):
        return self._add_labels(self.bytecode)

    def _add_labels(self, bytecode):
        bytecodes = [0] * len(bytecode)
        i = 0
        while i < len(self.bytecode):
            bytecodes[i] = self.bytecode[i]

            if  bytecode[i] == Bytecode.LOAD_CONST or bytecode[i] == Bytecode.STORE or bytecode[i] == Bytecode.LOAD  or bytecode[i] == Bytecode.INVOKE or bytecode[i] == Bytecode.INVOKE_GLOBAL:
                i += 1
                bytecodes[i] = bytecode[i]
                i += 1
            elif bytecode[i] == Bytecode.LOAD_DYNAMIC or bytecode[i] == Bytecode.STORE_DYNAMIC:
                i += 1
                bytecodes[i] = bytecode[i]
                i += 1
                bytecodes[i] = bytecode[i]
                i += 1
            elif bytecode[i] == Bytecode.JUMP_BACK or bytecode[i] == Bytecode.JUMP_IF_FALSE:

                bytecodes[i + 1] = self.get_label_value(bytecode[i + 1])
                i += 2
            else:
                i += 1

        return bytecodes

    def set_outer(self, outer_context):
        self._outer = outer_context

    def set_parameter_count(self, value):
        self._parameter_count = value

    def get_parameter_count(self):
        return self._parameter_count

    def register_dynamic(self, identifier):
        """ Register lookup of a non local scoped variable """

        if self._outer is None:
            return self.REGISTER_DYNAMIC_FAILED, 0

        outer_context = self._outer
        level = 1
        while outer_context is not None:
            if outer_context.has_local(identifier):
                return outer_context.register_local(identifier), level

            outer_context = outer_context._outer
            level += 1

        return self.REGISTER_DYNAMIC_FAILED, 0

    def register_local(self, identifier):
        """ Register a local variable in this method context
        and retrieve an offset that will be used in the stack
        to retrieve this variables value. """
        if identifier in self._id_to_number:
            return self._id_to_number[identifier]

        # If we don't have a mapping for this identifier yet create one
        # and create some space in the _locals list for it
        num = len(self._locals)
        self._id_to_number[identifier] = num
        self._locals.append(None)
        return num

    def has_local(self, identifier):
        if identifier in self._id_to_number:
            return True

        return False

    def register_literal(self, constant_value):
        """ Register a constant value """
        if constant_value in self._literals:
            return self._literals.index(constant_value)

        self._literals.append(constant_value)
        return len(self._literals) - 1

    def emit(self, bytecode, argument=-1):
        self.bytecode.append(bytecode)

        if argument >= 0:
            self.bytecode.append(argument)
