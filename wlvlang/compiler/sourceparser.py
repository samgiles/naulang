import py

from rpython.rlib.parsing.ebnfparse import parse_ebnf, check_for_missing_names
from rpython.rlib.parsing.parsing import ParseError, PackratParser

from rpython.rlib.objectmodel import we_are_translated

from wlvlang.compiler import compilerdir
from wlvlang.compiler.parser import create_parser, create_lexer


lexer = create_lexer()
parser = create_parser()

def _parse(source):
    return parser.parse(lexer.lex(source))


def parse(source):
    """ Parse the source code and produce an AST """
    t = _parse(source)
    return t

def debug_parse(source):
    t = _parse(source)
    return transformer.dispatch(ToAST().transform(t))
