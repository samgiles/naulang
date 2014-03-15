from wlvlang.interpreter.objectspace.method import Method
from wlvlang.interpreter.bytecode import Bytecode, get_stack_effect, stack_effect_depends_on_args, get_bytecode_length

class FunctionCompilerContext(object):
    """ Context used for compiling a function """
    REGISTER_DYNAMIC_FAILED = -1

    def __init__(self, object_space, outer=None, optimiser=None):
        self.space = object_space
        self.literals = []
        self.locals = []
        self.parameter_count = 0
        self.bytecode = []
        self.outer = outer
        self.id_to_number = {}
        self.inner_contexts = []

        self.labels = []

        # A stack, the top contains a 2-tuple of current labels for the
        # current loop value 1 being the label for the top of the loop (pre-condition)
        # value 2 being the label for the block after the loop.
        self.loop_control = []

        self.optimiser = optimiser

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
        self.labels.append(initial_value)
        return len(self.labels) - 1

    def set_label(self, label, value):
        """
            Updates the value of a label

            Arguments:
            label -- The label number to update (should be an integer)
            value -- The value to assign to this label (should be an integer)
        """
        self.labels[label] = value

    def get_label_value(self, label):
        """
            Returns the value of a label

            Arguments:
            label -- The label number to retrieve (expects an integer)
        """
        return self.labels[label]

    def push_loop_control(self, label_start, label_end):
        """
            Pushes the label representing the top of the loop and the tail of the loop to the loop control stack.

            This is useful for implementing statements such as 'break' and 'continue'

            Arguments:
            label_start -- The Label representing the start of the loop
            label_end   -- The label representing the end of the loop
        """
        self.loop_control.append((label_start, label_end))

    def peek_loop_control(self):
        """
            Returns the current loop control 2-tuple
        """
        return self.loop_control[len(self.loop_control) - 1]

    def pop_loop_control(self):
        """
            Returns the current loop control 2-tuple and removes it from the stack.
        """
        return self.loop_control.pop()

    def add_inner_context(self, context):
        """
            Add an inner function context to this context.
        """
        self.inner_contexts.append(context)

    def get_inner_contexts(self):
        """
            Get a list of inner function contexts.
        """
        return self.inner_contexts

    def get_outer_context(self):
        """
            Get the context enclosing this function context
        """
        return self.outer

    def objspace(self):
        """
            Get object space
        """
        return self.space

    def generate_method(self):
        """
            Generate a method object from this function context.
        """

        # First replace bytecode labels with actual values
        bytecode = self.get_bytecode()

        if self.optimiser is not None:
            bytecode = self.optimiser.optimise(bytecode)

        stack_depth = self._calculate_stack_depth(bytecode)

        # finalize locals and literals
        literals = [None] * len(self.literals)
        locals = [None] * len(self.locals)

        for i in range(0, len(literals)):
            literals[i] = self.literals[i]

        return Method(literals, len(locals), bytecode, stack_depth, argument_count=self.parameter_count)

    def _calculate_stack_depth(self, finalized_bytecode):
        max_depth = 0
        depth = 0
        i = 0
        while i < len(finalized_bytecode):
            bc = finalized_bytecode[i]

            if stack_effect_depends_on_args(bc):
                # HACK: It's difficult to find the arguments of a dynamically
                # loaded method therefore the arguments consumed by this
                # argument are assumed to be none.  Having a slightly larger
                # stack size than necessary shouldn't have a huge effect on
                # performance although not ideal.
                # Adding one for the return value
                depth += 1
            else:
                depth += get_stack_effect(bc)


            if depth > max_depth:
                max_depth = depth

            i += get_bytecode_length(bc)

        return max_depth


    def get_bytecode(self):
        """
            Get the bytecode representation of this function context with any optimisations or
            label applications applied.
        """
        return self._add_labels(self.bytecode)


    def set_outer(self, outer_context):
        """
            Set the outer context of this function context
        """
        self.outer = outer_context

    def set_parameter_count(self, value):
        """
            Set the number of arguments this function takes
        """
        self.parameter_count = value

    def get_parameter_count(self):
        """
            Get the parameter count
        """
        return self.parameter_count

    def register_dynamic(self, identifier):
        """
            Register lookup of a non local scoped variable
        """

        if self.outer is None:
            return self.REGISTER_DYNAMIC_FAILED, 0

        outer_context = self.outer
        level = 1
        while outer_context is not None:
            if outer_context.has_local(identifier):
                return outer_context.register_local(identifier), level

            outer_context = outer_context.outer
            level += 1

        return self.REGISTER_DYNAMIC_FAILED, 0

    def register_local(self, identifier):
        """ Register a local variable in this method context
        and retrieve an offset that will be used in the stack
        to retrieve this variables value. """
        if identifier in self.id_to_number:
            return self.id_to_number[identifier]

        # If we don't have a mapping for this identifier yet create one
        # and create some space in the _locals list for it
        num = len(self.locals)
        self.id_to_number[identifier] = num
        self.locals.append(None)
        return num

    def has_local(self, identifier):
        """ Get whether this function context has the identifier registered """
        if identifier in self.id_to_number:
            return True

        return False

    def register_literal(self, constant_value):
        """ Register a constant value within this function context """
        if constant_value in self.literals:
            return self.literals.index(constant_value)

        self.literals.append(constant_value)
        return len(self.literals) - 1

    def emit(self, bytecode, argument=-1):
        """ Emit a bytecode into this function context """
        self.bytecode.append(bytecode)

        if argument >= 0:
            self.bytecode.append(argument)

    def _add_labels(self, bytecode):
        """
            Update the bytecode with added labels
        """
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
            elif bytecode[i] == Bytecode.JUMP or bytecode[i] == Bytecode.JUMP_IF_FALSE:

                bytecodes[i + 1] = self.get_label_value(bytecode[i + 1])
                i += 2
            else:
                i += 1

        return bytecodes
