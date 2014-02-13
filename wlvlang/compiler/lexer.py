from rply import LexerGenerator

lg = LexerGenerator()


lg.ignore('([\s\f\t\n\r\v]+)|(//[^\n]*\n)|(/\*([^\*]|\*[^/])*\*?\*/)')

def get_tokens():
    return [
        ("LET", r"let"),
        ("SINGLE_EQ", r"eq"),
        ("IF", r"if"),
        ("ELSE", r"else"),
        ("WHILE", r"while"),
        ("RETURN", r"return"),
        ("TRUE", r"true"),
        ("FALSE", r"false"),
        ("INTEGER", r"-?0|[1-9][0-9]*"),
        ("FLOAT",r"(((0|[1-9][0-9]*)(\.[0-9]*)?)|(\.[0-9]+))([eE][\+\-]?[0-9]*)?"),
        ("SINGLE_STRING", r"'([^'\\]|\\.)*'"),
        ("DOUBLE_STRING", r"\"([^\"\\]|\\.)*\""),
        ("SELF", r"self"),
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
        ("IDENTIFIER", r"[a-zA-Z_$][a-zA-Z_0-9]*"),
        ("FN", r"fn"),
        ("LBRACE", r"\{"),
        ("RBRACE", r"\}"),
        ("COMMA", r","),
        ("DOT", r"\."),
        ("PLUS", r"\+"),
        ("MINUS", r"-"),
        ("MUL", r"\*"),
        ("DIV", r"/"),
        ("MOD", r"%"),
        ("CHAN_IN", r"<\+"),
        ("CHAN_OUT", r"<-"),
        ("IS", r"is"),
        ("DOUBLE_EQ", "=="),
        ("NOT_EQ", "!="),
        ("LT", r"<"),
        ("GT", r">"),
        ("LTEQ", r"<="),
        ("GTEQ", r">="),
        ("BANG", r"!"),
        ("PRINT", r"print"),
        ("AND", r"and"),
        ("OR", r"or"),
        ("NOT", r"not"),
        ("IS", r"is"),
    ]

tokens = get_tokens()

for token in tokens:
    lg.add(token[0], token[1])

def create_lexer():
    return lg.build()
