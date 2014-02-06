class CompilerContext(object):

    def __init__(self):
        self._registered_constants = []
        self.data = []

    def register_constant(self, constant_value):
        """ Register a constant value """
        self._registered_constants.append(constant_value)
        return len(self._registered_constants)

    def emit(self, bytecode, argument=None):
        pass
