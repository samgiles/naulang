import py
import os

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
            ("FN", parse_regex("fn")),
            ("IF", parse_regex("if")),
            ("ELSE", parse_regex("else")),
            ("WHILE", parse_regex("while")),
            ("BOOLEAN", parse_regex("(true|false)")),
            ("L_PAREN", parse_regex("\(")),
            ("R_PAREN", parse_regex("\)")),
            ("L_BRACE", parse_regex("{")),
            ("R_BRACE", parse_regex("}")),
            ("L_BRACK", parse_regex("\[")),
            ("R_BRACK", parse_regex("\]")),
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

    # Create abstract syntax tree
    s.visit(WLVLANGToAST())
    return s


# generated code between this line and it's other occurrence
class WLVLANGToAST(object):
    def visit_module(self, node):
        #auto-generated code, don't edit
        children = []
        expr = self.visit__plus_symbol0(node.children[0])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit__plus_symbol0(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            children = []
            children.extend(self.visit_declaration(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_declaration(node.children[0]))
        expr = self.visit__plus_symbol0(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_atomic(self, node):
        #auto-generated code, don't edit
        children = []
        children.extend([node.children[0]])
        return [Nonterminal(node.symbol, children)]
    def visit_number(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if node.children[0].symbol == 'FLOAT':
            children = []
            children.extend([node.children[0]])
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend([node.children[0]])
        return [Nonterminal(node.symbol, children)]
    def visit_string(self, node):
        #auto-generated code, don't edit
        children = []
        children.extend([node.children[0]])
        return [Nonterminal(node.symbol, children)]
    def visit_bool(self, node):
        #auto-generated code, don't edit
        children = []
        children.extend([node.children[0]])
        return [Nonterminal(node.symbol, children)]
    def visit__star_symbol0(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 2:
            children = []
            children.extend([node.children[0]])
            children.extend([node.children[1]])
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend([node.children[0]])
        children.extend([node.children[1]])
        expr = self.visit__star_symbol0(node.children[2])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_plainid(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            children = []
            children.extend([node.children[0]])
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend([node.children[0]])
        expr = self.visit__star_symbol0(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_id(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if node.children[0].symbol == 'FLOAT':
            children = []
            children.extend([node.children[0]])
            return [Nonterminal(node.symbol, children)]
        if node.children[0].symbol == 'INTEGER':
            children = []
            children.extend([node.children[0]])
            return [Nonterminal(node.symbol, children)]
        if node.children[0].symbol == 'STRING':
            children = []
            children.extend([node.children[0]])
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_plainid(node.children[0]))
        return [Nonterminal(node.symbol, children)]
    def visit__star_symbol1(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 2:
            children = []
            children.extend([node.children[0]])
            children.extend(self.visit_plainid(node.children[1]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend([node.children[0]])
        children.extend(self.visit_plainid(node.children[1]))
        expr = self.visit__star_symbol1(node.children[2])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_qualifiedid(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            children = []
            children.extend(self.visit_id(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_id(node.children[0]))
        expr = self.visit__star_symbol1(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_identifier(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if node.children[0].symbol == 'bool':
            return self.visit_bool(node.children[0])
        children = []
        children.extend(self.visit_id(node.children[0]))
        return [Nonterminal(node.symbol, children)]
    def visit__star_symbol2(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            children = []
            children.extend(self.visit_blockitem(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_blockitem(node.children[0]))
        expr = self.visit__star_symbol2(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_blockstatement(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 2:
            children = []
            children.extend([node.children[0]])
            children.extend([node.children[1]])
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend([node.children[0]])
        expr = self.visit__star_symbol2(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        children.extend([node.children[2]])
        return [Nonterminal(node.symbol, children)]
    def visit_blockitem(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if node.children[0].symbol == 'declaration':
            return self.visit_declaration(node.children[0])
        children = []
        children.extend(self.visit_statement(node.children[0]))
        return [Nonterminal(node.symbol, children)]
    def visit__maybe_symbol3(self, node):
        #auto-generated code, don't edit
        children = []
        children.extend([node.children[0]])
        children.extend(self.visit_blockstatement(node.children[1]))
        return [Nonterminal(node.symbol, children)]
    def visit__maybe_symbol4(self, node):
        #auto-generated code, don't edit
        children = []
        children.extend(self.visit_expressionroot(node.children[0]))
        return [Nonterminal(node.symbol, children)]
    def visit_statement(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            children = []
            children.extend(self.visit_expressionroot(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        if length == 2:
            children = []
            children.extend([node.children[0]])
            children.extend([node.children[1]])
            return [Nonterminal(node.symbol, children)]
        if length == 3:
            if node.children[0].symbol == 'IF':
                children = []
                children.extend([node.children[0]])
                children.extend(self.visit_expressionroot(node.children[1]))
                children.extend(self.visit_blockstatement(node.children[2]))
                return [Nonterminal(node.symbol, children)]
            if node.children[0].symbol == 'RETURN':
                children = []
                children.extend([node.children[0]])
                expr = self.visit__maybe_symbol4(node.children[1])
                assert len(expr) == 1
                children.extend(expr[0].children)
                children.extend([node.children[2]])
                return [Nonterminal(node.symbol, children)]
            children = []
            children.extend([node.children[0]])
            children.extend(self.visit_expressionroot(node.children[1]))
            children.extend(self.visit_blockstatement(node.children[2]))
            return [Nonterminal(node.symbol, children)]
        if length == 4:
            children = []
            children.extend([node.children[0]])
            children.extend(self.visit_expressionroot(node.children[1]))
            children.extend(self.visit_blockstatement(node.children[2]))
            expr = self.visit__maybe_symbol3(node.children[3])
            assert len(expr) == 1
            children.extend(expr[0].children)
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend([node.children[0]])
        children.extend(self.visit_blockstatement(node.children[1]))
        children.extend([node.children[2]])
        children.extend(self.visit_expressionroot(node.children[3]))
        children.extend([node.children[4]])
        return [Nonterminal(node.symbol, children)]
    def visit_declaration(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 4:
            children = []
            children.extend(self.visit_plainid(node.children[0]))
            children.extend([node.children[1]])
            children.extend(self.visit_expressionroot(node.children[2]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend([node.children[0]])
        children.extend(self.visit_plainid(node.children[1]))
        children.extend([node.children[2]])
        children.extend(self.visit_expressionroot(node.children[3]))
        return [Nonterminal(node.symbol, children)]
    def visit_expressionroot(self, node):
        #auto-generated code, don't edit
        return self.visit_functioncallexpr(node.children[0])
    def visit_functioncallexpr(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            children = []
            children.extend(self.visit_functionexpression(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_functionexpression(node.children[0]))
        children.extend(self.visit_argumentexprlist(node.children[1]))
        return [Nonterminal(node.symbol, children)]
    def visit_functionexpression(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            return self.visit_postfixexpr(node.children[0])
        children = []
        children.extend([node.children[0]])
        children.extend(self.visit_functionparameterlist(node.children[1]))
        children.extend(self.visit_blockstatement(node.children[2]))
        return [Nonterminal(node.symbol, children)]
    def visit__maybe_symbol5(self, node):
        #auto-generated code, don't edit
        children = []
        children.extend([node.children[0]])
        children.extend(self.visit_primaryexpr(node.children[1]))
        return [Nonterminal(node.symbol, children)]
    def visit__maybe_symbol6(self, node):
        #auto-generated code, don't edit
        children = []
        children.extend([node.children[0]])
        children.extend(self.visit_primaryexpr(node.children[1]))
        return [Nonterminal(node.symbol, children)]
    def visit__maybe_symbol7(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 2:
            children = []
            children.extend([node.children[0]])
            children.extend([node.children[1]])
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend([node.children[0]])
        children.extend([node.children[1]])
        expr = self.visit__maybe_symbol6(node.children[2])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit__star_symbol8(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 2:
            children = []
            children.extend([node.children[0]])
            expr = self.visit____star_symbol8_rest_0_0(node.children[1])
            assert len(expr) == 1
            children.extend(expr[0].children)
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend([node.children[0]])
        expr = self.visit__maybe_symbol5(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        expr = self.visit____star_symbol8_rest_0_0(node.children[2])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_functionparameterlist(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 2:
            children = []
            children.extend([node.children[0]])
            children.extend([node.children[1]])
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend([node.children[0]])
        expr = self.visit__star_symbol8(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        children.extend([node.children[2]])
        return [Nonterminal(node.symbol, children)]
    def visit__maybe_symbol9(self, node):
        #auto-generated code, don't edit
        children = []
        children.extend([node.children[0]])
        children.extend([node.children[1]])
        return [Nonterminal(node.symbol, children)]
    def visit__maybe_symbol10(self, node):
        #auto-generated code, don't edit
        children = []
        children.extend([node.children[0]])
        children.extend([node.children[1]])
        return [Nonterminal(node.symbol, children)]
    def visit__star_symbol11(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 2:
            children = []
            children.extend([node.children[0]])
            expr = self.visit____star_symbol11_rest_0_0(node.children[1])
            assert len(expr) == 1
            children.extend(expr[0].children)
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend([node.children[0]])
        expr = self.visit__maybe_symbol10(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        expr = self.visit____star_symbol11_rest_0_0(node.children[2])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit__star_symbol12(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            children = []
            expr = self.visit____star_symbol12_rest_0_0(node.children[0])
            assert len(expr) == 1
            children.extend(expr[0].children)
            return [Nonterminal(node.symbol, children)]
        children = []
        expr = self.visit__maybe_symbol9(node.children[0])
        assert len(expr) == 1
        children.extend(expr[0].children)
        expr = self.visit____star_symbol12_rest_0_0(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_argumentexprlist(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 2:
            children = []
            children.extend([node.children[0]])
            children.extend([node.children[1]])
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend([node.children[0]])
        expr = self.visit__star_symbol12(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        children.extend([node.children[2]])
        return [Nonterminal(node.symbol, children)]
    def visit_postfixexpr(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            return self.visit_unaryexpr(node.children[0])
        children = []
        children.extend(self.visit_unaryexpr(node.children[0]))
        children.extend([node.children[1]])
        children.extend(self.visit_postfixexpr(node.children[2]))
        children.extend([node.children[3]])
        return [Nonterminal(node.symbol, children)]
    def visit_unaryexpr(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            return self.visit_additiveexpr(node.children[0])
        children = []
        children.extend(self.visit_unaryoperator(node.children[0]))
        children.extend(self.visit_additiveexpr(node.children[1]))
        return [Nonterminal(node.symbol, children)]
    def visit_unaryoperator(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if node.children[0].symbol == 'ADD':
            children = []
            children.extend([node.children[0]])
            return [Nonterminal(node.symbol, children)]
        if node.children[0].symbol == 'MINUS':
            children = []
            children.extend([node.children[0]])
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend([node.children[0]])
        return [Nonterminal(node.symbol, children)]
    def visit_additiveexpr(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            return self.visit_multiplicativeexpr(node.children[0])
        if node.children[1].symbol == 'ADD':
            children = []
            children.extend(self.visit_multiplicativeexpr(node.children[0]))
            children.extend([node.children[1]])
            children.extend(self.visit_additiveexpr(node.children[2]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_multiplicativeexpr(node.children[0]))
        children.extend([node.children[1]])
        children.extend(self.visit_additiveexpr(node.children[2]))
        return [Nonterminal(node.symbol, children)]
    def visit_multiplicativeexpr(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            return self.visit_comparisonexpr(node.children[0])
        if node.children[1].symbol == 'DIV':
            children = []
            children.extend(self.visit_comparisonexpr(node.children[0]))
            children.extend([node.children[1]])
            children.extend(self.visit_multiplicativeexpr(node.children[2]))
            return [Nonterminal(node.symbol, children)]
        if node.children[1].symbol == 'MOD':
            children = []
            children.extend(self.visit_comparisonexpr(node.children[0]))
            children.extend([node.children[1]])
            children.extend(self.visit_multiplicativeexpr(node.children[2]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_comparisonexpr(node.children[0]))
        children.extend([node.children[1]])
        children.extend(self.visit_multiplicativeexpr(node.children[2]))
        return [Nonterminal(node.symbol, children)]
    def visit_comparisonexpr(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            return self.visit_equalityexpr(node.children[0])
        if node.children[1].symbol == 'GT':
            children = []
            children.extend(self.visit_equalityexpr(node.children[0]))
            children.extend([node.children[1]])
            children.extend(self.visit_comparisonexpr(node.children[2]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_equalityexpr(node.children[0]))
        children.extend([node.children[1]])
        children.extend(self.visit_comparisonexpr(node.children[2]))
        return [Nonterminal(node.symbol, children)]
    def visit_equalityexpr(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            return self.visit_logicalandexpr(node.children[0])
        if node.children[1].symbol == 'DOUBLE_EQ':
            children = []
            children.extend(self.visit_logicalandexpr(node.children[0]))
            children.extend([node.children[1]])
            children.extend(self.visit_equalityexpr(node.children[2]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_logicalandexpr(node.children[0]))
        children.extend([node.children[1]])
        children.extend(self.visit_equalityexpr(node.children[2]))
        return [Nonterminal(node.symbol, children)]
    def visit_logicalandexpr(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            return self.visit_logicalorexpr(node.children[0])
        children = []
        children.extend(self.visit_logicalorexpr(node.children[0]))
        children.extend([node.children[1]])
        children.extend(self.visit_logicalandexpr(node.children[2]))
        return [Nonterminal(node.symbol, children)]
    def visit_logicalorexpr(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            return self.visit_primaryexpr(node.children[0])
        children = []
        children.extend(self.visit_primaryexpr(node.children[0]))
        children.extend([node.children[1]])
        children.extend(self.visit_logicalorexpr(node.children[2]))
        return [Nonterminal(node.symbol, children)]
    def visit_primaryexpr(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            return self.visit_identifier(node.children[0])
        children = []
        children.extend([node.children[0]])
        children.extend(self.visit_unaryexpr(node.children[1]))
        children.extend([node.children[2]])
        return [Nonterminal(node.symbol, children)]
    def visit____star_symbol8_rest_0_0(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            children = []
            expr = self.visit____star_symbol8_rest_0_1(node.children[0])
            assert len(expr) == 1
            children.extend(expr[0].children)
            return [Nonterminal(node.symbol, children)]
        children = []
        expr = self.visit__maybe_symbol7(node.children[0])
        assert len(expr) == 1
        children.extend(expr[0].children)
        expr = self.visit____star_symbol8_rest_0_1(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit____star_symbol8_rest_0_1(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 0:
            children = []
            return [Nonterminal(node.symbol, children)]
        children = []
        expr = self.visit__star_symbol8(node.children[0])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit____star_symbol11_rest_0_0(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            children = []
            children.extend(self.visit_primaryexpr(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_primaryexpr(node.children[0]))
        expr = self.visit__star_symbol11(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit____star_symbol12_rest_0_0(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 2:
            children = []
            children.extend(self.visit_primaryexpr(node.children[0]))
            expr = self.visit____star_symbol12_rest_0_1(node.children[1])
            assert len(expr) == 1
            children.extend(expr[0].children)
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_primaryexpr(node.children[0]))
        expr = self.visit__star_symbol11(node.children[1])
        assert len(expr) == 1
        children.extend(expr[0].children)
        expr = self.visit____star_symbol12_rest_0_1(node.children[2])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit____star_symbol12_rest_0_1(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 0:
            children = []
            return [Nonterminal(node.symbol, children)]
        children = []
        expr = self.visit__star_symbol12(node.children[0])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def transform(self, tree):
        #auto-generated code, don't edit
        assert isinstance(tree, Nonterminal)
        assert tree.symbol == 'module'
        r = self.visit_module(tree)
        assert len(r) == 1
        if not we_are_translated():
            try:
                if py.test.config.option.view:
                    r[0].view()
            except AttributeError:
                pass
        return r[0]
parser = PackratParser([Rule('module', [['_plus_symbol0', 'EOF']]),
  Rule('_plus_symbol0', [['declaration', '_plus_symbol0'], ['declaration']]),
  Rule('atomic', [['ATOM']]),
  Rule('number', [['FLOAT'], ['INTEGER']]),
  Rule('string', [['STRING']]),
  Rule('bool', [['BOOLEAN']]),
  Rule('_star_symbol0', [['__0_.', 'ATOM', '_star_symbol0'], ['__0_.', 'ATOM']]),
  Rule('plainid', [['ATOM', '_star_symbol0'], ['ATOM']]),
  Rule('id', [['plainid'], ['STRING'], ['FLOAT'], ['INTEGER']]),
  Rule('_star_symbol1', [['DOT', 'plainid', '_star_symbol1'], ['DOT', 'plainid']]),
  Rule('qualifiedid', [['id', '_star_symbol1'], ['id']]),
  Rule('identifier', [['id'], ['bool']]),
  Rule('_star_symbol2', [['blockitem', '_star_symbol2'], ['blockitem']]),
  Rule('blockstatement', [['L_BRACE', '_star_symbol2', 'R_BRACE'], ['L_BRACE', 'R_BRACE']]),
  Rule('blockitem', [['declaration'], ['statement']]),
  Rule('_maybe_symbol3', [['ELSE', 'blockstatement']]),
  Rule('_maybe_symbol4', [['expressionroot']]),
  Rule('statement', [['IF', 'expressionroot', 'blockstatement', '_maybe_symbol3'], ['IF', 'expressionroot', 'blockstatement'], ['WHILE', 'expressionroot', 'blockstatement'], ['__1_do', 'blockstatement', 'WHILE', 'expressionroot', '__2_;'], ['RETURN', '_maybe_symbol4', '__2_;'], ['RETURN', '__2_;'], ['expressionroot']]),
  Rule('declaration', [['LET', 'plainid', 'SINGLE_EQ', 'expressionroot', '__2_;'], ['plainid', 'SINGLE_EQ', 'expressionroot', '__2_;']]),
  Rule('expressionroot', [['functioncallexpr']]),
  Rule('functioncallexpr', [['functionexpression'], ['functionexpression', 'argumentexprlist']]),
  Rule('functionexpression', [['postfixexpr'], ['FN', 'functionparameterlist', 'blockstatement']]),
  Rule('_maybe_symbol5', [['SINGLE_EQ', 'primaryexpr']]),
  Rule('_maybe_symbol6', [['SINGLE_EQ', 'primaryexpr']]),
  Rule('_maybe_symbol7', [['__3_,', 'ATOM', '_maybe_symbol6'], ['__3_,', 'ATOM']]),
  Rule('_star_symbol8', [['ATOM', '_maybe_symbol5', '___star_symbol8_rest_0_0'], ['ATOM', '___star_symbol8_rest_0_0']]),
  Rule('functionparameterlist', [['L_PAREN', '_star_symbol8', 'R_PAREN'], ['L_PAREN', 'R_PAREN']]),
  Rule('_maybe_symbol9', [['ATOM', '__4_=']]),
  Rule('_maybe_symbol10', [['ATOM', '__4_=']]),
  Rule('_star_symbol11', [['__3_,', '_maybe_symbol10', '___star_symbol11_rest_0_0'], ['__3_,', '___star_symbol11_rest_0_0']]),
  Rule('_star_symbol12', [['_maybe_symbol9', '___star_symbol12_rest_0_0'], ['___star_symbol12_rest_0_0']]),
  Rule('argumentexprlist', [['L_PAREN', '_star_symbol12', 'R_PAREN'], ['L_PAREN', 'R_PAREN']]),
  Rule('postfixexpr', [['unaryexpr'], ['unaryexpr', 'L_BRACK', 'postfixexpr', 'R_BRACK']]),
  Rule('unaryexpr', [['unaryoperator', 'additiveexpr'], ['additiveexpr']]),
  Rule('unaryoperator', [['ADD'], ['MINUS'], ['NOT']]),
  Rule('additiveexpr', [['multiplicativeexpr', 'ADD', 'additiveexpr'], ['multiplicativeexpr', 'MINUS', 'additiveexpr'], ['multiplicativeexpr']]),
  Rule('multiplicativeexpr', [['comparisonexpr', 'MUL', 'multiplicativeexpr'], ['comparisonexpr', 'DIV', 'multiplicativeexpr'], ['comparisonexpr', 'MOD', 'multiplicativeexpr'], ['comparisonexpr']]),
  Rule('comparisonexpr', [['equalityexpr', 'LT', 'comparisonexpr'], ['equalityexpr', 'GT', 'comparisonexpr'], ['equalityexpr']]),
  Rule('equalityexpr', [['logicalandexpr', 'DOUBLE_EQ', 'equalityexpr'], ['logicalandexpr', 'NEQ', 'equalityexpr'], ['logicalandexpr']]),
  Rule('logicalandexpr', [['logicalorexpr', 'AND', 'logicalandexpr'], ['logicalorexpr']]),
  Rule('logicalorexpr', [['primaryexpr', 'OR', 'logicalorexpr'], ['primaryexpr']]),
  Rule('primaryexpr', [['identifier'], ['L_PAREN', 'unaryexpr', 'R_PAREN']]),
  Rule('___star_symbol8_rest_0_0', [['_maybe_symbol7', '___star_symbol8_rest_0_1'], ['___star_symbol8_rest_0_1']]),
  Rule('___star_symbol8_rest_0_1', [['_star_symbol8'], []]),
  Rule('___star_symbol11_rest_0_0', [['primaryexpr', '_star_symbol11'], ['primaryexpr']]),
  Rule('___star_symbol12_rest_0_0', [['primaryexpr', '_star_symbol11', '___star_symbol12_rest_0_1'], ['primaryexpr', '___star_symbol12_rest_0_1']]),
  Rule('___star_symbol12_rest_0_1', [['_star_symbol12'], []])],
 'module')

def recognize(runner, i):
    #auto-generated code, don't edit
    assert i >= 0
    input = runner.text
    state = 0
    while 1:
        if state == 0:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 0
                return i
            if char == '\t':
                state = 1
            elif char == '\n':
                state = 1
            elif char == '\x0c':
                state = 1
            elif char == '\r':
                state = 1
            elif char == ' ':
                state = 1
            elif char == '!':
                state = 2
            elif char == '#':
                state = 3
            elif char == '"':
                state = 4
            elif char == '%':
                state = 5
            elif char == ')':
                state = 6
            elif char == '+':
                state = 7
            elif char == '*':
                state = 8
            elif char == '-':
                state = 9
            elif char == ',':
                state = 10
            elif char == '/':
                state = 11
            elif char == '.':
                state = 12
            elif '0' <= char <= '9':
                state = 13
            elif char == ';':
                state = 14
            elif char == '=':
                state = 15
            elif char == '<':
                state = 16
            elif char == '>':
                state = 17
            elif 'x' <= char <= 'z':
                state = 18
            elif char == 'b':
                state = 18
            elif char == 'c':
                state = 18
            elif char == 'g':
                state = 18
            elif char == 'h':
                state = 18
            elif char == 'j':
                state = 18
            elif char == 'k':
                state = 18
            elif char == 'p':
                state = 18
            elif char == 'q':
                state = 18
            elif char == 'u':
                state = 18
            elif char == 'v':
                state = 18
            elif char == '@':
                state = 18
            elif char == 'm':
                state = 18
            elif char == 's':
                state = 18
            elif char == '(':
                state = 19
            elif char == '[':
                state = 20
            elif char == ']':
                state = 21
            elif char == 'a':
                state = 22
            elif char == 'e':
                state = 23
            elif char == 'd':
                state = 24
            elif char == 'f':
                state = 25
            elif char == 'i':
                state = 26
            elif char == 'l':
                state = 27
            elif char == 'o':
                state = 28
            elif char == 'n':
                state = 29
            elif char == 'r':
                state = 30
            elif char == 't':
                state = 31
            elif char == 'w':
                state = 32
            elif char == '{':
                state = 33
            elif char == '}':
                state = 34
            else:
                break
        if state == 2:
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 2
                return ~i
            if char == '=':
                state = 69
            else:
                break
        if state == 3:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 3
                return i
            if '\x0b' <= char <= '\xff':
                state = 3
                continue
            elif '\x00' <= char <= '\t':
                state = 3
                continue
            else:
                break
        if state == 4:
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 4
                return ~i
            if char == '"':
                state = 68
            elif ']' <= char <= '\xff':
                state = 4
                continue
            elif '#' <= char <= '[':
                state = 4
                continue
            elif '\x00' <= char <= '!':
                state = 4
                continue
            else:
                break
        if state == 12:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 12
                return i
            if '0' <= char <= '9':
                state = 65
            else:
                break
        if state == 13:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 13
                return i
            if char == '.':
                state = 64
            elif '0' <= char <= '9':
                state = 13
                continue
            elif char == 'E':
                state = 63
            elif char == 'e':
                state = 63
            else:
                break
        if state == 15:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 15
                return i
            if char == '=':
                state = 62
            else:
                break
        if state == 18:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 18
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            else:
                break
        if state == 22:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 22
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 'm':
                state = 18
                continue
            elif 'o' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            elif char == 'n':
                state = 60
            else:
                break
        if state == 23:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 23
                return i
            if char == 'l':
                state = 57
            elif '@' <= char <= 'Z':
                state = 18
                continue
            elif 'm' <= char <= 'z':
                state = 18
                continue
            elif 'a' <= char <= 'k':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            else:
                break
        if state == 24:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 24
                return i
            if char == 'o':
                state = 56
            elif '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 'n':
                state = 18
                continue
            elif 'p' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            else:
                break
        if state == 25:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 25
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'b' <= char <= 'm':
                state = 18
                continue
            elif 'o' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            elif char == 'a':
                state = 53
            elif char == 'n':
                state = 54
            else:
                break
        if state == 26:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 26
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'g' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif 'a' <= char <= 'e':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            elif char == 'f':
                state = 52
            else:
                break
        if state == 27:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 27
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'f' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif 'a' <= char <= 'd':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            elif char == 'e':
                state = 50
            else:
                break
        if state == 28:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 28
                return i
            if char == 'r':
                state = 49
            elif '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 'q':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif 's' <= char <= 'z':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            else:
                break
        if state == 29:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 29
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 'n':
                state = 18
                continue
            elif 'p' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            elif char == 'o':
                state = 47
            else:
                break
        if state == 30:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 30
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'f' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif 'a' <= char <= 'd':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            elif char == 'e':
                state = 42
            else:
                break
        if state == 31:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 31
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 'q':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif 's' <= char <= 'z':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            elif char == 'r':
                state = 39
            else:
                break
        if state == 32:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 32
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'i' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif 'a' <= char <= 'g':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            elif char == 'h':
                state = 35
            else:
                break
        if state == 35:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 35
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'j' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif 'a' <= char <= 'h':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            elif char == 'i':
                state = 36
            else:
                break
        if state == 36:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 36
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'm' <= char <= 'z':
                state = 18
                continue
            elif 'a' <= char <= 'k':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            elif char == 'l':
                state = 37
            else:
                break
        if state == 37:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 37
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'f' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif 'a' <= char <= 'd':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            elif char == 'e':
                state = 38
            else:
                break
        if state == 38:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 38
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            else:
                break
        if state == 39:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 39
                return i
            if char == 'u':
                state = 40
            elif '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 't':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif 'v' <= char <= 'z':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            else:
                break
        if state == 40:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 40
                return i
            if char == 'e':
                state = 41
            elif '@' <= char <= 'Z':
                state = 18
                continue
            elif 'f' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif 'a' <= char <= 'd':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            else:
                break
        if state == 41:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 41
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            else:
                break
        if state == 42:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 42
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 's':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif 'u' <= char <= 'z':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            elif char == 't':
                state = 43
            else:
                break
        if state == 43:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 43
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 't':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif 'v' <= char <= 'z':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            elif char == 'u':
                state = 44
            else:
                break
        if state == 44:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 44
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 'q':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif 's' <= char <= 'z':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            elif char == 'r':
                state = 45
            else:
                break
        if state == 45:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 45
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 'm':
                state = 18
                continue
            elif 'o' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            elif char == 'n':
                state = 46
            else:
                break
        if state == 46:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 46
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            else:
                break
        if state == 47:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 47
                return i
            if char == 't':
                state = 48
            elif '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 's':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif 'u' <= char <= 'z':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            else:
                break
        if state == 48:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 48
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            else:
                break
        if state == 49:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 49
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            else:
                break
        if state == 50:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 50
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 's':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif 'u' <= char <= 'z':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            elif char == 't':
                state = 51
            else:
                break
        if state == 51:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 51
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            else:
                break
        if state == 52:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 52
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            else:
                break
        if state == 53:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 53
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'm' <= char <= 'z':
                state = 18
                continue
            elif 'a' <= char <= 'k':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            elif char == 'l':
                state = 55
            else:
                break
        if state == 54:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 54
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            else:
                break
        if state == 55:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 55
                return i
            if char == 's':
                state = 40
                continue
            elif '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 'r':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif 't' <= char <= 'z':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            else:
                break
        if state == 56:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 56
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            else:
                break
        if state == 57:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 57
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 'r':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif 't' <= char <= 'z':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            elif char == 's':
                state = 58
            else:
                break
        if state == 58:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 58
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'f' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif 'a' <= char <= 'd':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            elif char == 'e':
                state = 59
            else:
                break
        if state == 59:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 59
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            else:
                break
        if state == 60:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 60
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'e' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif 'a' <= char <= 'c':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            elif char == 'd':
                state = 61
            else:
                break
        if state == 61:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 61
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'a' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            else:
                break
        if state == 63:
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 63
                return ~i
            if char == '+':
                state = 66
            elif char == '-':
                state = 66
            elif '0' <= char <= '9':
                state = 67
            else:
                break
        if state == 64:
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 64
                return ~i
            if '0' <= char <= '9':
                state = 65
            else:
                break
        if state == 65:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 65
                return i
            if '0' <= char <= '9':
                state = 65
                continue
            elif char == 'E':
                state = 63
                continue
            elif char == 'e':
                state = 63
                continue
            else:
                break
        if state == 66:
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 66
                return ~i
            if '0' <= char <= '9':
                state = 67
            else:
                break
        if state == 67:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 67
                return i
            if '0' <= char <= '9':
                state = 67
                continue
            else:
                break
        runner.last_matched_state = state
        runner.last_matched_index = i - 1
        runner.state = state
        if i == len(input):
            return i
        else:
            return ~i
        break
    runner.state = state
    return ~i
lexer = DummyLexer(recognize, DFA(70,
 {(0, '\t'): 1,
  (0, '\n'): 1,
  (0, '\x0c'): 1,
  (0, '\r'): 1,
  (0, ' '): 1,
  (0, '!'): 2,
  (0, '"'): 4,
  (0, '#'): 3,
  (0, '%'): 5,
  (0, '('): 19,
  (0, ')'): 6,
  (0, '*'): 8,
  (0, '+'): 7,
  (0, ','): 10,
  (0, '-'): 9,
  (0, '.'): 12,
  (0, '/'): 11,
  (0, '0'): 13,
  (0, '1'): 13,
  (0, '2'): 13,
  (0, '3'): 13,
  (0, '4'): 13,
  (0, '5'): 13,
  (0, '6'): 13,
  (0, '7'): 13,
  (0, '8'): 13,
  (0, '9'): 13,
  (0, ';'): 14,
  (0, '<'): 16,
  (0, '='): 15,
  (0, '>'): 17,
  (0, '@'): 18,
  (0, '['): 20,
  (0, ']'): 21,
  (0, 'a'): 22,
  (0, 'b'): 18,
  (0, 'c'): 18,
  (0, 'd'): 24,
  (0, 'e'): 23,
  (0, 'f'): 25,
  (0, 'g'): 18,
  (0, 'h'): 18,
  (0, 'i'): 26,
  (0, 'j'): 18,
  (0, 'k'): 18,
  (0, 'l'): 27,
  (0, 'm'): 18,
  (0, 'n'): 29,
  (0, 'o'): 28,
  (0, 'p'): 18,
  (0, 'q'): 18,
  (0, 'r'): 30,
  (0, 's'): 18,
  (0, 't'): 31,
  (0, 'u'): 18,
  (0, 'v'): 18,
  (0, 'w'): 32,
  (0, 'x'): 18,
  (0, 'y'): 18,
  (0, 'z'): 18,
  (0, '{'): 33,
  (0, '}'): 34,
  (2, '='): 69,
  (3, '\x00'): 3,
  (3, '\x01'): 3,
  (3, '\x02'): 3,
  (3, '\x03'): 3,
  (3, '\x04'): 3,
  (3, '\x05'): 3,
  (3, '\x06'): 3,
  (3, '\x07'): 3,
  (3, '\x08'): 3,
  (3, '\t'): 3,
  (3, '\x0b'): 3,
  (3, '\x0c'): 3,
  (3, '\r'): 3,
  (3, '\x0e'): 3,
  (3, '\x0f'): 3,
  (3, '\x10'): 3,
  (3, '\x11'): 3,
  (3, '\x12'): 3,
  (3, '\x13'): 3,
  (3, '\x14'): 3,
  (3, '\x15'): 3,
  (3, '\x16'): 3,
  (3, '\x17'): 3,
  (3, '\x18'): 3,
  (3, '\x19'): 3,
  (3, '\x1a'): 3,
  (3, '\x1b'): 3,
  (3, '\x1c'): 3,
  (3, '\x1d'): 3,
  (3, '\x1e'): 3,
  (3, '\x1f'): 3,
  (3, ' '): 3,
  (3, '!'): 3,
  (3, '"'): 3,
  (3, '#'): 3,
  (3, '$'): 3,
  (3, '%'): 3,
  (3, '&'): 3,
  (3, "'"): 3,
  (3, '('): 3,
  (3, ')'): 3,
  (3, '*'): 3,
  (3, '+'): 3,
  (3, ','): 3,
  (3, '-'): 3,
  (3, '.'): 3,
  (3, '/'): 3,
  (3, '0'): 3,
  (3, '1'): 3,
  (3, '2'): 3,
  (3, '3'): 3,
  (3, '4'): 3,
  (3, '5'): 3,
  (3, '6'): 3,
  (3, '7'): 3,
  (3, '8'): 3,
  (3, '9'): 3,
  (3, ':'): 3,
  (3, ';'): 3,
  (3, '<'): 3,
  (3, '='): 3,
  (3, '>'): 3,
  (3, '?'): 3,
  (3, '@'): 3,
  (3, 'A'): 3,
  (3, 'B'): 3,
  (3, 'C'): 3,
  (3, 'D'): 3,
  (3, 'E'): 3,
  (3, 'F'): 3,
  (3, 'G'): 3,
  (3, 'H'): 3,
  (3, 'I'): 3,
  (3, 'J'): 3,
  (3, 'K'): 3,
  (3, 'L'): 3,
  (3, 'M'): 3,
  (3, 'N'): 3,
  (3, 'O'): 3,
  (3, 'P'): 3,
  (3, 'Q'): 3,
  (3, 'R'): 3,
  (3, 'S'): 3,
  (3, 'T'): 3,
  (3, 'U'): 3,
  (3, 'V'): 3,
  (3, 'W'): 3,
  (3, 'X'): 3,
  (3, 'Y'): 3,
  (3, 'Z'): 3,
  (3, '['): 3,
  (3, '\\'): 3,
  (3, ']'): 3,
  (3, '^'): 3,
  (3, '_'): 3,
  (3, '`'): 3,
  (3, 'a'): 3,
  (3, 'b'): 3,
  (3, 'c'): 3,
  (3, 'd'): 3,
  (3, 'e'): 3,
  (3, 'f'): 3,
  (3, 'g'): 3,
  (3, 'h'): 3,
  (3, 'i'): 3,
  (3, 'j'): 3,
  (3, 'k'): 3,
  (3, 'l'): 3,
  (3, 'm'): 3,
  (3, 'n'): 3,
  (3, 'o'): 3,
  (3, 'p'): 3,
  (3, 'q'): 3,
  (3, 'r'): 3,
  (3, 's'): 3,
  (3, 't'): 3,
  (3, 'u'): 3,
  (3, 'v'): 3,
  (3, 'w'): 3,
  (3, 'x'): 3,
  (3, 'y'): 3,
  (3, 'z'): 3,
  (3, '{'): 3,
  (3, '|'): 3,
  (3, '}'): 3,
  (3, '~'): 3,
  (3, '\x7f'): 3,
  (3, '\x80'): 3,
  (3, '\x81'): 3,
  (3, '\x82'): 3,
  (3, '\x83'): 3,
  (3, '\x84'): 3,
  (3, '\x85'): 3,
  (3, '\x86'): 3,
  (3, '\x87'): 3,
  (3, '\x88'): 3,
  (3, '\x89'): 3,
  (3, '\x8a'): 3,
  (3, '\x8b'): 3,
  (3, '\x8c'): 3,
  (3, '\x8d'): 3,
  (3, '\x8e'): 3,
  (3, '\x8f'): 3,
  (3, '\x90'): 3,
  (3, '\x91'): 3,
  (3, '\x92'): 3,
  (3, '\x93'): 3,
  (3, '\x94'): 3,
  (3, '\x95'): 3,
  (3, '\x96'): 3,
  (3, '\x97'): 3,
  (3, '\x98'): 3,
  (3, '\x99'): 3,
  (3, '\x9a'): 3,
  (3, '\x9b'): 3,
  (3, '\x9c'): 3,
  (3, '\x9d'): 3,
  (3, '\x9e'): 3,
  (3, '\x9f'): 3,
  (3, '\xa0'): 3,
  (3, '\xa1'): 3,
  (3, '\xa2'): 3,
  (3, '\xa3'): 3,
  (3, '\xa4'): 3,
  (3, '\xa5'): 3,
  (3, '\xa6'): 3,
  (3, '\xa7'): 3,
  (3, '\xa8'): 3,
  (3, '\xa9'): 3,
  (3, '\xaa'): 3,
  (3, '\xab'): 3,
  (3, '\xac'): 3,
  (3, '\xad'): 3,
  (3, '\xae'): 3,
  (3, '\xaf'): 3,
  (3, '\xb0'): 3,
  (3, '\xb1'): 3,
  (3, '\xb2'): 3,
  (3, '\xb3'): 3,
  (3, '\xb4'): 3,
  (3, '\xb5'): 3,
  (3, '\xb6'): 3,
  (3, '\xb7'): 3,
  (3, '\xb8'): 3,
  (3, '\xb9'): 3,
  (3, '\xba'): 3,
  (3, '\xbb'): 3,
  (3, '\xbc'): 3,
  (3, '\xbd'): 3,
  (3, '\xbe'): 3,
  (3, '\xbf'): 3,
  (3, '\xc0'): 3,
  (3, '\xc1'): 3,
  (3, '\xc2'): 3,
  (3, '\xc3'): 3,
  (3, '\xc4'): 3,
  (3, '\xc5'): 3,
  (3, '\xc6'): 3,
  (3, '\xc7'): 3,
  (3, '\xc8'): 3,
  (3, '\xc9'): 3,
  (3, '\xca'): 3,
  (3, '\xcb'): 3,
  (3, '\xcc'): 3,
  (3, '\xcd'): 3,
  (3, '\xce'): 3,
  (3, '\xcf'): 3,
  (3, '\xd0'): 3,
  (3, '\xd1'): 3,
  (3, '\xd2'): 3,
  (3, '\xd3'): 3,
  (3, '\xd4'): 3,
  (3, '\xd5'): 3,
  (3, '\xd6'): 3,
  (3, '\xd7'): 3,
  (3, '\xd8'): 3,
  (3, '\xd9'): 3,
  (3, '\xda'): 3,
  (3, '\xdb'): 3,
  (3, '\xdc'): 3,
  (3, '\xdd'): 3,
  (3, '\xde'): 3,
  (3, '\xdf'): 3,
  (3, '\xe0'): 3,
  (3, '\xe1'): 3,
  (3, '\xe2'): 3,
  (3, '\xe3'): 3,
  (3, '\xe4'): 3,
  (3, '\xe5'): 3,
  (3, '\xe6'): 3,
  (3, '\xe7'): 3,
  (3, '\xe8'): 3,
  (3, '\xe9'): 3,
  (3, '\xea'): 3,
  (3, '\xeb'): 3,
  (3, '\xec'): 3,
  (3, '\xed'): 3,
  (3, '\xee'): 3,
  (3, '\xef'): 3,
  (3, '\xf0'): 3,
  (3, '\xf1'): 3,
  (3, '\xf2'): 3,
  (3, '\xf3'): 3,
  (3, '\xf4'): 3,
  (3, '\xf5'): 3,
  (3, '\xf6'): 3,
  (3, '\xf7'): 3,
  (3, '\xf8'): 3,
  (3, '\xf9'): 3,
  (3, '\xfa'): 3,
  (3, '\xfb'): 3,
  (3, '\xfc'): 3,
  (3, '\xfd'): 3,
  (3, '\xfe'): 3,
  (3, '\xff'): 3,
  (4, '\x00'): 4,
  (4, '\x01'): 4,
  (4, '\x02'): 4,
  (4, '\x03'): 4,
  (4, '\x04'): 4,
  (4, '\x05'): 4,
  (4, '\x06'): 4,
  (4, '\x07'): 4,
  (4, '\x08'): 4,
  (4, '\t'): 4,
  (4, '\n'): 4,
  (4, '\x0b'): 4,
  (4, '\x0c'): 4,
  (4, '\r'): 4,
  (4, '\x0e'): 4,
  (4, '\x0f'): 4,
  (4, '\x10'): 4,
  (4, '\x11'): 4,
  (4, '\x12'): 4,
  (4, '\x13'): 4,
  (4, '\x14'): 4,
  (4, '\x15'): 4,
  (4, '\x16'): 4,
  (4, '\x17'): 4,
  (4, '\x18'): 4,
  (4, '\x19'): 4,
  (4, '\x1a'): 4,
  (4, '\x1b'): 4,
  (4, '\x1c'): 4,
  (4, '\x1d'): 4,
  (4, '\x1e'): 4,
  (4, '\x1f'): 4,
  (4, ' '): 4,
  (4, '!'): 4,
  (4, '"'): 68,
  (4, '#'): 4,
  (4, '$'): 4,
  (4, '%'): 4,
  (4, '&'): 4,
  (4, "'"): 4,
  (4, '('): 4,
  (4, ')'): 4,
  (4, '*'): 4,
  (4, '+'): 4,
  (4, ','): 4,
  (4, '-'): 4,
  (4, '.'): 4,
  (4, '/'): 4,
  (4, '0'): 4,
  (4, '1'): 4,
  (4, '2'): 4,
  (4, '3'): 4,
  (4, '4'): 4,
  (4, '5'): 4,
  (4, '6'): 4,
  (4, '7'): 4,
  (4, '8'): 4,
  (4, '9'): 4,
  (4, ':'): 4,
  (4, ';'): 4,
  (4, '<'): 4,
  (4, '='): 4,
  (4, '>'): 4,
  (4, '?'): 4,
  (4, '@'): 4,
  (4, 'A'): 4,
  (4, 'B'): 4,
  (4, 'C'): 4,
  (4, 'D'): 4,
  (4, 'E'): 4,
  (4, 'F'): 4,
  (4, 'G'): 4,
  (4, 'H'): 4,
  (4, 'I'): 4,
  (4, 'J'): 4,
  (4, 'K'): 4,
  (4, 'L'): 4,
  (4, 'M'): 4,
  (4, 'N'): 4,
  (4, 'O'): 4,
  (4, 'P'): 4,
  (4, 'Q'): 4,
  (4, 'R'): 4,
  (4, 'S'): 4,
  (4, 'T'): 4,
  (4, 'U'): 4,
  (4, 'V'): 4,
  (4, 'W'): 4,
  (4, 'X'): 4,
  (4, 'Y'): 4,
  (4, 'Z'): 4,
  (4, '['): 4,
  (4, ']'): 4,
  (4, '^'): 4,
  (4, '_'): 4,
  (4, '`'): 4,
  (4, 'a'): 4,
  (4, 'b'): 4,
  (4, 'c'): 4,
  (4, 'd'): 4,
  (4, 'e'): 4,
  (4, 'f'): 4,
  (4, 'g'): 4,
  (4, 'h'): 4,
  (4, 'i'): 4,
  (4, 'j'): 4,
  (4, 'k'): 4,
  (4, 'l'): 4,
  (4, 'm'): 4,
  (4, 'n'): 4,
  (4, 'o'): 4,
  (4, 'p'): 4,
  (4, 'q'): 4,
  (4, 'r'): 4,
  (4, 's'): 4,
  (4, 't'): 4,
  (4, 'u'): 4,
  (4, 'v'): 4,
  (4, 'w'): 4,
  (4, 'x'): 4,
  (4, 'y'): 4,
  (4, 'z'): 4,
  (4, '{'): 4,
  (4, '|'): 4,
  (4, '}'): 4,
  (4, '~'): 4,
  (4, '\x7f'): 4,
  (4, '\x80'): 4,
  (4, '\x81'): 4,
  (4, '\x82'): 4,
  (4, '\x83'): 4,
  (4, '\x84'): 4,
  (4, '\x85'): 4,
  (4, '\x86'): 4,
  (4, '\x87'): 4,
  (4, '\x88'): 4,
  (4, '\x89'): 4,
  (4, '\x8a'): 4,
  (4, '\x8b'): 4,
  (4, '\x8c'): 4,
  (4, '\x8d'): 4,
  (4, '\x8e'): 4,
  (4, '\x8f'): 4,
  (4, '\x90'): 4,
  (4, '\x91'): 4,
  (4, '\x92'): 4,
  (4, '\x93'): 4,
  (4, '\x94'): 4,
  (4, '\x95'): 4,
  (4, '\x96'): 4,
  (4, '\x97'): 4,
  (4, '\x98'): 4,
  (4, '\x99'): 4,
  (4, '\x9a'): 4,
  (4, '\x9b'): 4,
  (4, '\x9c'): 4,
  (4, '\x9d'): 4,
  (4, '\x9e'): 4,
  (4, '\x9f'): 4,
  (4, '\xa0'): 4,
  (4, '\xa1'): 4,
  (4, '\xa2'): 4,
  (4, '\xa3'): 4,
  (4, '\xa4'): 4,
  (4, '\xa5'): 4,
  (4, '\xa6'): 4,
  (4, '\xa7'): 4,
  (4, '\xa8'): 4,
  (4, '\xa9'): 4,
  (4, '\xaa'): 4,
  (4, '\xab'): 4,
  (4, '\xac'): 4,
  (4, '\xad'): 4,
  (4, '\xae'): 4,
  (4, '\xaf'): 4,
  (4, '\xb0'): 4,
  (4, '\xb1'): 4,
  (4, '\xb2'): 4,
  (4, '\xb3'): 4,
  (4, '\xb4'): 4,
  (4, '\xb5'): 4,
  (4, '\xb6'): 4,
  (4, '\xb7'): 4,
  (4, '\xb8'): 4,
  (4, '\xb9'): 4,
  (4, '\xba'): 4,
  (4, '\xbb'): 4,
  (4, '\xbc'): 4,
  (4, '\xbd'): 4,
  (4, '\xbe'): 4,
  (4, '\xbf'): 4,
  (4, '\xc0'): 4,
  (4, '\xc1'): 4,
  (4, '\xc2'): 4,
  (4, '\xc3'): 4,
  (4, '\xc4'): 4,
  (4, '\xc5'): 4,
  (4, '\xc6'): 4,
  (4, '\xc7'): 4,
  (4, '\xc8'): 4,
  (4, '\xc9'): 4,
  (4, '\xca'): 4,
  (4, '\xcb'): 4,
  (4, '\xcc'): 4,
  (4, '\xcd'): 4,
  (4, '\xce'): 4,
  (4, '\xcf'): 4,
  (4, '\xd0'): 4,
  (4, '\xd1'): 4,
  (4, '\xd2'): 4,
  (4, '\xd3'): 4,
  (4, '\xd4'): 4,
  (4, '\xd5'): 4,
  (4, '\xd6'): 4,
  (4, '\xd7'): 4,
  (4, '\xd8'): 4,
  (4, '\xd9'): 4,
  (4, '\xda'): 4,
  (4, '\xdb'): 4,
  (4, '\xdc'): 4,
  (4, '\xdd'): 4,
  (4, '\xde'): 4,
  (4, '\xdf'): 4,
  (4, '\xe0'): 4,
  (4, '\xe1'): 4,
  (4, '\xe2'): 4,
  (4, '\xe3'): 4,
  (4, '\xe4'): 4,
  (4, '\xe5'): 4,
  (4, '\xe6'): 4,
  (4, '\xe7'): 4,
  (4, '\xe8'): 4,
  (4, '\xe9'): 4,
  (4, '\xea'): 4,
  (4, '\xeb'): 4,
  (4, '\xec'): 4,
  (4, '\xed'): 4,
  (4, '\xee'): 4,
  (4, '\xef'): 4,
  (4, '\xf0'): 4,
  (4, '\xf1'): 4,
  (4, '\xf2'): 4,
  (4, '\xf3'): 4,
  (4, '\xf4'): 4,
  (4, '\xf5'): 4,
  (4, '\xf6'): 4,
  (4, '\xf7'): 4,
  (4, '\xf8'): 4,
  (4, '\xf9'): 4,
  (4, '\xfa'): 4,
  (4, '\xfb'): 4,
  (4, '\xfc'): 4,
  (4, '\xfd'): 4,
  (4, '\xfe'): 4,
  (4, '\xff'): 4,
  (12, '0'): 65,
  (12, '1'): 65,
  (12, '2'): 65,
  (12, '3'): 65,
  (12, '4'): 65,
  (12, '5'): 65,
  (12, '6'): 65,
  (12, '7'): 65,
  (12, '8'): 65,
  (12, '9'): 65,
  (13, '.'): 64,
  (13, '0'): 13,
  (13, '1'): 13,
  (13, '2'): 13,
  (13, '3'): 13,
  (13, '4'): 13,
  (13, '5'): 13,
  (13, '6'): 13,
  (13, '7'): 13,
  (13, '8'): 13,
  (13, '9'): 13,
  (13, 'E'): 63,
  (13, 'e'): 63,
  (15, '='): 62,
  (18, '0'): 18,
  (18, '1'): 18,
  (18, '2'): 18,
  (18, '3'): 18,
  (18, '4'): 18,
  (18, '5'): 18,
  (18, '6'): 18,
  (18, '7'): 18,
  (18, '8'): 18,
  (18, '9'): 18,
  (18, '@'): 18,
  (18, 'A'): 18,
  (18, 'B'): 18,
  (18, 'C'): 18,
  (18, 'D'): 18,
  (18, 'E'): 18,
  (18, 'F'): 18,
  (18, 'G'): 18,
  (18, 'H'): 18,
  (18, 'I'): 18,
  (18, 'J'): 18,
  (18, 'K'): 18,
  (18, 'L'): 18,
  (18, 'M'): 18,
  (18, 'N'): 18,
  (18, 'O'): 18,
  (18, 'P'): 18,
  (18, 'Q'): 18,
  (18, 'R'): 18,
  (18, 'S'): 18,
  (18, 'T'): 18,
  (18, 'U'): 18,
  (18, 'V'): 18,
  (18, 'W'): 18,
  (18, 'X'): 18,
  (18, 'Y'): 18,
  (18, 'Z'): 18,
  (18, '_'): 18,
  (18, 'a'): 18,
  (18, 'b'): 18,
  (18, 'c'): 18,
  (18, 'd'): 18,
  (18, 'e'): 18,
  (18, 'f'): 18,
  (18, 'g'): 18,
  (18, 'h'): 18,
  (18, 'i'): 18,
  (18, 'j'): 18,
  (18, 'k'): 18,
  (18, 'l'): 18,
  (18, 'm'): 18,
  (18, 'n'): 18,
  (18, 'o'): 18,
  (18, 'p'): 18,
  (18, 'q'): 18,
  (18, 'r'): 18,
  (18, 's'): 18,
  (18, 't'): 18,
  (18, 'u'): 18,
  (18, 'v'): 18,
  (18, 'w'): 18,
  (18, 'x'): 18,
  (18, 'y'): 18,
  (18, 'z'): 18,
  (22, '0'): 18,
  (22, '1'): 18,
  (22, '2'): 18,
  (22, '3'): 18,
  (22, '4'): 18,
  (22, '5'): 18,
  (22, '6'): 18,
  (22, '7'): 18,
  (22, '8'): 18,
  (22, '9'): 18,
  (22, '@'): 18,
  (22, 'A'): 18,
  (22, 'B'): 18,
  (22, 'C'): 18,
  (22, 'D'): 18,
  (22, 'E'): 18,
  (22, 'F'): 18,
  (22, 'G'): 18,
  (22, 'H'): 18,
  (22, 'I'): 18,
  (22, 'J'): 18,
  (22, 'K'): 18,
  (22, 'L'): 18,
  (22, 'M'): 18,
  (22, 'N'): 18,
  (22, 'O'): 18,
  (22, 'P'): 18,
  (22, 'Q'): 18,
  (22, 'R'): 18,
  (22, 'S'): 18,
  (22, 'T'): 18,
  (22, 'U'): 18,
  (22, 'V'): 18,
  (22, 'W'): 18,
  (22, 'X'): 18,
  (22, 'Y'): 18,
  (22, 'Z'): 18,
  (22, '_'): 18,
  (22, 'a'): 18,
  (22, 'b'): 18,
  (22, 'c'): 18,
  (22, 'd'): 18,
  (22, 'e'): 18,
  (22, 'f'): 18,
  (22, 'g'): 18,
  (22, 'h'): 18,
  (22, 'i'): 18,
  (22, 'j'): 18,
  (22, 'k'): 18,
  (22, 'l'): 18,
  (22, 'm'): 18,
  (22, 'n'): 60,
  (22, 'o'): 18,
  (22, 'p'): 18,
  (22, 'q'): 18,
  (22, 'r'): 18,
  (22, 's'): 18,
  (22, 't'): 18,
  (22, 'u'): 18,
  (22, 'v'): 18,
  (22, 'w'): 18,
  (22, 'x'): 18,
  (22, 'y'): 18,
  (22, 'z'): 18,
  (23, '0'): 18,
  (23, '1'): 18,
  (23, '2'): 18,
  (23, '3'): 18,
  (23, '4'): 18,
  (23, '5'): 18,
  (23, '6'): 18,
  (23, '7'): 18,
  (23, '8'): 18,
  (23, '9'): 18,
  (23, '@'): 18,
  (23, 'A'): 18,
  (23, 'B'): 18,
  (23, 'C'): 18,
  (23, 'D'): 18,
  (23, 'E'): 18,
  (23, 'F'): 18,
  (23, 'G'): 18,
  (23, 'H'): 18,
  (23, 'I'): 18,
  (23, 'J'): 18,
  (23, 'K'): 18,
  (23, 'L'): 18,
  (23, 'M'): 18,
  (23, 'N'): 18,
  (23, 'O'): 18,
  (23, 'P'): 18,
  (23, 'Q'): 18,
  (23, 'R'): 18,
  (23, 'S'): 18,
  (23, 'T'): 18,
  (23, 'U'): 18,
  (23, 'V'): 18,
  (23, 'W'): 18,
  (23, 'X'): 18,
  (23, 'Y'): 18,
  (23, 'Z'): 18,
  (23, '_'): 18,
  (23, 'a'): 18,
  (23, 'b'): 18,
  (23, 'c'): 18,
  (23, 'd'): 18,
  (23, 'e'): 18,
  (23, 'f'): 18,
  (23, 'g'): 18,
  (23, 'h'): 18,
  (23, 'i'): 18,
  (23, 'j'): 18,
  (23, 'k'): 18,
  (23, 'l'): 57,
  (23, 'm'): 18,
  (23, 'n'): 18,
  (23, 'o'): 18,
  (23, 'p'): 18,
  (23, 'q'): 18,
  (23, 'r'): 18,
  (23, 's'): 18,
  (23, 't'): 18,
  (23, 'u'): 18,
  (23, 'v'): 18,
  (23, 'w'): 18,
  (23, 'x'): 18,
  (23, 'y'): 18,
  (23, 'z'): 18,
  (24, '0'): 18,
  (24, '1'): 18,
  (24, '2'): 18,
  (24, '3'): 18,
  (24, '4'): 18,
  (24, '5'): 18,
  (24, '6'): 18,
  (24, '7'): 18,
  (24, '8'): 18,
  (24, '9'): 18,
  (24, '@'): 18,
  (24, 'A'): 18,
  (24, 'B'): 18,
  (24, 'C'): 18,
  (24, 'D'): 18,
  (24, 'E'): 18,
  (24, 'F'): 18,
  (24, 'G'): 18,
  (24, 'H'): 18,
  (24, 'I'): 18,
  (24, 'J'): 18,
  (24, 'K'): 18,
  (24, 'L'): 18,
  (24, 'M'): 18,
  (24, 'N'): 18,
  (24, 'O'): 18,
  (24, 'P'): 18,
  (24, 'Q'): 18,
  (24, 'R'): 18,
  (24, 'S'): 18,
  (24, 'T'): 18,
  (24, 'U'): 18,
  (24, 'V'): 18,
  (24, 'W'): 18,
  (24, 'X'): 18,
  (24, 'Y'): 18,
  (24, 'Z'): 18,
  (24, '_'): 18,
  (24, 'a'): 18,
  (24, 'b'): 18,
  (24, 'c'): 18,
  (24, 'd'): 18,
  (24, 'e'): 18,
  (24, 'f'): 18,
  (24, 'g'): 18,
  (24, 'h'): 18,
  (24, 'i'): 18,
  (24, 'j'): 18,
  (24, 'k'): 18,
  (24, 'l'): 18,
  (24, 'm'): 18,
  (24, 'n'): 18,
  (24, 'o'): 56,
  (24, 'p'): 18,
  (24, 'q'): 18,
  (24, 'r'): 18,
  (24, 's'): 18,
  (24, 't'): 18,
  (24, 'u'): 18,
  (24, 'v'): 18,
  (24, 'w'): 18,
  (24, 'x'): 18,
  (24, 'y'): 18,
  (24, 'z'): 18,
  (25, '0'): 18,
  (25, '1'): 18,
  (25, '2'): 18,
  (25, '3'): 18,
  (25, '4'): 18,
  (25, '5'): 18,
  (25, '6'): 18,
  (25, '7'): 18,
  (25, '8'): 18,
  (25, '9'): 18,
  (25, '@'): 18,
  (25, 'A'): 18,
  (25, 'B'): 18,
  (25, 'C'): 18,
  (25, 'D'): 18,
  (25, 'E'): 18,
  (25, 'F'): 18,
  (25, 'G'): 18,
  (25, 'H'): 18,
  (25, 'I'): 18,
  (25, 'J'): 18,
  (25, 'K'): 18,
  (25, 'L'): 18,
  (25, 'M'): 18,
  (25, 'N'): 18,
  (25, 'O'): 18,
  (25, 'P'): 18,
  (25, 'Q'): 18,
  (25, 'R'): 18,
  (25, 'S'): 18,
  (25, 'T'): 18,
  (25, 'U'): 18,
  (25, 'V'): 18,
  (25, 'W'): 18,
  (25, 'X'): 18,
  (25, 'Y'): 18,
  (25, 'Z'): 18,
  (25, '_'): 18,
  (25, 'a'): 53,
  (25, 'b'): 18,
  (25, 'c'): 18,
  (25, 'd'): 18,
  (25, 'e'): 18,
  (25, 'f'): 18,
  (25, 'g'): 18,
  (25, 'h'): 18,
  (25, 'i'): 18,
  (25, 'j'): 18,
  (25, 'k'): 18,
  (25, 'l'): 18,
  (25, 'm'): 18,
  (25, 'n'): 54,
  (25, 'o'): 18,
  (25, 'p'): 18,
  (25, 'q'): 18,
  (25, 'r'): 18,
  (25, 's'): 18,
  (25, 't'): 18,
  (25, 'u'): 18,
  (25, 'v'): 18,
  (25, 'w'): 18,
  (25, 'x'): 18,
  (25, 'y'): 18,
  (25, 'z'): 18,
  (26, '0'): 18,
  (26, '1'): 18,
  (26, '2'): 18,
  (26, '3'): 18,
  (26, '4'): 18,
  (26, '5'): 18,
  (26, '6'): 18,
  (26, '7'): 18,
  (26, '8'): 18,
  (26, '9'): 18,
  (26, '@'): 18,
  (26, 'A'): 18,
  (26, 'B'): 18,
  (26, 'C'): 18,
  (26, 'D'): 18,
  (26, 'E'): 18,
  (26, 'F'): 18,
  (26, 'G'): 18,
  (26, 'H'): 18,
  (26, 'I'): 18,
  (26, 'J'): 18,
  (26, 'K'): 18,
  (26, 'L'): 18,
  (26, 'M'): 18,
  (26, 'N'): 18,
  (26, 'O'): 18,
  (26, 'P'): 18,
  (26, 'Q'): 18,
  (26, 'R'): 18,
  (26, 'S'): 18,
  (26, 'T'): 18,
  (26, 'U'): 18,
  (26, 'V'): 18,
  (26, 'W'): 18,
  (26, 'X'): 18,
  (26, 'Y'): 18,
  (26, 'Z'): 18,
  (26, '_'): 18,
  (26, 'a'): 18,
  (26, 'b'): 18,
  (26, 'c'): 18,
  (26, 'd'): 18,
  (26, 'e'): 18,
  (26, 'f'): 52,
  (26, 'g'): 18,
  (26, 'h'): 18,
  (26, 'i'): 18,
  (26, 'j'): 18,
  (26, 'k'): 18,
  (26, 'l'): 18,
  (26, 'm'): 18,
  (26, 'n'): 18,
  (26, 'o'): 18,
  (26, 'p'): 18,
  (26, 'q'): 18,
  (26, 'r'): 18,
  (26, 's'): 18,
  (26, 't'): 18,
  (26, 'u'): 18,
  (26, 'v'): 18,
  (26, 'w'): 18,
  (26, 'x'): 18,
  (26, 'y'): 18,
  (26, 'z'): 18,
  (27, '0'): 18,
  (27, '1'): 18,
  (27, '2'): 18,
  (27, '3'): 18,
  (27, '4'): 18,
  (27, '5'): 18,
  (27, '6'): 18,
  (27, '7'): 18,
  (27, '8'): 18,
  (27, '9'): 18,
  (27, '@'): 18,
  (27, 'A'): 18,
  (27, 'B'): 18,
  (27, 'C'): 18,
  (27, 'D'): 18,
  (27, 'E'): 18,
  (27, 'F'): 18,
  (27, 'G'): 18,
  (27, 'H'): 18,
  (27, 'I'): 18,
  (27, 'J'): 18,
  (27, 'K'): 18,
  (27, 'L'): 18,
  (27, 'M'): 18,
  (27, 'N'): 18,
  (27, 'O'): 18,
  (27, 'P'): 18,
  (27, 'Q'): 18,
  (27, 'R'): 18,
  (27, 'S'): 18,
  (27, 'T'): 18,
  (27, 'U'): 18,
  (27, 'V'): 18,
  (27, 'W'): 18,
  (27, 'X'): 18,
  (27, 'Y'): 18,
  (27, 'Z'): 18,
  (27, '_'): 18,
  (27, 'a'): 18,
  (27, 'b'): 18,
  (27, 'c'): 18,
  (27, 'd'): 18,
  (27, 'e'): 50,
  (27, 'f'): 18,
  (27, 'g'): 18,
  (27, 'h'): 18,
  (27, 'i'): 18,
  (27, 'j'): 18,
  (27, 'k'): 18,
  (27, 'l'): 18,
  (27, 'm'): 18,
  (27, 'n'): 18,
  (27, 'o'): 18,
  (27, 'p'): 18,
  (27, 'q'): 18,
  (27, 'r'): 18,
  (27, 's'): 18,
  (27, 't'): 18,
  (27, 'u'): 18,
  (27, 'v'): 18,
  (27, 'w'): 18,
  (27, 'x'): 18,
  (27, 'y'): 18,
  (27, 'z'): 18,
  (28, '0'): 18,
  (28, '1'): 18,
  (28, '2'): 18,
  (28, '3'): 18,
  (28, '4'): 18,
  (28, '5'): 18,
  (28, '6'): 18,
  (28, '7'): 18,
  (28, '8'): 18,
  (28, '9'): 18,
  (28, '@'): 18,
  (28, 'A'): 18,
  (28, 'B'): 18,
  (28, 'C'): 18,
  (28, 'D'): 18,
  (28, 'E'): 18,
  (28, 'F'): 18,
  (28, 'G'): 18,
  (28, 'H'): 18,
  (28, 'I'): 18,
  (28, 'J'): 18,
  (28, 'K'): 18,
  (28, 'L'): 18,
  (28, 'M'): 18,
  (28, 'N'): 18,
  (28, 'O'): 18,
  (28, 'P'): 18,
  (28, 'Q'): 18,
  (28, 'R'): 18,
  (28, 'S'): 18,
  (28, 'T'): 18,
  (28, 'U'): 18,
  (28, 'V'): 18,
  (28, 'W'): 18,
  (28, 'X'): 18,
  (28, 'Y'): 18,
  (28, 'Z'): 18,
  (28, '_'): 18,
  (28, 'a'): 18,
  (28, 'b'): 18,
  (28, 'c'): 18,
  (28, 'd'): 18,
  (28, 'e'): 18,
  (28, 'f'): 18,
  (28, 'g'): 18,
  (28, 'h'): 18,
  (28, 'i'): 18,
  (28, 'j'): 18,
  (28, 'k'): 18,
  (28, 'l'): 18,
  (28, 'm'): 18,
  (28, 'n'): 18,
  (28, 'o'): 18,
  (28, 'p'): 18,
  (28, 'q'): 18,
  (28, 'r'): 49,
  (28, 's'): 18,
  (28, 't'): 18,
  (28, 'u'): 18,
  (28, 'v'): 18,
  (28, 'w'): 18,
  (28, 'x'): 18,
  (28, 'y'): 18,
  (28, 'z'): 18,
  (29, '0'): 18,
  (29, '1'): 18,
  (29, '2'): 18,
  (29, '3'): 18,
  (29, '4'): 18,
  (29, '5'): 18,
  (29, '6'): 18,
  (29, '7'): 18,
  (29, '8'): 18,
  (29, '9'): 18,
  (29, '@'): 18,
  (29, 'A'): 18,
  (29, 'B'): 18,
  (29, 'C'): 18,
  (29, 'D'): 18,
  (29, 'E'): 18,
  (29, 'F'): 18,
  (29, 'G'): 18,
  (29, 'H'): 18,
  (29, 'I'): 18,
  (29, 'J'): 18,
  (29, 'K'): 18,
  (29, 'L'): 18,
  (29, 'M'): 18,
  (29, 'N'): 18,
  (29, 'O'): 18,
  (29, 'P'): 18,
  (29, 'Q'): 18,
  (29, 'R'): 18,
  (29, 'S'): 18,
  (29, 'T'): 18,
  (29, 'U'): 18,
  (29, 'V'): 18,
  (29, 'W'): 18,
  (29, 'X'): 18,
  (29, 'Y'): 18,
  (29, 'Z'): 18,
  (29, '_'): 18,
  (29, 'a'): 18,
  (29, 'b'): 18,
  (29, 'c'): 18,
  (29, 'd'): 18,
  (29, 'e'): 18,
  (29, 'f'): 18,
  (29, 'g'): 18,
  (29, 'h'): 18,
  (29, 'i'): 18,
  (29, 'j'): 18,
  (29, 'k'): 18,
  (29, 'l'): 18,
  (29, 'm'): 18,
  (29, 'n'): 18,
  (29, 'o'): 47,
  (29, 'p'): 18,
  (29, 'q'): 18,
  (29, 'r'): 18,
  (29, 's'): 18,
  (29, 't'): 18,
  (29, 'u'): 18,
  (29, 'v'): 18,
  (29, 'w'): 18,
  (29, 'x'): 18,
  (29, 'y'): 18,
  (29, 'z'): 18,
  (30, '0'): 18,
  (30, '1'): 18,
  (30, '2'): 18,
  (30, '3'): 18,
  (30, '4'): 18,
  (30, '5'): 18,
  (30, '6'): 18,
  (30, '7'): 18,
  (30, '8'): 18,
  (30, '9'): 18,
  (30, '@'): 18,
  (30, 'A'): 18,
  (30, 'B'): 18,
  (30, 'C'): 18,
  (30, 'D'): 18,
  (30, 'E'): 18,
  (30, 'F'): 18,
  (30, 'G'): 18,
  (30, 'H'): 18,
  (30, 'I'): 18,
  (30, 'J'): 18,
  (30, 'K'): 18,
  (30, 'L'): 18,
  (30, 'M'): 18,
  (30, 'N'): 18,
  (30, 'O'): 18,
  (30, 'P'): 18,
  (30, 'Q'): 18,
  (30, 'R'): 18,
  (30, 'S'): 18,
  (30, 'T'): 18,
  (30, 'U'): 18,
  (30, 'V'): 18,
  (30, 'W'): 18,
  (30, 'X'): 18,
  (30, 'Y'): 18,
  (30, 'Z'): 18,
  (30, '_'): 18,
  (30, 'a'): 18,
  (30, 'b'): 18,
  (30, 'c'): 18,
  (30, 'd'): 18,
  (30, 'e'): 42,
  (30, 'f'): 18,
  (30, 'g'): 18,
  (30, 'h'): 18,
  (30, 'i'): 18,
  (30, 'j'): 18,
  (30, 'k'): 18,
  (30, 'l'): 18,
  (30, 'm'): 18,
  (30, 'n'): 18,
  (30, 'o'): 18,
  (30, 'p'): 18,
  (30, 'q'): 18,
  (30, 'r'): 18,
  (30, 's'): 18,
  (30, 't'): 18,
  (30, 'u'): 18,
  (30, 'v'): 18,
  (30, 'w'): 18,
  (30, 'x'): 18,
  (30, 'y'): 18,
  (30, 'z'): 18,
  (31, '0'): 18,
  (31, '1'): 18,
  (31, '2'): 18,
  (31, '3'): 18,
  (31, '4'): 18,
  (31, '5'): 18,
  (31, '6'): 18,
  (31, '7'): 18,
  (31, '8'): 18,
  (31, '9'): 18,
  (31, '@'): 18,
  (31, 'A'): 18,
  (31, 'B'): 18,
  (31, 'C'): 18,
  (31, 'D'): 18,
  (31, 'E'): 18,
  (31, 'F'): 18,
  (31, 'G'): 18,
  (31, 'H'): 18,
  (31, 'I'): 18,
  (31, 'J'): 18,
  (31, 'K'): 18,
  (31, 'L'): 18,
  (31, 'M'): 18,
  (31, 'N'): 18,
  (31, 'O'): 18,
  (31, 'P'): 18,
  (31, 'Q'): 18,
  (31, 'R'): 18,
  (31, 'S'): 18,
  (31, 'T'): 18,
  (31, 'U'): 18,
  (31, 'V'): 18,
  (31, 'W'): 18,
  (31, 'X'): 18,
  (31, 'Y'): 18,
  (31, 'Z'): 18,
  (31, '_'): 18,
  (31, 'a'): 18,
  (31, 'b'): 18,
  (31, 'c'): 18,
  (31, 'd'): 18,
  (31, 'e'): 18,
  (31, 'f'): 18,
  (31, 'g'): 18,
  (31, 'h'): 18,
  (31, 'i'): 18,
  (31, 'j'): 18,
  (31, 'k'): 18,
  (31, 'l'): 18,
  (31, 'm'): 18,
  (31, 'n'): 18,
  (31, 'o'): 18,
  (31, 'p'): 18,
  (31, 'q'): 18,
  (31, 'r'): 39,
  (31, 's'): 18,
  (31, 't'): 18,
  (31, 'u'): 18,
  (31, 'v'): 18,
  (31, 'w'): 18,
  (31, 'x'): 18,
  (31, 'y'): 18,
  (31, 'z'): 18,
  (32, '0'): 18,
  (32, '1'): 18,
  (32, '2'): 18,
  (32, '3'): 18,
  (32, '4'): 18,
  (32, '5'): 18,
  (32, '6'): 18,
  (32, '7'): 18,
  (32, '8'): 18,
  (32, '9'): 18,
  (32, '@'): 18,
  (32, 'A'): 18,
  (32, 'B'): 18,
  (32, 'C'): 18,
  (32, 'D'): 18,
  (32, 'E'): 18,
  (32, 'F'): 18,
  (32, 'G'): 18,
  (32, 'H'): 18,
  (32, 'I'): 18,
  (32, 'J'): 18,
  (32, 'K'): 18,
  (32, 'L'): 18,
  (32, 'M'): 18,
  (32, 'N'): 18,
  (32, 'O'): 18,
  (32, 'P'): 18,
  (32, 'Q'): 18,
  (32, 'R'): 18,
  (32, 'S'): 18,
  (32, 'T'): 18,
  (32, 'U'): 18,
  (32, 'V'): 18,
  (32, 'W'): 18,
  (32, 'X'): 18,
  (32, 'Y'): 18,
  (32, 'Z'): 18,
  (32, '_'): 18,
  (32, 'a'): 18,
  (32, 'b'): 18,
  (32, 'c'): 18,
  (32, 'd'): 18,
  (32, 'e'): 18,
  (32, 'f'): 18,
  (32, 'g'): 18,
  (32, 'h'): 35,
  (32, 'i'): 18,
  (32, 'j'): 18,
  (32, 'k'): 18,
  (32, 'l'): 18,
  (32, 'm'): 18,
  (32, 'n'): 18,
  (32, 'o'): 18,
  (32, 'p'): 18,
  (32, 'q'): 18,
  (32, 'r'): 18,
  (32, 's'): 18,
  (32, 't'): 18,
  (32, 'u'): 18,
  (32, 'v'): 18,
  (32, 'w'): 18,
  (32, 'x'): 18,
  (32, 'y'): 18,
  (32, 'z'): 18,
  (35, '0'): 18,
  (35, '1'): 18,
  (35, '2'): 18,
  (35, '3'): 18,
  (35, '4'): 18,
  (35, '5'): 18,
  (35, '6'): 18,
  (35, '7'): 18,
  (35, '8'): 18,
  (35, '9'): 18,
  (35, '@'): 18,
  (35, 'A'): 18,
  (35, 'B'): 18,
  (35, 'C'): 18,
  (35, 'D'): 18,
  (35, 'E'): 18,
  (35, 'F'): 18,
  (35, 'G'): 18,
  (35, 'H'): 18,
  (35, 'I'): 18,
  (35, 'J'): 18,
  (35, 'K'): 18,
  (35, 'L'): 18,
  (35, 'M'): 18,
  (35, 'N'): 18,
  (35, 'O'): 18,
  (35, 'P'): 18,
  (35, 'Q'): 18,
  (35, 'R'): 18,
  (35, 'S'): 18,
  (35, 'T'): 18,
  (35, 'U'): 18,
  (35, 'V'): 18,
  (35, 'W'): 18,
  (35, 'X'): 18,
  (35, 'Y'): 18,
  (35, 'Z'): 18,
  (35, '_'): 18,
  (35, 'a'): 18,
  (35, 'b'): 18,
  (35, 'c'): 18,
  (35, 'd'): 18,
  (35, 'e'): 18,
  (35, 'f'): 18,
  (35, 'g'): 18,
  (35, 'h'): 18,
  (35, 'i'): 36,
  (35, 'j'): 18,
  (35, 'k'): 18,
  (35, 'l'): 18,
  (35, 'm'): 18,
  (35, 'n'): 18,
  (35, 'o'): 18,
  (35, 'p'): 18,
  (35, 'q'): 18,
  (35, 'r'): 18,
  (35, 's'): 18,
  (35, 't'): 18,
  (35, 'u'): 18,
  (35, 'v'): 18,
  (35, 'w'): 18,
  (35, 'x'): 18,
  (35, 'y'): 18,
  (35, 'z'): 18,
  (36, '0'): 18,
  (36, '1'): 18,
  (36, '2'): 18,
  (36, '3'): 18,
  (36, '4'): 18,
  (36, '5'): 18,
  (36, '6'): 18,
  (36, '7'): 18,
  (36, '8'): 18,
  (36, '9'): 18,
  (36, '@'): 18,
  (36, 'A'): 18,
  (36, 'B'): 18,
  (36, 'C'): 18,
  (36, 'D'): 18,
  (36, 'E'): 18,
  (36, 'F'): 18,
  (36, 'G'): 18,
  (36, 'H'): 18,
  (36, 'I'): 18,
  (36, 'J'): 18,
  (36, 'K'): 18,
  (36, 'L'): 18,
  (36, 'M'): 18,
  (36, 'N'): 18,
  (36, 'O'): 18,
  (36, 'P'): 18,
  (36, 'Q'): 18,
  (36, 'R'): 18,
  (36, 'S'): 18,
  (36, 'T'): 18,
  (36, 'U'): 18,
  (36, 'V'): 18,
  (36, 'W'): 18,
  (36, 'X'): 18,
  (36, 'Y'): 18,
  (36, 'Z'): 18,
  (36, '_'): 18,
  (36, 'a'): 18,
  (36, 'b'): 18,
  (36, 'c'): 18,
  (36, 'd'): 18,
  (36, 'e'): 18,
  (36, 'f'): 18,
  (36, 'g'): 18,
  (36, 'h'): 18,
  (36, 'i'): 18,
  (36, 'j'): 18,
  (36, 'k'): 18,
  (36, 'l'): 37,
  (36, 'm'): 18,
  (36, 'n'): 18,
  (36, 'o'): 18,
  (36, 'p'): 18,
  (36, 'q'): 18,
  (36, 'r'): 18,
  (36, 's'): 18,
  (36, 't'): 18,
  (36, 'u'): 18,
  (36, 'v'): 18,
  (36, 'w'): 18,
  (36, 'x'): 18,
  (36, 'y'): 18,
  (36, 'z'): 18,
  (37, '0'): 18,
  (37, '1'): 18,
  (37, '2'): 18,
  (37, '3'): 18,
  (37, '4'): 18,
  (37, '5'): 18,
  (37, '6'): 18,
  (37, '7'): 18,
  (37, '8'): 18,
  (37, '9'): 18,
  (37, '@'): 18,
  (37, 'A'): 18,
  (37, 'B'): 18,
  (37, 'C'): 18,
  (37, 'D'): 18,
  (37, 'E'): 18,
  (37, 'F'): 18,
  (37, 'G'): 18,
  (37, 'H'): 18,
  (37, 'I'): 18,
  (37, 'J'): 18,
  (37, 'K'): 18,
  (37, 'L'): 18,
  (37, 'M'): 18,
  (37, 'N'): 18,
  (37, 'O'): 18,
  (37, 'P'): 18,
  (37, 'Q'): 18,
  (37, 'R'): 18,
  (37, 'S'): 18,
  (37, 'T'): 18,
  (37, 'U'): 18,
  (37, 'V'): 18,
  (37, 'W'): 18,
  (37, 'X'): 18,
  (37, 'Y'): 18,
  (37, 'Z'): 18,
  (37, '_'): 18,
  (37, 'a'): 18,
  (37, 'b'): 18,
  (37, 'c'): 18,
  (37, 'd'): 18,
  (37, 'e'): 38,
  (37, 'f'): 18,
  (37, 'g'): 18,
  (37, 'h'): 18,
  (37, 'i'): 18,
  (37, 'j'): 18,
  (37, 'k'): 18,
  (37, 'l'): 18,
  (37, 'm'): 18,
  (37, 'n'): 18,
  (37, 'o'): 18,
  (37, 'p'): 18,
  (37, 'q'): 18,
  (37, 'r'): 18,
  (37, 's'): 18,
  (37, 't'): 18,
  (37, 'u'): 18,
  (37, 'v'): 18,
  (37, 'w'): 18,
  (37, 'x'): 18,
  (37, 'y'): 18,
  (37, 'z'): 18,
  (38, '0'): 18,
  (38, '1'): 18,
  (38, '2'): 18,
  (38, '3'): 18,
  (38, '4'): 18,
  (38, '5'): 18,
  (38, '6'): 18,
  (38, '7'): 18,
  (38, '8'): 18,
  (38, '9'): 18,
  (38, '@'): 18,
  (38, 'A'): 18,
  (38, 'B'): 18,
  (38, 'C'): 18,
  (38, 'D'): 18,
  (38, 'E'): 18,
  (38, 'F'): 18,
  (38, 'G'): 18,
  (38, 'H'): 18,
  (38, 'I'): 18,
  (38, 'J'): 18,
  (38, 'K'): 18,
  (38, 'L'): 18,
  (38, 'M'): 18,
  (38, 'N'): 18,
  (38, 'O'): 18,
  (38, 'P'): 18,
  (38, 'Q'): 18,
  (38, 'R'): 18,
  (38, 'S'): 18,
  (38, 'T'): 18,
  (38, 'U'): 18,
  (38, 'V'): 18,
  (38, 'W'): 18,
  (38, 'X'): 18,
  (38, 'Y'): 18,
  (38, 'Z'): 18,
  (38, '_'): 18,
  (38, 'a'): 18,
  (38, 'b'): 18,
  (38, 'c'): 18,
  (38, 'd'): 18,
  (38, 'e'): 18,
  (38, 'f'): 18,
  (38, 'g'): 18,
  (38, 'h'): 18,
  (38, 'i'): 18,
  (38, 'j'): 18,
  (38, 'k'): 18,
  (38, 'l'): 18,
  (38, 'm'): 18,
  (38, 'n'): 18,
  (38, 'o'): 18,
  (38, 'p'): 18,
  (38, 'q'): 18,
  (38, 'r'): 18,
  (38, 's'): 18,
  (38, 't'): 18,
  (38, 'u'): 18,
  (38, 'v'): 18,
  (38, 'w'): 18,
  (38, 'x'): 18,
  (38, 'y'): 18,
  (38, 'z'): 18,
  (39, '0'): 18,
  (39, '1'): 18,
  (39, '2'): 18,
  (39, '3'): 18,
  (39, '4'): 18,
  (39, '5'): 18,
  (39, '6'): 18,
  (39, '7'): 18,
  (39, '8'): 18,
  (39, '9'): 18,
  (39, '@'): 18,
  (39, 'A'): 18,
  (39, 'B'): 18,
  (39, 'C'): 18,
  (39, 'D'): 18,
  (39, 'E'): 18,
  (39, 'F'): 18,
  (39, 'G'): 18,
  (39, 'H'): 18,
  (39, 'I'): 18,
  (39, 'J'): 18,
  (39, 'K'): 18,
  (39, 'L'): 18,
  (39, 'M'): 18,
  (39, 'N'): 18,
  (39, 'O'): 18,
  (39, 'P'): 18,
  (39, 'Q'): 18,
  (39, 'R'): 18,
  (39, 'S'): 18,
  (39, 'T'): 18,
  (39, 'U'): 18,
  (39, 'V'): 18,
  (39, 'W'): 18,
  (39, 'X'): 18,
  (39, 'Y'): 18,
  (39, 'Z'): 18,
  (39, '_'): 18,
  (39, 'a'): 18,
  (39, 'b'): 18,
  (39, 'c'): 18,
  (39, 'd'): 18,
  (39, 'e'): 18,
  (39, 'f'): 18,
  (39, 'g'): 18,
  (39, 'h'): 18,
  (39, 'i'): 18,
  (39, 'j'): 18,
  (39, 'k'): 18,
  (39, 'l'): 18,
  (39, 'm'): 18,
  (39, 'n'): 18,
  (39, 'o'): 18,
  (39, 'p'): 18,
  (39, 'q'): 18,
  (39, 'r'): 18,
  (39, 's'): 18,
  (39, 't'): 18,
  (39, 'u'): 40,
  (39, 'v'): 18,
  (39, 'w'): 18,
  (39, 'x'): 18,
  (39, 'y'): 18,
  (39, 'z'): 18,
  (40, '0'): 18,
  (40, '1'): 18,
  (40, '2'): 18,
  (40, '3'): 18,
  (40, '4'): 18,
  (40, '5'): 18,
  (40, '6'): 18,
  (40, '7'): 18,
  (40, '8'): 18,
  (40, '9'): 18,
  (40, '@'): 18,
  (40, 'A'): 18,
  (40, 'B'): 18,
  (40, 'C'): 18,
  (40, 'D'): 18,
  (40, 'E'): 18,
  (40, 'F'): 18,
  (40, 'G'): 18,
  (40, 'H'): 18,
  (40, 'I'): 18,
  (40, 'J'): 18,
  (40, 'K'): 18,
  (40, 'L'): 18,
  (40, 'M'): 18,
  (40, 'N'): 18,
  (40, 'O'): 18,
  (40, 'P'): 18,
  (40, 'Q'): 18,
  (40, 'R'): 18,
  (40, 'S'): 18,
  (40, 'T'): 18,
  (40, 'U'): 18,
  (40, 'V'): 18,
  (40, 'W'): 18,
  (40, 'X'): 18,
  (40, 'Y'): 18,
  (40, 'Z'): 18,
  (40, '_'): 18,
  (40, 'a'): 18,
  (40, 'b'): 18,
  (40, 'c'): 18,
  (40, 'd'): 18,
  (40, 'e'): 41,
  (40, 'f'): 18,
  (40, 'g'): 18,
  (40, 'h'): 18,
  (40, 'i'): 18,
  (40, 'j'): 18,
  (40, 'k'): 18,
  (40, 'l'): 18,
  (40, 'm'): 18,
  (40, 'n'): 18,
  (40, 'o'): 18,
  (40, 'p'): 18,
  (40, 'q'): 18,
  (40, 'r'): 18,
  (40, 's'): 18,
  (40, 't'): 18,
  (40, 'u'): 18,
  (40, 'v'): 18,
  (40, 'w'): 18,
  (40, 'x'): 18,
  (40, 'y'): 18,
  (40, 'z'): 18,
  (41, '0'): 18,
  (41, '1'): 18,
  (41, '2'): 18,
  (41, '3'): 18,
  (41, '4'): 18,
  (41, '5'): 18,
  (41, '6'): 18,
  (41, '7'): 18,
  (41, '8'): 18,
  (41, '9'): 18,
  (41, '@'): 18,
  (41, 'A'): 18,
  (41, 'B'): 18,
  (41, 'C'): 18,
  (41, 'D'): 18,
  (41, 'E'): 18,
  (41, 'F'): 18,
  (41, 'G'): 18,
  (41, 'H'): 18,
  (41, 'I'): 18,
  (41, 'J'): 18,
  (41, 'K'): 18,
  (41, 'L'): 18,
  (41, 'M'): 18,
  (41, 'N'): 18,
  (41, 'O'): 18,
  (41, 'P'): 18,
  (41, 'Q'): 18,
  (41, 'R'): 18,
  (41, 'S'): 18,
  (41, 'T'): 18,
  (41, 'U'): 18,
  (41, 'V'): 18,
  (41, 'W'): 18,
  (41, 'X'): 18,
  (41, 'Y'): 18,
  (41, 'Z'): 18,
  (41, '_'): 18,
  (41, 'a'): 18,
  (41, 'b'): 18,
  (41, 'c'): 18,
  (41, 'd'): 18,
  (41, 'e'): 18,
  (41, 'f'): 18,
  (41, 'g'): 18,
  (41, 'h'): 18,
  (41, 'i'): 18,
  (41, 'j'): 18,
  (41, 'k'): 18,
  (41, 'l'): 18,
  (41, 'm'): 18,
  (41, 'n'): 18,
  (41, 'o'): 18,
  (41, 'p'): 18,
  (41, 'q'): 18,
  (41, 'r'): 18,
  (41, 's'): 18,
  (41, 't'): 18,
  (41, 'u'): 18,
  (41, 'v'): 18,
  (41, 'w'): 18,
  (41, 'x'): 18,
  (41, 'y'): 18,
  (41, 'z'): 18,
  (42, '0'): 18,
  (42, '1'): 18,
  (42, '2'): 18,
  (42, '3'): 18,
  (42, '4'): 18,
  (42, '5'): 18,
  (42, '6'): 18,
  (42, '7'): 18,
  (42, '8'): 18,
  (42, '9'): 18,
  (42, '@'): 18,
  (42, 'A'): 18,
  (42, 'B'): 18,
  (42, 'C'): 18,
  (42, 'D'): 18,
  (42, 'E'): 18,
  (42, 'F'): 18,
  (42, 'G'): 18,
  (42, 'H'): 18,
  (42, 'I'): 18,
  (42, 'J'): 18,
  (42, 'K'): 18,
  (42, 'L'): 18,
  (42, 'M'): 18,
  (42, 'N'): 18,
  (42, 'O'): 18,
  (42, 'P'): 18,
  (42, 'Q'): 18,
  (42, 'R'): 18,
  (42, 'S'): 18,
  (42, 'T'): 18,
  (42, 'U'): 18,
  (42, 'V'): 18,
  (42, 'W'): 18,
  (42, 'X'): 18,
  (42, 'Y'): 18,
  (42, 'Z'): 18,
  (42, '_'): 18,
  (42, 'a'): 18,
  (42, 'b'): 18,
  (42, 'c'): 18,
  (42, 'd'): 18,
  (42, 'e'): 18,
  (42, 'f'): 18,
  (42, 'g'): 18,
  (42, 'h'): 18,
  (42, 'i'): 18,
  (42, 'j'): 18,
  (42, 'k'): 18,
  (42, 'l'): 18,
  (42, 'm'): 18,
  (42, 'n'): 18,
  (42, 'o'): 18,
  (42, 'p'): 18,
  (42, 'q'): 18,
  (42, 'r'): 18,
  (42, 's'): 18,
  (42, 't'): 43,
  (42, 'u'): 18,
  (42, 'v'): 18,
  (42, 'w'): 18,
  (42, 'x'): 18,
  (42, 'y'): 18,
  (42, 'z'): 18,
  (43, '0'): 18,
  (43, '1'): 18,
  (43, '2'): 18,
  (43, '3'): 18,
  (43, '4'): 18,
  (43, '5'): 18,
  (43, '6'): 18,
  (43, '7'): 18,
  (43, '8'): 18,
  (43, '9'): 18,
  (43, '@'): 18,
  (43, 'A'): 18,
  (43, 'B'): 18,
  (43, 'C'): 18,
  (43, 'D'): 18,
  (43, 'E'): 18,
  (43, 'F'): 18,
  (43, 'G'): 18,
  (43, 'H'): 18,
  (43, 'I'): 18,
  (43, 'J'): 18,
  (43, 'K'): 18,
  (43, 'L'): 18,
  (43, 'M'): 18,
  (43, 'N'): 18,
  (43, 'O'): 18,
  (43, 'P'): 18,
  (43, 'Q'): 18,
  (43, 'R'): 18,
  (43, 'S'): 18,
  (43, 'T'): 18,
  (43, 'U'): 18,
  (43, 'V'): 18,
  (43, 'W'): 18,
  (43, 'X'): 18,
  (43, 'Y'): 18,
  (43, 'Z'): 18,
  (43, '_'): 18,
  (43, 'a'): 18,
  (43, 'b'): 18,
  (43, 'c'): 18,
  (43, 'd'): 18,
  (43, 'e'): 18,
  (43, 'f'): 18,
  (43, 'g'): 18,
  (43, 'h'): 18,
  (43, 'i'): 18,
  (43, 'j'): 18,
  (43, 'k'): 18,
  (43, 'l'): 18,
  (43, 'm'): 18,
  (43, 'n'): 18,
  (43, 'o'): 18,
  (43, 'p'): 18,
  (43, 'q'): 18,
  (43, 'r'): 18,
  (43, 's'): 18,
  (43, 't'): 18,
  (43, 'u'): 44,
  (43, 'v'): 18,
  (43, 'w'): 18,
  (43, 'x'): 18,
  (43, 'y'): 18,
  (43, 'z'): 18,
  (44, '0'): 18,
  (44, '1'): 18,
  (44, '2'): 18,
  (44, '3'): 18,
  (44, '4'): 18,
  (44, '5'): 18,
  (44, '6'): 18,
  (44, '7'): 18,
  (44, '8'): 18,
  (44, '9'): 18,
  (44, '@'): 18,
  (44, 'A'): 18,
  (44, 'B'): 18,
  (44, 'C'): 18,
  (44, 'D'): 18,
  (44, 'E'): 18,
  (44, 'F'): 18,
  (44, 'G'): 18,
  (44, 'H'): 18,
  (44, 'I'): 18,
  (44, 'J'): 18,
  (44, 'K'): 18,
  (44, 'L'): 18,
  (44, 'M'): 18,
  (44, 'N'): 18,
  (44, 'O'): 18,
  (44, 'P'): 18,
  (44, 'Q'): 18,
  (44, 'R'): 18,
  (44, 'S'): 18,
  (44, 'T'): 18,
  (44, 'U'): 18,
  (44, 'V'): 18,
  (44, 'W'): 18,
  (44, 'X'): 18,
  (44, 'Y'): 18,
  (44, 'Z'): 18,
  (44, '_'): 18,
  (44, 'a'): 18,
  (44, 'b'): 18,
  (44, 'c'): 18,
  (44, 'd'): 18,
  (44, 'e'): 18,
  (44, 'f'): 18,
  (44, 'g'): 18,
  (44, 'h'): 18,
  (44, 'i'): 18,
  (44, 'j'): 18,
  (44, 'k'): 18,
  (44, 'l'): 18,
  (44, 'm'): 18,
  (44, 'n'): 18,
  (44, 'o'): 18,
  (44, 'p'): 18,
  (44, 'q'): 18,
  (44, 'r'): 45,
  (44, 's'): 18,
  (44, 't'): 18,
  (44, 'u'): 18,
  (44, 'v'): 18,
  (44, 'w'): 18,
  (44, 'x'): 18,
  (44, 'y'): 18,
  (44, 'z'): 18,
  (45, '0'): 18,
  (45, '1'): 18,
  (45, '2'): 18,
  (45, '3'): 18,
  (45, '4'): 18,
  (45, '5'): 18,
  (45, '6'): 18,
  (45, '7'): 18,
  (45, '8'): 18,
  (45, '9'): 18,
  (45, '@'): 18,
  (45, 'A'): 18,
  (45, 'B'): 18,
  (45, 'C'): 18,
  (45, 'D'): 18,
  (45, 'E'): 18,
  (45, 'F'): 18,
  (45, 'G'): 18,
  (45, 'H'): 18,
  (45, 'I'): 18,
  (45, 'J'): 18,
  (45, 'K'): 18,
  (45, 'L'): 18,
  (45, 'M'): 18,
  (45, 'N'): 18,
  (45, 'O'): 18,
  (45, 'P'): 18,
  (45, 'Q'): 18,
  (45, 'R'): 18,
  (45, 'S'): 18,
  (45, 'T'): 18,
  (45, 'U'): 18,
  (45, 'V'): 18,
  (45, 'W'): 18,
  (45, 'X'): 18,
  (45, 'Y'): 18,
  (45, 'Z'): 18,
  (45, '_'): 18,
  (45, 'a'): 18,
  (45, 'b'): 18,
  (45, 'c'): 18,
  (45, 'd'): 18,
  (45, 'e'): 18,
  (45, 'f'): 18,
  (45, 'g'): 18,
  (45, 'h'): 18,
  (45, 'i'): 18,
  (45, 'j'): 18,
  (45, 'k'): 18,
  (45, 'l'): 18,
  (45, 'm'): 18,
  (45, 'n'): 46,
  (45, 'o'): 18,
  (45, 'p'): 18,
  (45, 'q'): 18,
  (45, 'r'): 18,
  (45, 's'): 18,
  (45, 't'): 18,
  (45, 'u'): 18,
  (45, 'v'): 18,
  (45, 'w'): 18,
  (45, 'x'): 18,
  (45, 'y'): 18,
  (45, 'z'): 18,
  (46, '0'): 18,
  (46, '1'): 18,
  (46, '2'): 18,
  (46, '3'): 18,
  (46, '4'): 18,
  (46, '5'): 18,
  (46, '6'): 18,
  (46, '7'): 18,
  (46, '8'): 18,
  (46, '9'): 18,
  (46, '@'): 18,
  (46, 'A'): 18,
  (46, 'B'): 18,
  (46, 'C'): 18,
  (46, 'D'): 18,
  (46, 'E'): 18,
  (46, 'F'): 18,
  (46, 'G'): 18,
  (46, 'H'): 18,
  (46, 'I'): 18,
  (46, 'J'): 18,
  (46, 'K'): 18,
  (46, 'L'): 18,
  (46, 'M'): 18,
  (46, 'N'): 18,
  (46, 'O'): 18,
  (46, 'P'): 18,
  (46, 'Q'): 18,
  (46, 'R'): 18,
  (46, 'S'): 18,
  (46, 'T'): 18,
  (46, 'U'): 18,
  (46, 'V'): 18,
  (46, 'W'): 18,
  (46, 'X'): 18,
  (46, 'Y'): 18,
  (46, 'Z'): 18,
  (46, '_'): 18,
  (46, 'a'): 18,
  (46, 'b'): 18,
  (46, 'c'): 18,
  (46, 'd'): 18,
  (46, 'e'): 18,
  (46, 'f'): 18,
  (46, 'g'): 18,
  (46, 'h'): 18,
  (46, 'i'): 18,
  (46, 'j'): 18,
  (46, 'k'): 18,
  (46, 'l'): 18,
  (46, 'm'): 18,
  (46, 'n'): 18,
  (46, 'o'): 18,
  (46, 'p'): 18,
  (46, 'q'): 18,
  (46, 'r'): 18,
  (46, 's'): 18,
  (46, 't'): 18,
  (46, 'u'): 18,
  (46, 'v'): 18,
  (46, 'w'): 18,
  (46, 'x'): 18,
  (46, 'y'): 18,
  (46, 'z'): 18,
  (47, '0'): 18,
  (47, '1'): 18,
  (47, '2'): 18,
  (47, '3'): 18,
  (47, '4'): 18,
  (47, '5'): 18,
  (47, '6'): 18,
  (47, '7'): 18,
  (47, '8'): 18,
  (47, '9'): 18,
  (47, '@'): 18,
  (47, 'A'): 18,
  (47, 'B'): 18,
  (47, 'C'): 18,
  (47, 'D'): 18,
  (47, 'E'): 18,
  (47, 'F'): 18,
  (47, 'G'): 18,
  (47, 'H'): 18,
  (47, 'I'): 18,
  (47, 'J'): 18,
  (47, 'K'): 18,
  (47, 'L'): 18,
  (47, 'M'): 18,
  (47, 'N'): 18,
  (47, 'O'): 18,
  (47, 'P'): 18,
  (47, 'Q'): 18,
  (47, 'R'): 18,
  (47, 'S'): 18,
  (47, 'T'): 18,
  (47, 'U'): 18,
  (47, 'V'): 18,
  (47, 'W'): 18,
  (47, 'X'): 18,
  (47, 'Y'): 18,
  (47, 'Z'): 18,
  (47, '_'): 18,
  (47, 'a'): 18,
  (47, 'b'): 18,
  (47, 'c'): 18,
  (47, 'd'): 18,
  (47, 'e'): 18,
  (47, 'f'): 18,
  (47, 'g'): 18,
  (47, 'h'): 18,
  (47, 'i'): 18,
  (47, 'j'): 18,
  (47, 'k'): 18,
  (47, 'l'): 18,
  (47, 'm'): 18,
  (47, 'n'): 18,
  (47, 'o'): 18,
  (47, 'p'): 18,
  (47, 'q'): 18,
  (47, 'r'): 18,
  (47, 's'): 18,
  (47, 't'): 48,
  (47, 'u'): 18,
  (47, 'v'): 18,
  (47, 'w'): 18,
  (47, 'x'): 18,
  (47, 'y'): 18,
  (47, 'z'): 18,
  (48, '0'): 18,
  (48, '1'): 18,
  (48, '2'): 18,
  (48, '3'): 18,
  (48, '4'): 18,
  (48, '5'): 18,
  (48, '6'): 18,
  (48, '7'): 18,
  (48, '8'): 18,
  (48, '9'): 18,
  (48, '@'): 18,
  (48, 'A'): 18,
  (48, 'B'): 18,
  (48, 'C'): 18,
  (48, 'D'): 18,
  (48, 'E'): 18,
  (48, 'F'): 18,
  (48, 'G'): 18,
  (48, 'H'): 18,
  (48, 'I'): 18,
  (48, 'J'): 18,
  (48, 'K'): 18,
  (48, 'L'): 18,
  (48, 'M'): 18,
  (48, 'N'): 18,
  (48, 'O'): 18,
  (48, 'P'): 18,
  (48, 'Q'): 18,
  (48, 'R'): 18,
  (48, 'S'): 18,
  (48, 'T'): 18,
  (48, 'U'): 18,
  (48, 'V'): 18,
  (48, 'W'): 18,
  (48, 'X'): 18,
  (48, 'Y'): 18,
  (48, 'Z'): 18,
  (48, '_'): 18,
  (48, 'a'): 18,
  (48, 'b'): 18,
  (48, 'c'): 18,
  (48, 'd'): 18,
  (48, 'e'): 18,
  (48, 'f'): 18,
  (48, 'g'): 18,
  (48, 'h'): 18,
  (48, 'i'): 18,
  (48, 'j'): 18,
  (48, 'k'): 18,
  (48, 'l'): 18,
  (48, 'm'): 18,
  (48, 'n'): 18,
  (48, 'o'): 18,
  (48, 'p'): 18,
  (48, 'q'): 18,
  (48, 'r'): 18,
  (48, 's'): 18,
  (48, 't'): 18,
  (48, 'u'): 18,
  (48, 'v'): 18,
  (48, 'w'): 18,
  (48, 'x'): 18,
  (48, 'y'): 18,
  (48, 'z'): 18,
  (49, '0'): 18,
  (49, '1'): 18,
  (49, '2'): 18,
  (49, '3'): 18,
  (49, '4'): 18,
  (49, '5'): 18,
  (49, '6'): 18,
  (49, '7'): 18,
  (49, '8'): 18,
  (49, '9'): 18,
  (49, '@'): 18,
  (49, 'A'): 18,
  (49, 'B'): 18,
  (49, 'C'): 18,
  (49, 'D'): 18,
  (49, 'E'): 18,
  (49, 'F'): 18,
  (49, 'G'): 18,
  (49, 'H'): 18,
  (49, 'I'): 18,
  (49, 'J'): 18,
  (49, 'K'): 18,
  (49, 'L'): 18,
  (49, 'M'): 18,
  (49, 'N'): 18,
  (49, 'O'): 18,
  (49, 'P'): 18,
  (49, 'Q'): 18,
  (49, 'R'): 18,
  (49, 'S'): 18,
  (49, 'T'): 18,
  (49, 'U'): 18,
  (49, 'V'): 18,
  (49, 'W'): 18,
  (49, 'X'): 18,
  (49, 'Y'): 18,
  (49, 'Z'): 18,
  (49, '_'): 18,
  (49, 'a'): 18,
  (49, 'b'): 18,
  (49, 'c'): 18,
  (49, 'd'): 18,
  (49, 'e'): 18,
  (49, 'f'): 18,
  (49, 'g'): 18,
  (49, 'h'): 18,
  (49, 'i'): 18,
  (49, 'j'): 18,
  (49, 'k'): 18,
  (49, 'l'): 18,
  (49, 'm'): 18,
  (49, 'n'): 18,
  (49, 'o'): 18,
  (49, 'p'): 18,
  (49, 'q'): 18,
  (49, 'r'): 18,
  (49, 's'): 18,
  (49, 't'): 18,
  (49, 'u'): 18,
  (49, 'v'): 18,
  (49, 'w'): 18,
  (49, 'x'): 18,
  (49, 'y'): 18,
  (49, 'z'): 18,
  (50, '0'): 18,
  (50, '1'): 18,
  (50, '2'): 18,
  (50, '3'): 18,
  (50, '4'): 18,
  (50, '5'): 18,
  (50, '6'): 18,
  (50, '7'): 18,
  (50, '8'): 18,
  (50, '9'): 18,
  (50, '@'): 18,
  (50, 'A'): 18,
  (50, 'B'): 18,
  (50, 'C'): 18,
  (50, 'D'): 18,
  (50, 'E'): 18,
  (50, 'F'): 18,
  (50, 'G'): 18,
  (50, 'H'): 18,
  (50, 'I'): 18,
  (50, 'J'): 18,
  (50, 'K'): 18,
  (50, 'L'): 18,
  (50, 'M'): 18,
  (50, 'N'): 18,
  (50, 'O'): 18,
  (50, 'P'): 18,
  (50, 'Q'): 18,
  (50, 'R'): 18,
  (50, 'S'): 18,
  (50, 'T'): 18,
  (50, 'U'): 18,
  (50, 'V'): 18,
  (50, 'W'): 18,
  (50, 'X'): 18,
  (50, 'Y'): 18,
  (50, 'Z'): 18,
  (50, '_'): 18,
  (50, 'a'): 18,
  (50, 'b'): 18,
  (50, 'c'): 18,
  (50, 'd'): 18,
  (50, 'e'): 18,
  (50, 'f'): 18,
  (50, 'g'): 18,
  (50, 'h'): 18,
  (50, 'i'): 18,
  (50, 'j'): 18,
  (50, 'k'): 18,
  (50, 'l'): 18,
  (50, 'm'): 18,
  (50, 'n'): 18,
  (50, 'o'): 18,
  (50, 'p'): 18,
  (50, 'q'): 18,
  (50, 'r'): 18,
  (50, 's'): 18,
  (50, 't'): 51,
  (50, 'u'): 18,
  (50, 'v'): 18,
  (50, 'w'): 18,
  (50, 'x'): 18,
  (50, 'y'): 18,
  (50, 'z'): 18,
  (51, '0'): 18,
  (51, '1'): 18,
  (51, '2'): 18,
  (51, '3'): 18,
  (51, '4'): 18,
  (51, '5'): 18,
  (51, '6'): 18,
  (51, '7'): 18,
  (51, '8'): 18,
  (51, '9'): 18,
  (51, '@'): 18,
  (51, 'A'): 18,
  (51, 'B'): 18,
  (51, 'C'): 18,
  (51, 'D'): 18,
  (51, 'E'): 18,
  (51, 'F'): 18,
  (51, 'G'): 18,
  (51, 'H'): 18,
  (51, 'I'): 18,
  (51, 'J'): 18,
  (51, 'K'): 18,
  (51, 'L'): 18,
  (51, 'M'): 18,
  (51, 'N'): 18,
  (51, 'O'): 18,
  (51, 'P'): 18,
  (51, 'Q'): 18,
  (51, 'R'): 18,
  (51, 'S'): 18,
  (51, 'T'): 18,
  (51, 'U'): 18,
  (51, 'V'): 18,
  (51, 'W'): 18,
  (51, 'X'): 18,
  (51, 'Y'): 18,
  (51, 'Z'): 18,
  (51, '_'): 18,
  (51, 'a'): 18,
  (51, 'b'): 18,
  (51, 'c'): 18,
  (51, 'd'): 18,
  (51, 'e'): 18,
  (51, 'f'): 18,
  (51, 'g'): 18,
  (51, 'h'): 18,
  (51, 'i'): 18,
  (51, 'j'): 18,
  (51, 'k'): 18,
  (51, 'l'): 18,
  (51, 'm'): 18,
  (51, 'n'): 18,
  (51, 'o'): 18,
  (51, 'p'): 18,
  (51, 'q'): 18,
  (51, 'r'): 18,
  (51, 's'): 18,
  (51, 't'): 18,
  (51, 'u'): 18,
  (51, 'v'): 18,
  (51, 'w'): 18,
  (51, 'x'): 18,
  (51, 'y'): 18,
  (51, 'z'): 18,
  (52, '0'): 18,
  (52, '1'): 18,
  (52, '2'): 18,
  (52, '3'): 18,
  (52, '4'): 18,
  (52, '5'): 18,
  (52, '6'): 18,
  (52, '7'): 18,
  (52, '8'): 18,
  (52, '9'): 18,
  (52, '@'): 18,
  (52, 'A'): 18,
  (52, 'B'): 18,
  (52, 'C'): 18,
  (52, 'D'): 18,
  (52, 'E'): 18,
  (52, 'F'): 18,
  (52, 'G'): 18,
  (52, 'H'): 18,
  (52, 'I'): 18,
  (52, 'J'): 18,
  (52, 'K'): 18,
  (52, 'L'): 18,
  (52, 'M'): 18,
  (52, 'N'): 18,
  (52, 'O'): 18,
  (52, 'P'): 18,
  (52, 'Q'): 18,
  (52, 'R'): 18,
  (52, 'S'): 18,
  (52, 'T'): 18,
  (52, 'U'): 18,
  (52, 'V'): 18,
  (52, 'W'): 18,
  (52, 'X'): 18,
  (52, 'Y'): 18,
  (52, 'Z'): 18,
  (52, '_'): 18,
  (52, 'a'): 18,
  (52, 'b'): 18,
  (52, 'c'): 18,
  (52, 'd'): 18,
  (52, 'e'): 18,
  (52, 'f'): 18,
  (52, 'g'): 18,
  (52, 'h'): 18,
  (52, 'i'): 18,
  (52, 'j'): 18,
  (52, 'k'): 18,
  (52, 'l'): 18,
  (52, 'm'): 18,
  (52, 'n'): 18,
  (52, 'o'): 18,
  (52, 'p'): 18,
  (52, 'q'): 18,
  (52, 'r'): 18,
  (52, 's'): 18,
  (52, 't'): 18,
  (52, 'u'): 18,
  (52, 'v'): 18,
  (52, 'w'): 18,
  (52, 'x'): 18,
  (52, 'y'): 18,
  (52, 'z'): 18,
  (53, '0'): 18,
  (53, '1'): 18,
  (53, '2'): 18,
  (53, '3'): 18,
  (53, '4'): 18,
  (53, '5'): 18,
  (53, '6'): 18,
  (53, '7'): 18,
  (53, '8'): 18,
  (53, '9'): 18,
  (53, '@'): 18,
  (53, 'A'): 18,
  (53, 'B'): 18,
  (53, 'C'): 18,
  (53, 'D'): 18,
  (53, 'E'): 18,
  (53, 'F'): 18,
  (53, 'G'): 18,
  (53, 'H'): 18,
  (53, 'I'): 18,
  (53, 'J'): 18,
  (53, 'K'): 18,
  (53, 'L'): 18,
  (53, 'M'): 18,
  (53, 'N'): 18,
  (53, 'O'): 18,
  (53, 'P'): 18,
  (53, 'Q'): 18,
  (53, 'R'): 18,
  (53, 'S'): 18,
  (53, 'T'): 18,
  (53, 'U'): 18,
  (53, 'V'): 18,
  (53, 'W'): 18,
  (53, 'X'): 18,
  (53, 'Y'): 18,
  (53, 'Z'): 18,
  (53, '_'): 18,
  (53, 'a'): 18,
  (53, 'b'): 18,
  (53, 'c'): 18,
  (53, 'd'): 18,
  (53, 'e'): 18,
  (53, 'f'): 18,
  (53, 'g'): 18,
  (53, 'h'): 18,
  (53, 'i'): 18,
  (53, 'j'): 18,
  (53, 'k'): 18,
  (53, 'l'): 55,
  (53, 'm'): 18,
  (53, 'n'): 18,
  (53, 'o'): 18,
  (53, 'p'): 18,
  (53, 'q'): 18,
  (53, 'r'): 18,
  (53, 's'): 18,
  (53, 't'): 18,
  (53, 'u'): 18,
  (53, 'v'): 18,
  (53, 'w'): 18,
  (53, 'x'): 18,
  (53, 'y'): 18,
  (53, 'z'): 18,
  (54, '0'): 18,
  (54, '1'): 18,
  (54, '2'): 18,
  (54, '3'): 18,
  (54, '4'): 18,
  (54, '5'): 18,
  (54, '6'): 18,
  (54, '7'): 18,
  (54, '8'): 18,
  (54, '9'): 18,
  (54, '@'): 18,
  (54, 'A'): 18,
  (54, 'B'): 18,
  (54, 'C'): 18,
  (54, 'D'): 18,
  (54, 'E'): 18,
  (54, 'F'): 18,
  (54, 'G'): 18,
  (54, 'H'): 18,
  (54, 'I'): 18,
  (54, 'J'): 18,
  (54, 'K'): 18,
  (54, 'L'): 18,
  (54, 'M'): 18,
  (54, 'N'): 18,
  (54, 'O'): 18,
  (54, 'P'): 18,
  (54, 'Q'): 18,
  (54, 'R'): 18,
  (54, 'S'): 18,
  (54, 'T'): 18,
  (54, 'U'): 18,
  (54, 'V'): 18,
  (54, 'W'): 18,
  (54, 'X'): 18,
  (54, 'Y'): 18,
  (54, 'Z'): 18,
  (54, '_'): 18,
  (54, 'a'): 18,
  (54, 'b'): 18,
  (54, 'c'): 18,
  (54, 'd'): 18,
  (54, 'e'): 18,
  (54, 'f'): 18,
  (54, 'g'): 18,
  (54, 'h'): 18,
  (54, 'i'): 18,
  (54, 'j'): 18,
  (54, 'k'): 18,
  (54, 'l'): 18,
  (54, 'm'): 18,
  (54, 'n'): 18,
  (54, 'o'): 18,
  (54, 'p'): 18,
  (54, 'q'): 18,
  (54, 'r'): 18,
  (54, 's'): 18,
  (54, 't'): 18,
  (54, 'u'): 18,
  (54, 'v'): 18,
  (54, 'w'): 18,
  (54, 'x'): 18,
  (54, 'y'): 18,
  (54, 'z'): 18,
  (55, '0'): 18,
  (55, '1'): 18,
  (55, '2'): 18,
  (55, '3'): 18,
  (55, '4'): 18,
  (55, '5'): 18,
  (55, '6'): 18,
  (55, '7'): 18,
  (55, '8'): 18,
  (55, '9'): 18,
  (55, '@'): 18,
  (55, 'A'): 18,
  (55, 'B'): 18,
  (55, 'C'): 18,
  (55, 'D'): 18,
  (55, 'E'): 18,
  (55, 'F'): 18,
  (55, 'G'): 18,
  (55, 'H'): 18,
  (55, 'I'): 18,
  (55, 'J'): 18,
  (55, 'K'): 18,
  (55, 'L'): 18,
  (55, 'M'): 18,
  (55, 'N'): 18,
  (55, 'O'): 18,
  (55, 'P'): 18,
  (55, 'Q'): 18,
  (55, 'R'): 18,
  (55, 'S'): 18,
  (55, 'T'): 18,
  (55, 'U'): 18,
  (55, 'V'): 18,
  (55, 'W'): 18,
  (55, 'X'): 18,
  (55, 'Y'): 18,
  (55, 'Z'): 18,
  (55, '_'): 18,
  (55, 'a'): 18,
  (55, 'b'): 18,
  (55, 'c'): 18,
  (55, 'd'): 18,
  (55, 'e'): 18,
  (55, 'f'): 18,
  (55, 'g'): 18,
  (55, 'h'): 18,
  (55, 'i'): 18,
  (55, 'j'): 18,
  (55, 'k'): 18,
  (55, 'l'): 18,
  (55, 'm'): 18,
  (55, 'n'): 18,
  (55, 'o'): 18,
  (55, 'p'): 18,
  (55, 'q'): 18,
  (55, 'r'): 18,
  (55, 's'): 40,
  (55, 't'): 18,
  (55, 'u'): 18,
  (55, 'v'): 18,
  (55, 'w'): 18,
  (55, 'x'): 18,
  (55, 'y'): 18,
  (55, 'z'): 18,
  (56, '0'): 18,
  (56, '1'): 18,
  (56, '2'): 18,
  (56, '3'): 18,
  (56, '4'): 18,
  (56, '5'): 18,
  (56, '6'): 18,
  (56, '7'): 18,
  (56, '8'): 18,
  (56, '9'): 18,
  (56, '@'): 18,
  (56, 'A'): 18,
  (56, 'B'): 18,
  (56, 'C'): 18,
  (56, 'D'): 18,
  (56, 'E'): 18,
  (56, 'F'): 18,
  (56, 'G'): 18,
  (56, 'H'): 18,
  (56, 'I'): 18,
  (56, 'J'): 18,
  (56, 'K'): 18,
  (56, 'L'): 18,
  (56, 'M'): 18,
  (56, 'N'): 18,
  (56, 'O'): 18,
  (56, 'P'): 18,
  (56, 'Q'): 18,
  (56, 'R'): 18,
  (56, 'S'): 18,
  (56, 'T'): 18,
  (56, 'U'): 18,
  (56, 'V'): 18,
  (56, 'W'): 18,
  (56, 'X'): 18,
  (56, 'Y'): 18,
  (56, 'Z'): 18,
  (56, '_'): 18,
  (56, 'a'): 18,
  (56, 'b'): 18,
  (56, 'c'): 18,
  (56, 'd'): 18,
  (56, 'e'): 18,
  (56, 'f'): 18,
  (56, 'g'): 18,
  (56, 'h'): 18,
  (56, 'i'): 18,
  (56, 'j'): 18,
  (56, 'k'): 18,
  (56, 'l'): 18,
  (56, 'm'): 18,
  (56, 'n'): 18,
  (56, 'o'): 18,
  (56, 'p'): 18,
  (56, 'q'): 18,
  (56, 'r'): 18,
  (56, 's'): 18,
  (56, 't'): 18,
  (56, 'u'): 18,
  (56, 'v'): 18,
  (56, 'w'): 18,
  (56, 'x'): 18,
  (56, 'y'): 18,
  (56, 'z'): 18,
  (57, '0'): 18,
  (57, '1'): 18,
  (57, '2'): 18,
  (57, '3'): 18,
  (57, '4'): 18,
  (57, '5'): 18,
  (57, '6'): 18,
  (57, '7'): 18,
  (57, '8'): 18,
  (57, '9'): 18,
  (57, '@'): 18,
  (57, 'A'): 18,
  (57, 'B'): 18,
  (57, 'C'): 18,
  (57, 'D'): 18,
  (57, 'E'): 18,
  (57, 'F'): 18,
  (57, 'G'): 18,
  (57, 'H'): 18,
  (57, 'I'): 18,
  (57, 'J'): 18,
  (57, 'K'): 18,
  (57, 'L'): 18,
  (57, 'M'): 18,
  (57, 'N'): 18,
  (57, 'O'): 18,
  (57, 'P'): 18,
  (57, 'Q'): 18,
  (57, 'R'): 18,
  (57, 'S'): 18,
  (57, 'T'): 18,
  (57, 'U'): 18,
  (57, 'V'): 18,
  (57, 'W'): 18,
  (57, 'X'): 18,
  (57, 'Y'): 18,
  (57, 'Z'): 18,
  (57, '_'): 18,
  (57, 'a'): 18,
  (57, 'b'): 18,
  (57, 'c'): 18,
  (57, 'd'): 18,
  (57, 'e'): 18,
  (57, 'f'): 18,
  (57, 'g'): 18,
  (57, 'h'): 18,
  (57, 'i'): 18,
  (57, 'j'): 18,
  (57, 'k'): 18,
  (57, 'l'): 18,
  (57, 'm'): 18,
  (57, 'n'): 18,
  (57, 'o'): 18,
  (57, 'p'): 18,
  (57, 'q'): 18,
  (57, 'r'): 18,
  (57, 's'): 58,
  (57, 't'): 18,
  (57, 'u'): 18,
  (57, 'v'): 18,
  (57, 'w'): 18,
  (57, 'x'): 18,
  (57, 'y'): 18,
  (57, 'z'): 18,
  (58, '0'): 18,
  (58, '1'): 18,
  (58, '2'): 18,
  (58, '3'): 18,
  (58, '4'): 18,
  (58, '5'): 18,
  (58, '6'): 18,
  (58, '7'): 18,
  (58, '8'): 18,
  (58, '9'): 18,
  (58, '@'): 18,
  (58, 'A'): 18,
  (58, 'B'): 18,
  (58, 'C'): 18,
  (58, 'D'): 18,
  (58, 'E'): 18,
  (58, 'F'): 18,
  (58, 'G'): 18,
  (58, 'H'): 18,
  (58, 'I'): 18,
  (58, 'J'): 18,
  (58, 'K'): 18,
  (58, 'L'): 18,
  (58, 'M'): 18,
  (58, 'N'): 18,
  (58, 'O'): 18,
  (58, 'P'): 18,
  (58, 'Q'): 18,
  (58, 'R'): 18,
  (58, 'S'): 18,
  (58, 'T'): 18,
  (58, 'U'): 18,
  (58, 'V'): 18,
  (58, 'W'): 18,
  (58, 'X'): 18,
  (58, 'Y'): 18,
  (58, 'Z'): 18,
  (58, '_'): 18,
  (58, 'a'): 18,
  (58, 'b'): 18,
  (58, 'c'): 18,
  (58, 'd'): 18,
  (58, 'e'): 59,
  (58, 'f'): 18,
  (58, 'g'): 18,
  (58, 'h'): 18,
  (58, 'i'): 18,
  (58, 'j'): 18,
  (58, 'k'): 18,
  (58, 'l'): 18,
  (58, 'm'): 18,
  (58, 'n'): 18,
  (58, 'o'): 18,
  (58, 'p'): 18,
  (58, 'q'): 18,
  (58, 'r'): 18,
  (58, 's'): 18,
  (58, 't'): 18,
  (58, 'u'): 18,
  (58, 'v'): 18,
  (58, 'w'): 18,
  (58, 'x'): 18,
  (58, 'y'): 18,
  (58, 'z'): 18,
  (59, '0'): 18,
  (59, '1'): 18,
  (59, '2'): 18,
  (59, '3'): 18,
  (59, '4'): 18,
  (59, '5'): 18,
  (59, '6'): 18,
  (59, '7'): 18,
  (59, '8'): 18,
  (59, '9'): 18,
  (59, '@'): 18,
  (59, 'A'): 18,
  (59, 'B'): 18,
  (59, 'C'): 18,
  (59, 'D'): 18,
  (59, 'E'): 18,
  (59, 'F'): 18,
  (59, 'G'): 18,
  (59, 'H'): 18,
  (59, 'I'): 18,
  (59, 'J'): 18,
  (59, 'K'): 18,
  (59, 'L'): 18,
  (59, 'M'): 18,
  (59, 'N'): 18,
  (59, 'O'): 18,
  (59, 'P'): 18,
  (59, 'Q'): 18,
  (59, 'R'): 18,
  (59, 'S'): 18,
  (59, 'T'): 18,
  (59, 'U'): 18,
  (59, 'V'): 18,
  (59, 'W'): 18,
  (59, 'X'): 18,
  (59, 'Y'): 18,
  (59, 'Z'): 18,
  (59, '_'): 18,
  (59, 'a'): 18,
  (59, 'b'): 18,
  (59, 'c'): 18,
  (59, 'd'): 18,
  (59, 'e'): 18,
  (59, 'f'): 18,
  (59, 'g'): 18,
  (59, 'h'): 18,
  (59, 'i'): 18,
  (59, 'j'): 18,
  (59, 'k'): 18,
  (59, 'l'): 18,
  (59, 'm'): 18,
  (59, 'n'): 18,
  (59, 'o'): 18,
  (59, 'p'): 18,
  (59, 'q'): 18,
  (59, 'r'): 18,
  (59, 's'): 18,
  (59, 't'): 18,
  (59, 'u'): 18,
  (59, 'v'): 18,
  (59, 'w'): 18,
  (59, 'x'): 18,
  (59, 'y'): 18,
  (59, 'z'): 18,
  (60, '0'): 18,
  (60, '1'): 18,
  (60, '2'): 18,
  (60, '3'): 18,
  (60, '4'): 18,
  (60, '5'): 18,
  (60, '6'): 18,
  (60, '7'): 18,
  (60, '8'): 18,
  (60, '9'): 18,
  (60, '@'): 18,
  (60, 'A'): 18,
  (60, 'B'): 18,
  (60, 'C'): 18,
  (60, 'D'): 18,
  (60, 'E'): 18,
  (60, 'F'): 18,
  (60, 'G'): 18,
  (60, 'H'): 18,
  (60, 'I'): 18,
  (60, 'J'): 18,
  (60, 'K'): 18,
  (60, 'L'): 18,
  (60, 'M'): 18,
  (60, 'N'): 18,
  (60, 'O'): 18,
  (60, 'P'): 18,
  (60, 'Q'): 18,
  (60, 'R'): 18,
  (60, 'S'): 18,
  (60, 'T'): 18,
  (60, 'U'): 18,
  (60, 'V'): 18,
  (60, 'W'): 18,
  (60, 'X'): 18,
  (60, 'Y'): 18,
  (60, 'Z'): 18,
  (60, '_'): 18,
  (60, 'a'): 18,
  (60, 'b'): 18,
  (60, 'c'): 18,
  (60, 'd'): 61,
  (60, 'e'): 18,
  (60, 'f'): 18,
  (60, 'g'): 18,
  (60, 'h'): 18,
  (60, 'i'): 18,
  (60, 'j'): 18,
  (60, 'k'): 18,
  (60, 'l'): 18,
  (60, 'm'): 18,
  (60, 'n'): 18,
  (60, 'o'): 18,
  (60, 'p'): 18,
  (60, 'q'): 18,
  (60, 'r'): 18,
  (60, 's'): 18,
  (60, 't'): 18,
  (60, 'u'): 18,
  (60, 'v'): 18,
  (60, 'w'): 18,
  (60, 'x'): 18,
  (60, 'y'): 18,
  (60, 'z'): 18,
  (61, '0'): 18,
  (61, '1'): 18,
  (61, '2'): 18,
  (61, '3'): 18,
  (61, '4'): 18,
  (61, '5'): 18,
  (61, '6'): 18,
  (61, '7'): 18,
  (61, '8'): 18,
  (61, '9'): 18,
  (61, '@'): 18,
  (61, 'A'): 18,
  (61, 'B'): 18,
  (61, 'C'): 18,
  (61, 'D'): 18,
  (61, 'E'): 18,
  (61, 'F'): 18,
  (61, 'G'): 18,
  (61, 'H'): 18,
  (61, 'I'): 18,
  (61, 'J'): 18,
  (61, 'K'): 18,
  (61, 'L'): 18,
  (61, 'M'): 18,
  (61, 'N'): 18,
  (61, 'O'): 18,
  (61, 'P'): 18,
  (61, 'Q'): 18,
  (61, 'R'): 18,
  (61, 'S'): 18,
  (61, 'T'): 18,
  (61, 'U'): 18,
  (61, 'V'): 18,
  (61, 'W'): 18,
  (61, 'X'): 18,
  (61, 'Y'): 18,
  (61, 'Z'): 18,
  (61, '_'): 18,
  (61, 'a'): 18,
  (61, 'b'): 18,
  (61, 'c'): 18,
  (61, 'd'): 18,
  (61, 'e'): 18,
  (61, 'f'): 18,
  (61, 'g'): 18,
  (61, 'h'): 18,
  (61, 'i'): 18,
  (61, 'j'): 18,
  (61, 'k'): 18,
  (61, 'l'): 18,
  (61, 'm'): 18,
  (61, 'n'): 18,
  (61, 'o'): 18,
  (61, 'p'): 18,
  (61, 'q'): 18,
  (61, 'r'): 18,
  (61, 's'): 18,
  (61, 't'): 18,
  (61, 'u'): 18,
  (61, 'v'): 18,
  (61, 'w'): 18,
  (61, 'x'): 18,
  (61, 'y'): 18,
  (61, 'z'): 18,
  (63, '+'): 66,
  (63, '-'): 66,
  (63, '0'): 67,
  (63, '1'): 67,
  (63, '2'): 67,
  (63, '3'): 67,
  (63, '4'): 67,
  (63, '5'): 67,
  (63, '6'): 67,
  (63, '7'): 67,
  (63, '8'): 67,
  (63, '9'): 67,
  (64, '0'): 65,
  (64, '1'): 65,
  (64, '2'): 65,
  (64, '3'): 65,
  (64, '4'): 65,
  (64, '5'): 65,
  (64, '6'): 65,
  (64, '7'): 65,
  (64, '8'): 65,
  (64, '9'): 65,
  (65, '0'): 65,
  (65, '1'): 65,
  (65, '2'): 65,
  (65, '3'): 65,
  (65, '4'): 65,
  (65, '5'): 65,
  (65, '6'): 65,
  (65, '7'): 65,
  (65, '8'): 65,
  (65, '9'): 65,
  (65, 'E'): 63,
  (65, 'e'): 63,
  (66, '0'): 67,
  (66, '1'): 67,
  (66, '2'): 67,
  (66, '3'): 67,
  (66, '4'): 67,
  (66, '5'): 67,
  (66, '6'): 67,
  (66, '7'): 67,
  (66, '8'): 67,
  (66, '9'): 67,
  (67, '0'): 67,
  (67, '1'): 67,
  (67, '2'): 67,
  (67, '3'): 67,
  (67, '4'): 67,
  (67, '5'): 67,
  (67, '6'): 67,
  (67, '7'): 67,
  (67, '8'): 67,
  (67, '9'): 67},
 set([0,
      1,
      3,
      5,
      6,
      7,
      8,
      9,
      10,
      11,
      12,
      13,
      14,
      15,
      16,
      17,
      18,
      19,
      20,
      21,
      22,
      23,
      24,
      25,
      26,
      27,
      28,
      29,
      30,
      31,
      32,
      33,
      34,
      35,
      36,
      37,
      38,
      39,
      40,
      41,
      42,
      43,
      44,
      45,
      46,
      47,
      48,
      49,
      50,
      51,
      52,
      53,
      54,
      55,
      56,
      57,
      58,
      59,
      60,
      61,
      62,
      65,
      67,
      68,
      69]),
 set([0,
      1,
      3,
      5,
      6,
      7,
      8,
      9,
      10,
      11,
      12,
      13,
      14,
      15,
      16,
      17,
      18,
      19,
      20,
      21,
      22,
      23,
      24,
      25,
      26,
      27,
      28,
      29,
      30,
      31,
      32,
      33,
      34,
      35,
      36,
      37,
      38,
      39,
      40,
      41,
      42,
      43,
      44,
      45,
      46,
      47,
      48,
      49,
      50,
      51,
      52,
      53,
      54,
      55,
      56,
      57,
      58,
      59,
      60,
      61,
      62,
      65,
      67,
      68,
      69]),
 ['INTEGER',
  'IGNORE',
  '1',
  'IGNORE',
  'start*, 1, final*, 0, start|, 0, start|, 0, final*, start*, final*, 0, 0, final*, start*, final*, 0, start|, 0, final|, start|, 0, 1, final*, start*, final*, 0, 0, final*, start*, final*, 0, 1, final|, start|, 0, final|, start|, 0, final*, start*, final*, 0, 0, final*, start*, final*, 0, final|, start|, 0, 1, final|, start|, 0, final*, start*, final*, 0, 0, final*, final*, 0, final|, start|, 0, 1, final|, start|, 0, final*, start*, final*, 0, 1, final*, 0, start|, 0, start|, 0, final*, start*, final*, start*, 0, final*, 0, start|, 0, final|, start|, 0, 1, final*, start*, final*, 0, final*, 0, start|, 0, final|, start|, 0, 1, final*, start*, final*, start*, 0, final*, 0, 1, final|, start|, 0, final|, start|, 0, final*, start*, final*, 0, final*, 0, 1, final|, start|, 0, final|, start|, 0, final*, start*, final*, start*, 0, final*, 0, final|, start|, 0, 1, final|, start|, 0, final*, start*, final*, 0, final*, 0, final|, start|, 0, 1, final|, start|, 0, final*, start*, final*, start*, 0, final*, 0, final|, start|, 0, 1, final|, start|, 0, final*, start*, final*, 0, 1, final*, 0, final|, start|, 0, 1, final|, start|, 0, final*, start*, final*, start*, 0',
  'MOD',
  'R_PAREN',
  'PLUS',
  'MUL',
  'MINUS',
  'COMMA',
  'DIV',
  'DOT',
  'INTEGER',
  '__2_;',
  'SINGLE_EQ',
  'LT',
  'GT',
  'ATOM',
  'L_PAREN',
  'L_BRACK',
  'R_BRACK',
  'ATOM',
  'ATOM',
  'ATOM',
  'ATOM',
  'ATOM',
  'ATOM',
  'ATOM',
  'ATOM',
  'ATOM',
  'ATOM',
  'ATOM',
  'L_BRACE',
  'R_BRACE',
  'ATOM',
  'ATOM',
  'ATOM',
  'WHILE',
  'ATOM',
  'ATOM',
  'BOOLEAN',
  'ATOM',
  'ATOM',
  'ATOM',
  'ATOM',
  'RETURN',
  'ATOM',
  'NOT',
  'OR',
  'ATOM',
  'LET',
  'IF',
  'ATOM',
  'FN',
  'ATOM',
  'ATOM',
  'ATOM',
  'ATOM',
  'ELSE',
  'ATOM',
  'AND',
  'DOUBLE_EQ',
  'final*, 1, final|, final*, 0, final|, start|, 0, start|, 0, 0, final*, final|, 1, final*, 0, final|, start|, 0, start|, 0, 0',
  '0, final*, 0, final|, 1',
  'FLOAT',
  'final|, 0, 1, final|, final*, final|, 0, final|, final*, 1',
  'FLOAT',
  'STRING',
  'NEQ']), {'IGNORE': None})

# generated code between this line and it's other occurrence

if __name__ == '__main__':
    f = py.path.local(__file__)
    grammar_file = os.path.dirname(os.path.realpath(__file__)) + "/grammar.ebnf"
    ebnff = py.path.local(grammar_file)
    ebnf = ebnff.read()
    oldcontent = f.read()
    s = "# GENERATED CODE BETWEEN THIS LINE AND IT'S OTHER OCCURRENCE\n".lower()
    pre, gen, after = oldcontent.split(s)

    try:
        lexer, parser, transformer = make_all(ebnf)
        transformer = transformer.source
        newcontent = ("%s%s%s\nparser = %r\n\n%s\n\n%s%s" % (pre, s,transformer.replace("ToAST", "WLVLANGToAST"), parser, lexer.get_dummy_repr(), s, after, ))
        f.write(newcontent)
        print "success"
    except ParseError, e:
        print e.nice_error_message(filename="grammar.ebnf", source=ebnf)
