from rply import LexerGenerator

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
        ("LET", r"let"),
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
        ("LBRACK", r"\["),
        ("RBRACK", r"\]"),
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

LEXER = lg.build()

def get_lexer():
    return LEXER
