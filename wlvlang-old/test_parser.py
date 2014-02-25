from rply import ParserGenerator, LexerGenerator
from rply.errors import LexingError

from wlvlang.compiler import ast

lg = LexerGenerator()

lg.ignore('([\s\f\t\n\r\v]+)|#.*$')

lg.add("AND", r"and")
lg.add("OR", r"or")
lg.add("TRUE", r"true")
lg.add("FALSE", r"false")


lexer = lg.build()

pg = ParserGenerator(["AND", "OR", "TRUE", "FALSE"],
                     precedence=[
                         ("left", ["OR", "AND"]),
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

@pg.error
def error_handler(token):
    raise ValueError("Ran into a %s where it was't expected" % token.gettokentype())


parser = pg.build()

try:
    print parser.parse(lexer.lex("true and false or true and false # comment"))
except LexingError, e:
    print e.getsourcepos()
