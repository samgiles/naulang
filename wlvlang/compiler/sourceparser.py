import py
from rpython.rlib.parsing.ebnfparse import parse_ebnf, make_parse_function
from rpython.rlib.parsing.parsing import ParseError
from wlvlang.compiler import compilerdir
from wlvlang.compiler.ast import Transformer

grammar = py.path.local(compilerdir).join('grammar.ebnf').read("rt")
try:
    regexes, rules, ToAST = parse_ebnf(grammar)
    _parse = make_parse_function(regexes, rules, eof=True)
except ParseError, e:
   print e.nice_error_message(filename="grammar.ebnf", source=grammar)
   raise e


transformer = Transformer()

def parse(source):
    """ Parse the source code and produce an AST """
    result = None
    try:
        result =  transformer.visit_program(_parse(source))
    except ParseError, e:
        print e.nice_error_message(source=source)
        raise e

    return result
