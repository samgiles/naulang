from wlvlang.vmobjects.method import Method
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

    def add_inner_context(self, context):
        self._inner_contexts.append(context)

    def universe(self):
        return self._universe

    def generate_method(self):
        return Method(self._signature, self._literals, self._locals, self.bytecode, argument_count=self._parameter_count)

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

            outer_countext = outer_context._outer

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
        self._literals.append(constant_value)
        return len(self._literals) - 1

    def emit(self, bytecode, argument=-1):
        self.bytecode.append(bytecode)

        if argument >= 0:
            self.bytecode.append(chr(argument))
