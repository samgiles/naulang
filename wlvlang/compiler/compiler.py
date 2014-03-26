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


def _print_syntax_error_message(message, source_position, source):
    lineno = source_position.lineno
    colno = source_position.colno
    lines = source.splitlines()

    os.write(2, lines[lineno - 1] + "\n")

    for i in range(0, colno - 1):
        os.write(2, " ")
    os.write(2, "^\n")

    os.write(2, "Syntax Error on line %d, column %d: %s\n" % (lineno, colno, message))

def parse(source):
    return parser.parse(lexer.lex(source))

def compile_file_with_arguments(filename, object_space, command_line_arguments=[]):
    path = os.getcwd()
    fullname = path + os.sep + filename
    try:
        input_file = open_file_as_stream(fullname, "r")
        source = input_file.readall()
        try:
            ast = parse(source)
        except ParsingError, e:
            _print_syntax_error_message(e.message, e.getsourcepos(), source)
            raise e
        finally:
            input_file.close()
    except OSError, msg:
        os.write(2, "%s: %s\n" % (os.strerror(msg.errno), fullname))
        raise IOError()

    # Set up compilation context
    compiler_context = FunctionCompilerContext(object_space)

    # Add file arguments into 'args' array parameter
    array = object_space.new_array(len(command_line_arguments))

    i = len(command_line_arguments) - 1
    while i >= 0:
        array.set_value_at(i, object_space.new_string(str(command_line_arguments[i])))
        i -= 1

    arg_local = compiler_context.register_local("args")

    # Translate
    sdt = SyntaxDirectedTranslator(compiler_context)
    ast.accept(sdt)

    # Ensure the bytecode is halting
    compiler_context.emit(Bytecode.HALT)

    return compiler_context.generate_method(), arg_local, array
