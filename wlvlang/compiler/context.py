from wlvlang.vmobjects.method import Method
class MethodCompilerContext(object):

    def __init__(self, vm_universe, outer=None):
        self._universe = vm_universe
        self._registered_constants = []
        self._arguments = []
        self._literals = []
        self._locals = []
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
        return Method(self._literals, self._locals, self.bytecode)

    def set_outer(self, outer_context):
        self._outer = outer_context

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

    # TODO: Issues with access links and scopes will arise here at some point

    def has_local(self, identifier):
        if identifier in self._id_to_number:
            return True

        if self._outer == None:
            return False

        return self._outer.has_local()


    def register_literal(self, constant_value):
        """ Register a constant value """
        self._literals.append(constant_value)
        return len(self._literals)

    def emit(self, bytecode, argument=None):
        self.bytecode.append(bytecode)

        if argument != None:
            self.bytecode.append(chr(argument))
