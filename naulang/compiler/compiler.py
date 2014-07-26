import os

from rply.errors import ParsingError

from naulang.compiler.lexer import get_lexer
from naulang.compiler.parser import create_parser
from naulang.compiler.context import FunctionCompilerContext
from naulang.compiler.translator import SyntaxDirectedTranslator
from naulang.compiler.error import CompilerException

from naulang.interpreter.bytecode import Bytecode
from naulang.interpreter.error import NauRuntimeError

from rpython.rlib.streamio import open_file_as_stream


lexer = get_lexer()
parser = create_parser()


def parse(source):
    return parser.parse(lexer.lex(source))


def compile_file_with_arguments(filename, object_space, error_displayer, command_line_arguments=[]):

    source, ast = _parse_file(filename, error_displayer)

    compiler_context = FunctionCompilerContext(object_space, optimise=True)
    arguments_array = _create_commandline_arguments_array(object_space, command_line_arguments)
    arguments_local_offset = _register_symbol_in_compiler_context(compiler_context, symbol="args")

    try:
        translator = SyntaxDirectedTranslator(compiler_context)
        ast.accept(translator)
    except CompilerException as e:
        error_displayer.handle_compilererror(e)
        raise e
    except NauRuntimeError as e:
        error_displayer.handle_runtimeerror(e)
        raise e

    # Ensure the bytecode is halting
    compiler_context.emit([Bytecode.HALT])

    return compiler_context.generate_method(), arguments_local_offset, arguments_array


def _parse_file(filename, error_displayer):
    path = os.getcwd()
    fullname = path + os.sep + filename
    try:
        input_file = open_file_as_stream(fullname, "r")
        source = input_file.readall()
        error_displayer.source = source
        try:
            ast = parse(source)
        except ParsingError as e:
            error_displayer.handle_error(e.message, e.getsourcepos(), "Syntax Error")
            raise e
        finally:
            input_file.close()
    except OSError as msg:
        os.write(2, "%s: %s\n" % (os.strerror(msg.errno), fullname))
        raise IOError()
    return source, ast


def _create_commandline_arguments_array(object_space, command_line_arguments=[]):
    argument_array = object_space.new_array(len(command_line_arguments))

    argument_index = len(command_line_arguments) - 1

    while argument_index >= 0:
        argument_array.set_value_at(
            argument_index, object_space.new_string(str(command_line_arguments[argument_index])))
        argument_index -= 1

    return argument_array


def _register_symbol_in_compiler_context(compiler_context, symbol):
    return compiler_context.register_local(symbol)
