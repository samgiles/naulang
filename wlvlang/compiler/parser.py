from rply import ParserGenerator, LexerGenerator
from rply.errors import LexingError

from wlvlang.compiler import ast

lg = LexerGenerator()

lg.ignore('([\s\f\t\n\r\v]+)|#.*$')

def get_tokens():
    return [
        # Arithmetic Operators
        ("MUL", r"\*"),
        ("DIV", r"/"),
        ("MOD", r"%"),
        ("PLUS", r"\+"),
        ("MINUS", r"-"),
        # Logical Operators
        ("AND", r"and"),
        ("OR", r"or"),
        ("NOT", r"not"),
        # Comparison Operators
        ("IS", r"is"),
        ("DOUBLE_EQ", r"=="),
        ("NOT_EQ", r"!="),
        # Punctuation
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
        # Literals
        ("TRUE", r"true"),
        ("FALSE", r"false"),
        ("INTEGER", r"-?0|[1-9][0-9]*"),
        # Others
        ("PRINT", r"print"),
    ]

tokens = get_tokens()

for token in tokens:
    lg.add(token[0], token[1])

lexer = lg.build()

tokentypes, _ = zip(*get_tokens())

pg = ParserGenerator(tokentypes,
                     precedence=[
                         ("left", ["OR", "AND"]),
                         ("left", ["IS", "DOUBLE_EQ"]),
                         ("left", ["MUL", "DIV", "MOD"]),
                         ("left", ["PLUS", "MINUS"]),
                     ], cache_id="wlvlang-parser-test")

@pg.production("main : expression")
def main(p):
    return ast.Block([p[0]])

@pg.production("statement_list : statement statement_list")
def statement_list(p):
    return p

@pg.production("statement_list : none")
def statement_list_none(p):
    return None

@pg.production("statement : expression")
def statement_expression(p):
    return p[0]

@pg.production("expression : INTEGER")
def expression_integer_literal(p):
    return ast.IntegerConstant(int(p[0]))

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

@pg.production("expression : expression MINUS expression")
def expression_minus(p):
    return ast.SubtractOp(p[0], p[2])

@pg.production("expression : expression MUL expression")
def expression_multiply(p):
    return ast.MulOp(p[0], p[2])

@pg.production("expression : expression DIV expression")
def expression_divide(p):
    return ast.DivOp(p[0], p[2])

@pg.production("expression : expression MOD expression")
def expression_mod(p):
    return ast.ModOp(p[0], p[2])

@pg.production("expression : LPAREN expression RPAREN")
def expression_parens(p):
    return p[0]

@pg.production("expression : NOT expression")
def expression_unary_not(p):
    return ast.UnaryNot(p[1])

@pg.production("expression : expression IS expression")
@pg.production("expression : expression DOUBLE_EQ expression")
def expression_equality(p):
    return ast.Equals(p[0], p[2])

@pg.production("expression : expression NOT_EQ expression")
def expression_notequals(p):
    return ast.NotEquals(p[0], p[2])

@pg.production("statement : PRINT expression")
def statement_print(p):
    return ast.PrintStatement(p[0])

@pg.production("none : ")
def none(p):
    return None

@pg.error
def error_handler(token):
    raise ValueError("Ran into a %s where it was't expected" % token.gettokentype())

def create_parser():
    return pg.build()

def create_lexer():
    return lg.build()
