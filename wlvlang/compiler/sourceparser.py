import py

from rpython.rlib.parsing.ebnfparse import parse_ebnf, check_for_missing_names
from rpython.rlib.parsing.parsing import ParseError, PackratParser

from rpython.rlib.objectmodel import we_are_translated

from wlvlang.compiler import compilerdir
from wlvlang.compiler.ast import Transformer

USE_RPLY = True

if USE_RPLY:
    from wlvlang.compiler.parser import create_parser, create_lexer
    lexer = create_lexer()
    parser = create_parser()
    def _parse(source):
        return parser.parse(lexer.lex(source))

else:
    def make_parse_function(regexs, rules, eof=False):
        from rpython.rlib.parsing.lexer import Lexer
        names, regexs = zip(*regexs)
        if "IGNORE" in names:
            ignore = ["IGNORE"]
        else:
            ignore = []
        check_for_missing_names(names, regexs, rules)
        lexer = Lexer(list(regexs), list(names), ignore=ignore)
        parser = PackratParser(rules, rules[0].nonterminal, check_for_left_recursion=False)
        def parse(s):
            tokens = lexer.tokenize(s, eof=eof)
            s = parser.parse(tokens)
            if not we_are_translated():
                try:
                    if py.test.config.option.view:
                        s.view()
                except AttributeError:
                    pass

            return s
        return parse


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
    t = _parse(source)
    return t

def debug_parse(source):
    t = _parse(source)
    return transformer.dispatch(ToAST().transform(t))
