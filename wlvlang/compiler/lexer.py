from rply import LexerGenerator

lg = LexerGenerator()

lg.add("LET", r"let")
lg.add("SINGLE_EQ", r"eq")
lg.add("IF", r"if")
lg.add("ELSE", r"else")
lg.add("WHILE", r"while")
lg.add("RETURN", r"return")
lg.add("TRUE", r"true")
lg.add("FALSE", r"false")
lg.add("INTEGER", r"-?0|[1-9][0-9]*")
lg.add("FLOAT",r"(((0|[1-9][0-9]*)(\.[0-9]*)?)|(\.[0-9]+))([eE][\+\-]?[0-9]*)?")
lg.add("SINGLE_STRING", r"'([^'\\]|\\.)*'")
lg.add("DOUBLE_STRING", r"\"([^\"\\]|\\.)*\"")
lg.add("SELF", r"self")
lg.add("LPAREN", r"\(")
lg.add("RPAREN", r"\)")
lg.add("IDENTIFIER_NAME", r"[a-zA-Z_$][a-zA-Z_0-9]*")
lg.add("FN", r"fn")
lg.add("LBRACE", r"\{")
lg.add("RBRACE", r"\}")
lg.add("COMMA", r",")
lg.add("DOT", r"\.")
lg.add("PLUS", r"\+")
lg.add("MINUS", r"-")
lg.add("MUL", r"\*")
lg.add("DIV", r"/")

lg.ignore('([ \f\t\n\r\v]*)|(//[^\n]*\n)|(/\*([^\*]|\*[^/])*\*?\*/)')

lexer = lg.build()

