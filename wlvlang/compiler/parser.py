from rply import ParserGenerator, LexerGenerator
from rply.errors import LexingError

from wlvlang.compiler import ast

lg = LexerGenerator()

lg.ignore('([\s\f\t\n\r\v]+)|#.*$')

def get_tokens():
    return [
        # Arithmetic Operators
        ("PLUS", r"\+"),
        # Logical Operators
        ("AND", r"and"),
        ("OR", r"or"),
        ("TRUE", r"true"),
        ("FALSE", r"false"),
    ]

tokens = get_tokens()

for token in tokens:
    lg.add(token[0], token[1])

lexer = lg.build()

tokentypes, _ = zip(*get_tokens())

pg = ParserGenerator(tokentypes,
                     precedence=[
                         ("left", ["OR", "AND"]),
                         ("left", ["PLUS"]),
                     ], cache_id="wlvlang-parser-test")

@pg.production("main : expression")
def main(p):
    return p[0]

@pg.production("expression : TRUE")
@pg.production("expression : FALSE")
def expression_literal_bool(p):
    if p[0].gettokentype() == "TRUE":
        return ast.BooleanConstant(True)

    return ast.BooleanConstant(False)

@pg.production("expression : expression AND expression")
def expression_and(p):
    return ast.And(p[0], p[2])

@pg.production("expression : expression OR expression")
def expression_or(p):
    return ast.Or(p[0], p[2])

@pg.production("expression : expression PLUS expression")
def expression_plus(p):
    return ast.AddOp(p[0], p[2])

@pg.error
def error_handler(token):
    raise ValueError("Ran into a %s where it was't expected" % token.gettokentype())

def create_parser():
    return pg.build()

def create_lexer():
    return lg.build()
