import os

from rply.errors import ParsingError

from wlvlang.compiler.lexer import get_lexer
from wlvlang.compiler.parser import create_parser
from wlvlang.compiler.context import FunctionCompilerContext
from wlvlang.compiler.translator import SyntaxDirectedTranslator

from wlvlang.interpreter.bytecode import Bytecode

from rpython.rlib.streamio import open_file_as_stream


lexer = get_lexer()
parser = create_parser()


def _parse_source(source):
    try:
        t = parser.parse(lexer.lex(source))
    except ParsingError, e:
        source_position = e.getsourcepos()
        lines = source.split("\n")
        print e.message
        print lines[source_position.lineno - 1]

        for i in range(source_position.colno - 1):
            os.write(1, " ")

        os.write(1, "^\n")
        raise e

    return t


def parse_file(filename, object_space, arguments=[]):
    """ Given a source file, return a vmobjects.Method object """
    path = os.getcwd()
    fullname = path + os.sep + filename
    try:
        input_file = open_file_as_stream(fullname, "r")
        source = input_file.readall()
        try:
            ast = _parse_source(source)
        except ParsingError, e:
            # TODO: Better errors
            os.write(2, "Failed to parse")
            raise e
        finally:
            input_file.close()
    except OSError, msg:
        os.write(2, "%s: %s\n" % (os.strerror(msg.errno), fullname))
        raise IOError()

    # Set up compilation context
    compiler_context = FunctionCompilerContext(object_space)

    # Add file arguments into 'args' array parameter
    array = object_space.new_array(len(arguments))

    i = len(arguments) - 1
    while i >= 0:
        array.set_value_at(i, object_space.new_string(str(arguments[i])))
        i -= 1

    arg_local = compiler_context.register_local("args")
    compiler_context.locals[arg_local] = array

    # Translate
    sdt = SyntaxDirectedTranslator(compiler_context)
    ast.accept(sdt)

    # Ensure the bytecode is halting
    compiler_context.emit(Bytecode.HALT)

    return compiler_context.generate_method()
