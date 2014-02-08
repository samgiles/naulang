import os

from rpython.rlib.streamio import open_file_as_stream
from rpython.rlib.parsing.parsing import ParseError

from wlvlang.compiler.sourceparser import parse
from wlvlang.compiler.context import MethodCompilerContext
from wlvlang.interpreter.bytecode import Bytecode

def compile_source_from_file(path, filename, universe):
    """ Given a source file, return a vmobjects.Method object """
    fullname = path + os.sep + filename
    try:
        input_file = open_file_as_stream(fullname, "r")
        source = input_file.readall()

        try:
            ast = parse(source)
        except ParseError, e:
            os.write(2, e.nice_error_message(filename=fullname, source=source))
            # Raise something less specific here (as we output)
            raise e
        finally:
            input_file.close()
    except OSError, msg:
        os.write(2, "%s: %s\n" % (os.strerror(msg.errno), fullname))
        raise IOError()

    compiler_context = MethodCompilerContext(universe)
    ast.compile(compiler_context)
    compiler_context.emit(Bytecode.HALT)
    method = compiler_context.generate_method()
    return method
