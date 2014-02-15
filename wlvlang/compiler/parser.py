from rply import ParserGenerator, LexerGenerator
from rply.errors import LexingError

from wlvlang.compiler import ast

lg = LexerGenerator()

lg.ignore(r"([\s\f\t\n\r\v]+)|#.*$")

def get_tokens():
    return [
        # Keywords
        ("IF", r"if"),
        ("PRINT", r"print"),
        ("FN", r"fn"),
        ("WHILE", r"while"),
        ("RETURN", r"return"),
        # Arithmetic Operators
        ("MUL", r"\*"),
        ("DIV", r"/"),
        ("MOD", r"%"),
        ("PLUS", r"\+"),
        ("MINUS", r"-"),
        ("NEGATE", r"-"),
        # Logical Operators
        ("AND", r"and"),
        ("OR", r"or"),
        ("NOT", r"not"),
        # Comparison Operators
        ("IS", r"is"),
        ("DOUBLE_EQ", r"=="),
        ("NOT_EQ", r"!="),
        # Relational Operators
        ("LTEQ", r"<="),
        ("GTEQ", r">="),
        ("LT", r"<"),
        ("GT", r">"),
        # Punctuation
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
        ("LBRACE", r"{"),
        ("RBRACE", r"}"),
        ("COMMA", r","),
        # Literals
        ("TRUE", r"true"),
        ("FALSE", r"false"),
        ("FLOAT", r"(((0|[1-9][0-9]*)(\.[0-9]*)+)|(\.[0-9]+))([eE][\+\-]?[0-9]*)?"),
        ("INTEGER", r"-?(0|[1-9][0-9]*)"),
        ("IDENTIFIER", r"[a-zA-Z_$][a-zA-Z_0-9]*"),
        # Others
        ("EQUAL", r"="),
    ]

tokens = get_tokens()

for token in tokens:
    lg.add(token[0], token[1])

lexer = lg.build()

tokentypes, _ = zip(*get_tokens())

pg = ParserGenerator(tokentypes,
                     precedence=[
                         ("right", ["UMINUS"]),
                         ("right", ["NEGATE"]),
                         ("left", ["PLUS", "MINUS"]),
                         ("left", ["MUL", "DIV", "MOD"]),
                         ("nonassoc", ["LT", "GT", "LTEQ", "GTEQ"]),
                         ("nonassoc", ["IS", "DOUBLE_EQ"]),
                         ("left", ["OR", "AND"]),
                     ], cache_id="wlvlang-parser-test")

@pg.production("main : statement_block")
def main(p):
    return p[0]

@pg.production("statement_block : statement_block statement")
def statement_list(p):
    if p[0] is None:
        return ast.Block([p[1]])

    return ast.Block(p[0].get_statements() + [p[1]])

@pg.production("statement_block : none")
def statement_list_none(p):
    return p[0]

@pg.production("statement : expression")
def statement_expression(p):
    return p[0]

@pg.production("statement : PRINT expression")
def statement_print(p):
    return ast.PrintStatement(p[1])

@pg.production("statement : RETURN expression")
def statement_return(p):
    return ast.ReturnStatement(p[1])

@pg.production("statement : RETURN none")
def statement_return_none(p):
    return ast.ReturnStatement(p[1])

@pg.production("statement : IF expression LBRACE statement_block RBRACE")
def statement_if(p):
    return ast.IfStatement(p[1], p[3])

@pg.production("statement : WHILE expression LBRACE statement_block RBRACE")
def statement_while(p):
    return ast.WhileStatement(p[1], p[3])

@pg.production("statement : IDENTIFIER EQUAL expression")
def statement_assignment(p):
    return ast.Assignment(p[0].getstr(), p[2])

@pg.production("expression : FN LPAREN parameter_list RPAREN LBRACE statement_block RBRACE")
def expression_function(p):
    return ast.FunctionExpression(p[2], p[5])

@pg.production("expression : IDENTIFIER LPAREN argument_list RPAREN")
def statement_function_invocation(p):
    return ast.FunctionCall(p[0].getstr(), p[2])

@pg.production("expression : FN IDENTIFIER LPAREN parameter_list RPAREN LBRACE statement_block RBRACE")
def statement_function(p):
    return ast.FunctionStatement(p[1].getstr(), p[3], p[6])


@pg.production("argument_list : arg_opt expression comma_elision")
def argument_list(p):
    if p[0] is None:
        return ast.FunctionArgList([p[1]])

    return ast.FunctionArgList(p[0].get_arguments() + [p[1]])

@pg.production("argument_list : none")
def arg_list_none(p):
    return ast.FunctionArgList([])

@pg.production("arg_opt : arg_opt expression COMMA")
def arg_opt(p):
    if p[0] is None:
        return ast.FunctionArgList([p[1]])

    return ast.FunctionArgList(p[0].get_arguments() + [p[1]])

@pg.production("arg_opt : none")
def arg_opt_none(p):
    return p[0]

@pg.production("parameter_list : param_opt IDENTIFIER comma_elision")
def param_list(p):
    if p[0] is None:
        return ast.ParameterList([p[1].getstr()])

    return ast.ParameterList(p[0].get_parameters() + [p[1].getstr()])

@pg.production("parameter_list : none")
def param_list_none(p):
    return ast.ParameterList([])

@pg.production("param_opt : param_opt IDENTIFIER COMMA")
def param_opt(p):
    if p[0] is None:
        return ast.ParameterList([p[1].getstr()])

    return ast.ParameterList(p[0].get_parameters() + [p[1].getstr()])

@pg.production("param_opt : none")
def param_opt_none(p):
    return p[0]

@pg.production("comma_elision : COMMA")
@pg.production("comma_elision : none")
def comma_elision(p):
    return None

@pg.production("expression : INTEGER")
def expression_integer_literal(p):
    return ast.IntegerConstant(int(p[0].getstr()))

@pg.production("expression : FLOAT")
def expression_float_literal(p):
    return ast.FloatConstant(float(p[0].getstr()))

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

@pg.production("expression : expression LT expression")
def expression_lt(p):
    return ast.LessThan(p[0], p[2])

@pg.production("expression : expression GT expression")
def expression_gt(p):
    return ast.GreaterThan(p[0], p[2])

@pg.production("expression : expression LTEQ expression")
def expression_lteq(p):
    return ast.LessThanOrEqual(p[0], p[2])

@pg.production("expression : expression GTEQ expression")
def expression_gteq(p):
    return ast.GreaterThanOrEqual(p[0], p[2])

@pg.production("expression : expression PLUS expression")
def expression_plus(p):
    return ast.AddOp(p[0], p[2])

@pg.production("expression : expression MINUS expression")
def expression_minus(p):
    return ast.SubtractOp(p[0], p[2])

@pg.production("expression : MINUS expression", precedence="UMINUS")
def expression_negate(p):
    return ast.UnaryNegate(p[1])

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

@pg.production("expression : IDENTIFIER")
def expression_identifier(p):
    return ast.IdentifierExpression(p[0].getstr())

@pg.production("none : ")
def none(p):
    return None

@pg.error
def error_handler(token):
    raise Exception("Ran into a %r where it was't expected" % token.getstr())

def create_parser():
    return pg.build()

def create_lexer():
    return lg.build()
