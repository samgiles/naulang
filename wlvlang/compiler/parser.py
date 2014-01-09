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

    # Create abstract syntax tree
    s.visit(WLVLANGToAST())
    assert len(s) == 1
    s = s[0]
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
            children.extend(self.visit_statementexpr(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_statementexpr(node.children[0]))
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
    def visit_identifier(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if node.children[0].symbol == 'atomic':
            children = []
            expr = self.visit_atomic(node.children[0])
            assert len(expr) == 1
            children.extend(expr[0].children)
            return [Nonterminal(node.symbol, children)]
        if node.children[0].symbol == 'bool':
            children = []
            expr = self.visit_bool(node.children[0])
            assert len(expr) == 1
            children.extend(expr[0].children)
            return [Nonterminal(node.symbol, children)]
        if node.children[0].symbol == 'number':
            children = []
            expr = self.visit_number(node.children[0])
            assert len(expr) == 1
            children.extend(expr[0].children)
            return [Nonterminal(node.symbol, children)]
        children = []
        expr = self.visit_string(node.children[0])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_statementexpr(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            if node.children[0].symbol == 'ifstatement':
                children = []
                children.extend(self.visit_ifstatement(node.children[0]))
                return [Nonterminal(node.symbol, children)]
            children = []
            children.extend(self.visit_whilestatement(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        if node.children[0].symbol == 'assignmentstatement':
            children = []
            children.extend(self.visit_assignmentstatement(node.children[0]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_unaryexpr(node.children[0]))
        return [Nonterminal(node.symbol, children)]
    def visit__maybe_symbol0(self, node):
        #auto-generated code, don't edit
        children = []
        children.extend(self.visit_statementexpr(node.children[0]))
        return [Nonterminal(node.symbol, children)]
    def visit__maybe_symbol1(self, node):
        #auto-generated code, don't edit
        children = []
        children.extend(self.visit_statementexpr(node.children[0]))
        return [Nonterminal(node.symbol, children)]
    def visit_ifstatement(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 6:
            children = []
            children.extend(self.visit_unaryexpr(node.children[2]))
            expr = self.visit___ifstatement_rest_0_0(node.children[5])
            assert len(expr) == 1
            children.extend(expr[0].children)
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_unaryexpr(node.children[2]))
        expr = self.visit__maybe_symbol0(node.children[5])
        assert len(expr) == 1
        children.extend(expr[0].children)
        expr = self.visit___ifstatement_rest_0_0(node.children[6])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit__maybe_symbol2(self, node):
        #auto-generated code, don't edit
        children = []
        children.extend(self.visit_statementexpr(node.children[0]))
        return [Nonterminal(node.symbol, children)]
    def visit_whilestatement(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 6:
            children = []
            children.extend(self.visit_unaryexpr(node.children[2]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_unaryexpr(node.children[2]))
        expr = self.visit__maybe_symbol2(node.children[5])
        assert len(expr) == 1
        children.extend(expr[0].children)
        return [Nonterminal(node.symbol, children)]
    def visit_assignmentstatement(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 3:
            children = []
            children.extend(self.visit_atomic(node.children[0]))
            children.extend([node.children[1]])
            children.extend(self.visit_unaryexpr(node.children[2]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend([node.children[0]])
        children.extend(self.visit_atomic(node.children[1]))
        children.extend([node.children[2]])
        children.extend(self.visit_unaryexpr(node.children[3]))
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
            return self.visit_multitiveexpr(node.children[0])
        if node.children[1].symbol == 'MINUS':
            children = []
            children.extend([node.children[0]])
            children.extend([node.children[1]])
            children.extend(self.visit_additiveexpr(node.children[2]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend([node.children[0]])
        children.extend([node.children[1]])
        children.extend(self.visit_additiveexpr(node.children[2]))
        return [Nonterminal(node.symbol, children)]
    def visit_multitiveexpr(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 1:
            return self.visit_comparisonexpr(node.children[0])
        if node.children[1].symbol == 'DIV':
            children = []
            children.extend(self.visit_comparisonexpr(node.children[0]))
            children.extend([node.children[1]])
            children.extend(self.visit_multitiveexpr(node.children[2]))
            return [Nonterminal(node.symbol, children)]
        if node.children[1].symbol == 'MOD':
            children = []
            children.extend(self.visit_comparisonexpr(node.children[0]))
            children.extend([node.children[1]])
            children.extend(self.visit_multitiveexpr(node.children[2]))
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend(self.visit_comparisonexpr(node.children[0]))
        children.extend([node.children[1]])
        children.extend(self.visit_multitiveexpr(node.children[2]))
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
        return self.visit_unaryexpr(node.children[1])
    def visit___ifstatement_rest_0_0(self, node):
        #auto-generated code, don't edit
        length = len(node.children)
        if length == 4:
            children = []
            children.extend([node.children[1]])
            return [Nonterminal(node.symbol, children)]
        children = []
        children.extend([node.children[1]])
        expr = self.visit__maybe_symbol1(node.children[3])
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
  Rule('_plus_symbol0', [['statementexpr', '_plus_symbol0'], ['statementexpr']]),
  Rule('atomic', [['ATOM']]),
  Rule('number', [['FLOAT'], ['INTEGER']]),
  Rule('string', [['STRING']]),
  Rule('bool', [['BOOLEAN']]),
  Rule('identifier', [['atomic'], ['string'], ['number'], ['bool']]),
  Rule('statementexpr', [['whilestatement'], ['ifstatement'], ['assignmentstatement', '__0_;'], ['unaryexpr', '__0_;']]),
  Rule('_maybe_symbol0', [['statementexpr']]),
  Rule('_maybe_symbol1', [['statementexpr']]),
  Rule('ifstatement', [['IF', 'L_PAREN', 'unaryexpr', 'RPAREN', 'L_BRACE', '_maybe_symbol0', '__ifstatement_rest_0_0'], ['IF', 'L_PAREN', 'unaryexpr', 'RPAREN', 'L_BRACE', '__ifstatement_rest_0_0']]),
  Rule('_maybe_symbol2', [['statementexpr']]),
  Rule('whilestatement', [['WHILE', 'L_PAREN', 'unaryexpr', 'R_PAREN', 'L_BRACE', '_maybe_symbol2', 'R_BRACE'], ['WHILE', 'L_PAREN', 'unaryexpr', 'R_PAREN', 'L_BRACE', 'R_BRACE']]),
  Rule('assignmentstatement', [['LET', 'atomic', 'SINGLE_EQ', 'unaryexpr'], ['atomic', 'SINGLE_EQ', 'unaryexpr']]),
  Rule('unaryexpr', [['unaryoperator', 'additiveexpr'], ['additiveexpr']]),
  Rule('unaryoperator', [['ADD'], ['MINUS'], ['NOT']]),
  Rule('additiveexpr', [['multitive', 'PLUS', 'additiveexpr'], ['multitive', 'MINUS', 'additiveexpr'], ['multitiveexpr']]),
  Rule('multitiveexpr', [['comparisonexpr', 'MUL', 'multitiveexpr'], ['comparisonexpr', 'DIV', 'multitiveexpr'], ['comparisonexpr', 'MOD', 'multitiveexpr'], ['comparisonexpr']]),
  Rule('comparisonexpr', [['equalityexpr', 'LT', 'comparisonexpr'], ['equalityexpr', 'GT', 'comparisonexpr'], ['equalityexpr']]),
  Rule('equalityexpr', [['logicalandexpr', 'DOUBLE_EQ', 'equalityexpr'], ['logicalandexpr', 'NEQ', 'equalityexpr'], ['logicalandexpr']]),
  Rule('logicalandexpr', [['logicalorexpr', 'AND', 'logicalandexpr'], ['logicalorexpr']]),
  Rule('logicalorexpr', [['primaryexpr', 'OR', 'logicalorexpr'], ['primaryexpr']]),
  Rule('primaryexpr', [['L_PAREN', 'unaryexpr', 'R_PAREN'], ['identifier']]),
  Rule('__ifstatement_rest_0_0', [['R_BRACE', 'ELSE', 'L_BRACE', '_maybe_symbol1', 'R_BRACE'], ['R_BRACE', 'ELSE', 'L_BRACE', 'R_BRACE']])],
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
            elif 'b' <= char <= 'd':
                state = 18
            elif 'x' <= char <= 'z':
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
            elif char == 'a':
                state = 19
            elif char == 'e':
                state = 20
            elif char == 'f':
                state = 21
            elif char == 'i':
                state = 22
            elif char == 'l':
                state = 23
            elif char == 'o':
                state = 24
            elif char == 'n':
                state = 25
            elif char == 'r':
                state = 26
            elif char == 't':
                state = 27
            elif char == 'w':
                state = 28
            elif char == '(':
                state = 29
            elif char == '{':
                state = 30
            elif char == '}':
                state = 31
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
                state = 64
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
            if ']' <= char <= '\xff':
                state = 4
                continue
            elif '#' <= char <= '[':
                state = 4
                continue
            elif '\x00' <= char <= '!':
                state = 4
                continue
            elif char == '"':
                state = 63
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
                state = 60
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
            if char == 'E':
                state = 58
            elif char == 'e':
                state = 58
            elif char == '.':
                state = 59
            elif '0' <= char <= '9':
                state = 13
                continue
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
                state = 57
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
        if state == 19:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 19
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
                state = 55
            else:
                break
        if state == 20:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 20
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
                state = 52
            else:
                break
        if state == 21:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 21
                return i
            if '@' <= char <= 'Z':
                state = 18
                continue
            elif 'b' <= char <= 'z':
                state = 18
                continue
            elif '0' <= char <= '9':
                state = 18
                continue
            elif char == '_':
                state = 18
                continue
            elif char == 'a':
                state = 50
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
            if char == 'f':
                state = 49
            elif '@' <= char <= 'Z':
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
                state = 47
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
                state = 46
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
                state = 44
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
                state = 39
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
                state = 36
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
            if char == 'h':
                state = 32
            elif '@' <= char <= 'Z':
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
            if char == 'i':
                state = 33
            elif '@' <= char <= 'Z':
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
            else:
                break
        if state == 33:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 33
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
                state = 34
            else:
                break
        if state == 34:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 34
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
            if char == 't':
                state = 40
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
        if state == 40:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 40
                return i
            if char == 'u':
                state = 41
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
                state = 42
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
                state = 37
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
                state = 53
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
                state = 54
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
            if char == 'd':
                state = 56
            elif '@' <= char <= 'Z':
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
        if state == 58:
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 58
                return ~i
            if char == '+':
                state = 61
            elif char == '-':
                state = 61
            elif '0' <= char <= '9':
                state = 62
            else:
                break
        if state == 59:
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 59
                return ~i
            if '0' <= char <= '9':
                state = 60
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
            if char == 'E':
                state = 58
                continue
            elif char == 'e':
                state = 58
                continue
            elif '0' <= char <= '9':
                state = 60
                continue
            else:
                break
        if state == 61:
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 61
                return ~i
            if '0' <= char <= '9':
                state = 62
            else:
                break
        if state == 62:
            runner.last_matched_index = i - 1
            runner.last_matched_state = state
            try:
                char = input[i]
                i += 1
            except IndexError:
                runner.state = 62
                return i
            if '0' <= char <= '9':
                state = 62
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
lexer = DummyLexer(recognize, DFA(65,
 {(0, '\t'): 1,
  (0, '\n'): 1,
  (0, '\x0c'): 1,
  (0, '\r'): 1,
  (0, ' '): 1,
  (0, '!'): 2,
  (0, '"'): 4,
  (0, '#'): 3,
  (0, '%'): 5,
  (0, '('): 29,
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
  (0, 'a'): 19,
  (0, 'b'): 18,
  (0, 'c'): 18,
  (0, 'd'): 18,
  (0, 'e'): 20,
  (0, 'f'): 21,
  (0, 'g'): 18,
  (0, 'h'): 18,
  (0, 'i'): 22,
  (0, 'j'): 18,
  (0, 'k'): 18,
  (0, 'l'): 23,
  (0, 'm'): 18,
  (0, 'n'): 25,
  (0, 'o'): 24,
  (0, 'p'): 18,
  (0, 'q'): 18,
  (0, 'r'): 26,
  (0, 's'): 18,
  (0, 't'): 27,
  (0, 'u'): 18,
  (0, 'v'): 18,
  (0, 'w'): 28,
  (0, 'x'): 18,
  (0, 'y'): 18,
  (0, 'z'): 18,
  (0, '{'): 30,
  (0, '}'): 31,
  (2, '='): 64,
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
  (4, '"'): 63,
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
  (12, '0'): 60,
  (12, '1'): 60,
  (12, '2'): 60,
  (12, '3'): 60,
  (12, '4'): 60,
  (12, '5'): 60,
  (12, '6'): 60,
  (12, '7'): 60,
  (12, '8'): 60,
  (12, '9'): 60,
  (13, '.'): 59,
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
  (13, 'E'): 58,
  (13, 'e'): 58,
  (15, '='): 57,
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
  (19, '0'): 18,
  (19, '1'): 18,
  (19, '2'): 18,
  (19, '3'): 18,
  (19, '4'): 18,
  (19, '5'): 18,
  (19, '6'): 18,
  (19, '7'): 18,
  (19, '8'): 18,
  (19, '9'): 18,
  (19, '@'): 18,
  (19, 'A'): 18,
  (19, 'B'): 18,
  (19, 'C'): 18,
  (19, 'D'): 18,
  (19, 'E'): 18,
  (19, 'F'): 18,
  (19, 'G'): 18,
  (19, 'H'): 18,
  (19, 'I'): 18,
  (19, 'J'): 18,
  (19, 'K'): 18,
  (19, 'L'): 18,
  (19, 'M'): 18,
  (19, 'N'): 18,
  (19, 'O'): 18,
  (19, 'P'): 18,
  (19, 'Q'): 18,
  (19, 'R'): 18,
  (19, 'S'): 18,
  (19, 'T'): 18,
  (19, 'U'): 18,
  (19, 'V'): 18,
  (19, 'W'): 18,
  (19, 'X'): 18,
  (19, 'Y'): 18,
  (19, 'Z'): 18,
  (19, '_'): 18,
  (19, 'a'): 18,
  (19, 'b'): 18,
  (19, 'c'): 18,
  (19, 'd'): 18,
  (19, 'e'): 18,
  (19, 'f'): 18,
  (19, 'g'): 18,
  (19, 'h'): 18,
  (19, 'i'): 18,
  (19, 'j'): 18,
  (19, 'k'): 18,
  (19, 'l'): 18,
  (19, 'm'): 18,
  (19, 'n'): 55,
  (19, 'o'): 18,
  (19, 'p'): 18,
  (19, 'q'): 18,
  (19, 'r'): 18,
  (19, 's'): 18,
  (19, 't'): 18,
  (19, 'u'): 18,
  (19, 'v'): 18,
  (19, 'w'): 18,
  (19, 'x'): 18,
  (19, 'y'): 18,
  (19, 'z'): 18,
  (20, '0'): 18,
  (20, '1'): 18,
  (20, '2'): 18,
  (20, '3'): 18,
  (20, '4'): 18,
  (20, '5'): 18,
  (20, '6'): 18,
  (20, '7'): 18,
  (20, '8'): 18,
  (20, '9'): 18,
  (20, '@'): 18,
  (20, 'A'): 18,
  (20, 'B'): 18,
  (20, 'C'): 18,
  (20, 'D'): 18,
  (20, 'E'): 18,
  (20, 'F'): 18,
  (20, 'G'): 18,
  (20, 'H'): 18,
  (20, 'I'): 18,
  (20, 'J'): 18,
  (20, 'K'): 18,
  (20, 'L'): 18,
  (20, 'M'): 18,
  (20, 'N'): 18,
  (20, 'O'): 18,
  (20, 'P'): 18,
  (20, 'Q'): 18,
  (20, 'R'): 18,
  (20, 'S'): 18,
  (20, 'T'): 18,
  (20, 'U'): 18,
  (20, 'V'): 18,
  (20, 'W'): 18,
  (20, 'X'): 18,
  (20, 'Y'): 18,
  (20, 'Z'): 18,
  (20, '_'): 18,
  (20, 'a'): 18,
  (20, 'b'): 18,
  (20, 'c'): 18,
  (20, 'd'): 18,
  (20, 'e'): 18,
  (20, 'f'): 18,
  (20, 'g'): 18,
  (20, 'h'): 18,
  (20, 'i'): 18,
  (20, 'j'): 18,
  (20, 'k'): 18,
  (20, 'l'): 52,
  (20, 'm'): 18,
  (20, 'n'): 18,
  (20, 'o'): 18,
  (20, 'p'): 18,
  (20, 'q'): 18,
  (20, 'r'): 18,
  (20, 's'): 18,
  (20, 't'): 18,
  (20, 'u'): 18,
  (20, 'v'): 18,
  (20, 'w'): 18,
  (20, 'x'): 18,
  (20, 'y'): 18,
  (20, 'z'): 18,
  (21, '0'): 18,
  (21, '1'): 18,
  (21, '2'): 18,
  (21, '3'): 18,
  (21, '4'): 18,
  (21, '5'): 18,
  (21, '6'): 18,
  (21, '7'): 18,
  (21, '8'): 18,
  (21, '9'): 18,
  (21, '@'): 18,
  (21, 'A'): 18,
  (21, 'B'): 18,
  (21, 'C'): 18,
  (21, 'D'): 18,
  (21, 'E'): 18,
  (21, 'F'): 18,
  (21, 'G'): 18,
  (21, 'H'): 18,
  (21, 'I'): 18,
  (21, 'J'): 18,
  (21, 'K'): 18,
  (21, 'L'): 18,
  (21, 'M'): 18,
  (21, 'N'): 18,
  (21, 'O'): 18,
  (21, 'P'): 18,
  (21, 'Q'): 18,
  (21, 'R'): 18,
  (21, 'S'): 18,
  (21, 'T'): 18,
  (21, 'U'): 18,
  (21, 'V'): 18,
  (21, 'W'): 18,
  (21, 'X'): 18,
  (21, 'Y'): 18,
  (21, 'Z'): 18,
  (21, '_'): 18,
  (21, 'a'): 50,
  (21, 'b'): 18,
  (21, 'c'): 18,
  (21, 'd'): 18,
  (21, 'e'): 18,
  (21, 'f'): 18,
  (21, 'g'): 18,
  (21, 'h'): 18,
  (21, 'i'): 18,
  (21, 'j'): 18,
  (21, 'k'): 18,
  (21, 'l'): 18,
  (21, 'm'): 18,
  (21, 'n'): 18,
  (21, 'o'): 18,
  (21, 'p'): 18,
  (21, 'q'): 18,
  (21, 'r'): 18,
  (21, 's'): 18,
  (21, 't'): 18,
  (21, 'u'): 18,
  (21, 'v'): 18,
  (21, 'w'): 18,
  (21, 'x'): 18,
  (21, 'y'): 18,
  (21, 'z'): 18,
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
  (22, 'f'): 49,
  (22, 'g'): 18,
  (22, 'h'): 18,
  (22, 'i'): 18,
  (22, 'j'): 18,
  (22, 'k'): 18,
  (22, 'l'): 18,
  (22, 'm'): 18,
  (22, 'n'): 18,
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
  (23, 'e'): 47,
  (23, 'f'): 18,
  (23, 'g'): 18,
  (23, 'h'): 18,
  (23, 'i'): 18,
  (23, 'j'): 18,
  (23, 'k'): 18,
  (23, 'l'): 18,
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
  (24, 'o'): 18,
  (24, 'p'): 18,
  (24, 'q'): 18,
  (24, 'r'): 46,
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
  (25, 'a'): 18,
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
  (25, 'n'): 18,
  (25, 'o'): 44,
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
  (26, 'e'): 39,
  (26, 'f'): 18,
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
  (27, 'e'): 18,
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
  (27, 'r'): 36,
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
  (28, 'h'): 32,
  (28, 'i'): 18,
  (28, 'j'): 18,
  (28, 'k'): 18,
  (28, 'l'): 18,
  (28, 'm'): 18,
  (28, 'n'): 18,
  (28, 'o'): 18,
  (28, 'p'): 18,
  (28, 'q'): 18,
  (28, 'r'): 18,
  (28, 's'): 18,
  (28, 't'): 18,
  (28, 'u'): 18,
  (28, 'v'): 18,
  (28, 'w'): 18,
  (28, 'x'): 18,
  (28, 'y'): 18,
  (28, 'z'): 18,
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
  (32, 'h'): 18,
  (32, 'i'): 33,
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
  (33, '0'): 18,
  (33, '1'): 18,
  (33, '2'): 18,
  (33, '3'): 18,
  (33, '4'): 18,
  (33, '5'): 18,
  (33, '6'): 18,
  (33, '7'): 18,
  (33, '8'): 18,
  (33, '9'): 18,
  (33, '@'): 18,
  (33, 'A'): 18,
  (33, 'B'): 18,
  (33, 'C'): 18,
  (33, 'D'): 18,
  (33, 'E'): 18,
  (33, 'F'): 18,
  (33, 'G'): 18,
  (33, 'H'): 18,
  (33, 'I'): 18,
  (33, 'J'): 18,
  (33, 'K'): 18,
  (33, 'L'): 18,
  (33, 'M'): 18,
  (33, 'N'): 18,
  (33, 'O'): 18,
  (33, 'P'): 18,
  (33, 'Q'): 18,
  (33, 'R'): 18,
  (33, 'S'): 18,
  (33, 'T'): 18,
  (33, 'U'): 18,
  (33, 'V'): 18,
  (33, 'W'): 18,
  (33, 'X'): 18,
  (33, 'Y'): 18,
  (33, 'Z'): 18,
  (33, '_'): 18,
  (33, 'a'): 18,
  (33, 'b'): 18,
  (33, 'c'): 18,
  (33, 'd'): 18,
  (33, 'e'): 18,
  (33, 'f'): 18,
  (33, 'g'): 18,
  (33, 'h'): 18,
  (33, 'i'): 18,
  (33, 'j'): 18,
  (33, 'k'): 18,
  (33, 'l'): 34,
  (33, 'm'): 18,
  (33, 'n'): 18,
  (33, 'o'): 18,
  (33, 'p'): 18,
  (33, 'q'): 18,
  (33, 'r'): 18,
  (33, 's'): 18,
  (33, 't'): 18,
  (33, 'u'): 18,
  (33, 'v'): 18,
  (33, 'w'): 18,
  (33, 'x'): 18,
  (33, 'y'): 18,
  (33, 'z'): 18,
  (34, '0'): 18,
  (34, '1'): 18,
  (34, '2'): 18,
  (34, '3'): 18,
  (34, '4'): 18,
  (34, '5'): 18,
  (34, '6'): 18,
  (34, '7'): 18,
  (34, '8'): 18,
  (34, '9'): 18,
  (34, '@'): 18,
  (34, 'A'): 18,
  (34, 'B'): 18,
  (34, 'C'): 18,
  (34, 'D'): 18,
  (34, 'E'): 18,
  (34, 'F'): 18,
  (34, 'G'): 18,
  (34, 'H'): 18,
  (34, 'I'): 18,
  (34, 'J'): 18,
  (34, 'K'): 18,
  (34, 'L'): 18,
  (34, 'M'): 18,
  (34, 'N'): 18,
  (34, 'O'): 18,
  (34, 'P'): 18,
  (34, 'Q'): 18,
  (34, 'R'): 18,
  (34, 'S'): 18,
  (34, 'T'): 18,
  (34, 'U'): 18,
  (34, 'V'): 18,
  (34, 'W'): 18,
  (34, 'X'): 18,
  (34, 'Y'): 18,
  (34, 'Z'): 18,
  (34, '_'): 18,
  (34, 'a'): 18,
  (34, 'b'): 18,
  (34, 'c'): 18,
  (34, 'd'): 18,
  (34, 'e'): 35,
  (34, 'f'): 18,
  (34, 'g'): 18,
  (34, 'h'): 18,
  (34, 'i'): 18,
  (34, 'j'): 18,
  (34, 'k'): 18,
  (34, 'l'): 18,
  (34, 'm'): 18,
  (34, 'n'): 18,
  (34, 'o'): 18,
  (34, 'p'): 18,
  (34, 'q'): 18,
  (34, 'r'): 18,
  (34, 's'): 18,
  (34, 't'): 18,
  (34, 'u'): 18,
  (34, 'v'): 18,
  (34, 'w'): 18,
  (34, 'x'): 18,
  (34, 'y'): 18,
  (34, 'z'): 18,
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
  (35, 'i'): 18,
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
  (36, 'l'): 18,
  (36, 'm'): 18,
  (36, 'n'): 18,
  (36, 'o'): 18,
  (36, 'p'): 18,
  (36, 'q'): 18,
  (36, 'r'): 18,
  (36, 's'): 18,
  (36, 't'): 18,
  (36, 'u'): 37,
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
  (39, 't'): 40,
  (39, 'u'): 18,
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
  (40, 'e'): 18,
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
  (40, 'u'): 41,
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
  (41, 'r'): 42,
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
  (42, 'n'): 43,
  (42, 'o'): 18,
  (42, 'p'): 18,
  (42, 'q'): 18,
  (42, 'r'): 18,
  (42, 's'): 18,
  (42, 't'): 18,
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
  (43, 'u'): 18,
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
  (44, 'r'): 18,
  (44, 's'): 18,
  (44, 't'): 45,
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
  (45, 'n'): 18,
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
  (50, 'l'): 51,
  (50, 'm'): 18,
  (50, 'n'): 18,
  (50, 'o'): 18,
  (50, 'p'): 18,
  (50, 'q'): 18,
  (50, 'r'): 18,
  (50, 's'): 18,
  (50, 't'): 18,
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
  (51, 's'): 37,
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
  (52, 's'): 53,
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
  (53, 'e'): 54,
  (53, 'f'): 18,
  (53, 'g'): 18,
  (53, 'h'): 18,
  (53, 'i'): 18,
  (53, 'j'): 18,
  (53, 'k'): 18,
  (53, 'l'): 18,
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
  (55, 'd'): 56,
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
  (55, 's'): 18,
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
  (58, '+'): 61,
  (58, '-'): 61,
  (58, '0'): 62,
  (58, '1'): 62,
  (58, '2'): 62,
  (58, '3'): 62,
  (58, '4'): 62,
  (58, '5'): 62,
  (58, '6'): 62,
  (58, '7'): 62,
  (58, '8'): 62,
  (58, '9'): 62,
  (59, '0'): 60,
  (59, '1'): 60,
  (59, '2'): 60,
  (59, '3'): 60,
  (59, '4'): 60,
  (59, '5'): 60,
  (59, '6'): 60,
  (59, '7'): 60,
  (59, '8'): 60,
  (59, '9'): 60,
  (60, '0'): 60,
  (60, '1'): 60,
  (60, '2'): 60,
  (60, '3'): 60,
  (60, '4'): 60,
  (60, '5'): 60,
  (60, '6'): 60,
  (60, '7'): 60,
  (60, '8'): 60,
  (60, '9'): 60,
  (60, 'E'): 58,
  (60, 'e'): 58,
  (61, '0'): 62,
  (61, '1'): 62,
  (61, '2'): 62,
  (61, '3'): 62,
  (61, '4'): 62,
  (61, '5'): 62,
  (61, '6'): 62,
  (61, '7'): 62,
  (61, '8'): 62,
  (61, '9'): 62,
  (62, '0'): 62,
  (62, '1'): 62,
  (62, '2'): 62,
  (62, '3'): 62,
  (62, '4'): 62,
  (62, '5'): 62,
  (62, '6'): 62,
  (62, '7'): 62,
  (62, '8'): 62,
  (62, '9'): 62},
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
      60,
      62,
      63,
      64]),
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
      60,
      62,
      63,
      64]),
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
  '__0_;',
  'SINGLE_EQ',
  'LT',
  'GT',
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
  'L_PAREN',
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
    ebnff = py.path.local("grammar.ebnf")
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
