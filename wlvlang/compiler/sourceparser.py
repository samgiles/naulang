import py

from wlvlang.compiler.parser import create_parser, create_lexer


lexer = create_lexer()
parser = create_parser()

def _parse(source):
    return parser.parse(lexer.lex(source))


def parse(source):
    """ Parse the source code and produce an AST """
    t = _parse(source)
    return t
