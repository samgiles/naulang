from rply import LexerGenerator

lexer_gen = LexerGenerator()

lexer_gen.ignore(r"([\s\f\t\n\r\v]+)|#.*$")

def get_tokens():
    return [
        # Keywords
        ("IF", r"if\b"),
        ("PRINT", r"print\b"),
        ("FN", r"fn\b"),
        ("WHILE", r"while\b"),
        ("RETURN", r"return\b"),
        ("LET", r"let\b"),
        ("BREAK", r"break\b"),
        ("CONTINUE", r"continue\b"),
        ("ASYNC", r"async\b"),
        # Channel Operators
        ("CHAN_OUT", r"<:"),
        ("CHAN_IN", r"<-"),
        # Arithmetic Operators
        ("MUL", r"\*"),
        ("DIV", r"/"),
        ("MOD", r"%"),
        ("PLUS", r"\+"),
        ("MINUS", r"-"),
        # Logical Operators
        ("AND", r"and\b"),
        ("OR", r"or\b"),
        ("NOT", r"not\b"),
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
        ("TRUE", r"true\b"),
        ("FALSE", r"false\b"),
        ("FLOAT", r"(((0|[1-9][0-9]*)(\.[0-9]*)+)|(\.[0-9]+))([eE][\+\-]?[0-9]*)?"),
        ("INTEGER", r"-?(0|[1-9][0-9]*)"),
        ("STRING", r"\"([^\"\\]|\\.)*\""),
        ("IDENTIFIER", r"[a-zA-Z_$][a-zA-Z_0-9]*"),
        # Others
        ("EQUAL", r"="),
    ]

tokens = get_tokens()

for token in tokens:
    lexer_gen.add(token[0], token[1])

LEXER = lexer_gen.build()

def get_lexer():
    return LEXER
