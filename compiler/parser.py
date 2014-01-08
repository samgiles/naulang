import py

from rpython.rlib.parsing.lexer import Lexer, DummyLexer
from rpython.rlib.parsing.regexparse import parse_regex
from rpython.rlib.parsing.parsing import PackratParser, Rule, ParseError
from rpython.rlib.parsing.ebnfparse import parse_ebnf
from rpython.rlib.parsing.deterministic import DFA
from rpython.rlib.parsing.tree import Nonterminal, Symbol, RPythonVisitor

def make_regular_expressions():
        regexes = [

            ("INTEGER", parse_regex("([0-9]*)")),
            ("FLOAT", parse_regex("(0|[1-9][0-9]?)*(\.)?([0-9]+)([eE][-+]?[0-9]+)?")),
            ("STRING", parse_regex('"[^"\\\]*(\\.[^"\\\]*)*"')),

            # Ignore whitespace and comments, python style '# comments'
            ("IGNORE", parse_regex("([\\n\\t\\r\\s])|(#[^\\n]*)")),
            ("LET", parse_regex("let")),
            ("IF", parse_regex("if")),
            ("ELSE", parse_regex("else")),
            ("WHILE", parse_regex("while")),
            ("BOOLEAN", parse_regex("(true|false)")),
            ("L_PAREN", parse_regex("\(")),
            ("R_PAREN", parse_regex("\)")),
            ("L_BRACE", parse_regex("{")),
            ("R_BRACE", parse_regex("}")),
            ("DOT", parse_regex("\.")),
            ("COMMA", parse_regex(",")),
            ("RETURN", parse_regex("return")),

            ("MINUS", parse_regex("-")),
            ("PLUS", parse_regex("\+")),

            ("DOUBLE_EQ", parse_regex("==")),
            ("SINGLE_EQ", parse_regex("=")),
            ("LT", parse_regex("<")),
            ("GT", parse_regex(">")),
            ("OR", parse_regex("or")),
            ("AND", parse_regex("and")),
            ("DIV", parse_regex("/")),
            ("MUL", parse_regex("\*")),
            ("NOT", parse_regex("not")),
            ("MOD", parse_regex("%")),
            ("NEQ", parse_regex("!=")),

            ("ATOM", parse_regex("[a-z@][0-9a-zA-Z_@]*")),

        ]
        return zip(*regexes)

def make_parser(ebnf):
    names, regular_expressions = make_regular_expressions()
    rs, rules, transformer = parse_ebnf(ebnf)
    namelist = list(names)
    regexlist = list(regular_expressions)

    if len(rs) > 0:
        names2, regular_expressions2 = zip(*rs)
        regexlist = regexlist + list(regular_expressions2)
        namelist = namelist + list(names2)

    lexer = Lexer(regexlist, namelist, ignore=["IGNORE"])
    parser = PackratParser(rules, 'module')
    return parser, lexer, transformer

def make_all(ebnf):
	parser, lexer, transformer = make_parser(ebnf)
	return lexer, parser, transformer

def parse_wlvlang(module):

    # Tokenise the input stream (module is simply a string)
    tokens = lexer.tokenize(module, True)

    # Parse the token stream with the parser
    s = parser.parse(tokens)
    return s


# generated code between this line and it's other occurrence
# generated code between this line and it's other occurrence

if __name__ == '__main__':
    f = py.path.local(__file__)
    ebnff = py.path.local("grammar.txt")
    ebnf = ebnff.read()
    oldcontent = f.read()
    s = "# GENERATED CODE BETWEEN THIS LINE AND IT'S OTHER OCCURRENCE\n".lower()
    pre, gen, after = oldcontent.split(s)

    try:
        lexer, parser, transformer = make_all(ebnf)
        transformer = transformer.source
        newcontent = ("%s%s%s\nparser = %r\n\n%s\n\n%s%s"
                      % (pre, s,transformer.replace("ToAST", "SLANGToAST"), parser, lexer.get_dummy_repr(), s, after, ))
        f.write(newcontent)
        print "success"
    except ParseError, e:
        print e.nice_error_message(filename="slang_grammar.txt", source=ebnf)
