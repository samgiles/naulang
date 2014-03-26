import os

from rply.errors import ParsingError

from wlvlang.compiler.lexer import get_lexer
from wlvlang.compiler.parser import create_parser
from wlvlang.compiler.context import FunctionCompilerContext
from wlvlang.compiler.translator import SyntaxDirectedTranslator
from wlvlang.compiler.error import CompilerException

from wlvlang.interpreter.bytecode import Bytecode

from rpython.rlib.streamio import open_file_as_stream


lexer = get_lexer()
parser = create_parser()


def parse(source):
    return parser.parse(lexer.lex(source))

def compile_file_with_arguments(filename, object_space, command_line_arguments=[]):

    source, ast = _parse_file(filename)

    compiler_context = FunctionCompilerContext(object_space)

    arguments_array        = _create_commandline_arguments_array(object_space, command_line_arguments)
    arguments_local_offset = _register_symbol_in_compiler_context(compiler_context, symbol="args")

    translator = SyntaxDirectedTranslator(compiler_context)

    try:
        ast.accept(translator)
    except CompilerException, e:
        _print_error_message(e.message, e.getsourcepos(), source, error_type="Compilation Error")
        raise e

    # Ensure the bytecode is halting
    compiler_context.emit(Bytecode.HALT)

    return compiler_context.generate_method(), arguments_local_offset, arguments_array

def _parse_file(filename):
    path = os.getcwd()
    fullname = path + os.sep + filename
    try:
        input_file = open_file_as_stream(fullname, "r")
        source = input_file.readall()
        try:
            ast = parse(source)
        except ParsingError, e:
            _print_error_message(e.message, e.getsourcepos(), source, error_type="Syntax Error")
            raise e
        finally:
            input_file.close()
    except OSError, msg:
        os.write(2, "%s: %s\n" % (os.strerror(msg.errno), fullname))
        raise IOError()
    return source, ast

def _create_commandline_arguments_array(object_space, command_line_arguments=[]):
    argument_array = object_space.new_array(len(command_line_arguments))

    argument_index = len(command_line_arguments) - 1

    while argument_index >= 0:
        argument_array.set_value_at(argument_index, object_space.new_string(str(command_line_arguments[argument_index])))
        argument_index -= 1

    return argument_array

def _register_symbol_in_compiler_context(compiler_context, symbol):
    return compiler_context.register_local(symbol)

def _print_error_message(message, source_position, source, error_type="Syntax Error"):
    lineno = source_position.lineno
    colno = source_position.colno
    lines = source.splitlines()

    os.write(2, lines[lineno - 1] + "\n")

    for i in range(0, colno - 1):
        os.write(2, " ")
    os.write(2, "^\n")

    os.write(2, "%s on line %d, column %d: %s\n" % (error_type, lineno, colno, message))
