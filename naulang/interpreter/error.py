import os
from naulang.interpreter.bytecode import bytecode_names


class NauRuntimeError(Exception):

    def __init__(self, message, method=None, pc=-1, frame=None):
        self.message = message
        self.method = method
        self.pc = pc
        self.frame = frame

    def getsourceposition(self):
        if self.method is not None and self.method.sourcemap is not None:
            return self.method.sourcemap.get(self.pc)
        return None

    def getbytecodename(self):
        if self.method is not None:
            return bytecode_names[self.method.get_bytecode(self.pc)]
        return "Bytecode name unavailable"


class ErrorDisplay:

    def __init__(self, source):
        self.source = source

    def handle_runtimeerror(self, runtimeerror):
        assert isinstance(runtimeerror, NauRuntimeError)
        self._print_error_message(runtimeerror.message, runtimeerror.getsourceposition(), error_type="Runtime Error")

    def handle_compilererror(self, compilererror):
        self._print_error_message(compilererror.message, compilererror.getsourcepos(), error_type="Compilation Error")

    def handle_error(self, message, source_position, etype):
        self._print_error_message(message, source_position, etype)

    def _print_error_message(self, message, source_position, error_type="Syntax Error"):
        lines = self.source.splitlines()
        if source_position is not None:
            lineno = source_position.lineno
            colno = source_position.colno
        else:
            lineno = 0
            colno = 0

        os.write(2, lines[lineno - 1] + "\n")

        for i in range(0, colno - 1):
            os.write(2, " ")
        os.write(2, "^\n")

        os.write(2, "%s on line %d, column %d: %s\n" % (error_type, lineno, colno, message))
