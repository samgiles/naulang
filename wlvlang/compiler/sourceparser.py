import py
import os

from rply.errors import ParsingError
from wlvlang.compiler.parser import create_parser, create_lexer


lexer = create_lexer()
parser = create_parser()

def _parse(source):
    return parser.parse(lexer.lex(source))


def parse(source):
    """ Parse the source code and produce an AST """
    try:
        t = _parse(source)
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
