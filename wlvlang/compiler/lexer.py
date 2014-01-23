import string

from rpython.rlib.rstring import StringBuilder
from rpython.rlib.runicode import unicode_encode_utf_8

from rply import Token, LexerGenerator
from rply.token import SourcePosition

class LexerError(Exception):
    def __init__(self, pos, msg=None):
        self.pos = pos
        self.msg = "" if msg is None else msg

class LexerWrapper(object):
    def __init__(self, source, lexer=None):
        if lexer is None:
            l = Lexer(source)
        else:
            l = lexer(source)

        self.lexer = l.build()

    def next(self):
        return self.lexer.next()

class RplyLexer(object):
    ignore = r"([\n\t\r\s])|(#[^\n]*)"
    terminals = [
        ("IDENTIFIER",  r"[a-zA-Z_$][a-zA-Z_0-9]*"),
        ("DECIMALLITERAL", r"(((0|[1-9][0-9]*)(\.[0-9]*)?)|(\.[0-9]+))([eE][\+\-]?[0-9]*)?"),
        ("HEXINTEGERLITERAL", r"0[xX][0-9a-fA-F]+"),
        ("OCTALINTEGERLITERAL", r"0[oO][0-7]+"),
        ("BINARYINTEGERLITERAL", r"0[bB][0-1]+"),
        ("SINGLESTRING", r"'([^'\\]|\\.)*'"),
        ("DOUBLESTRING", r"\"([^\"\\]|\\.)*\""),
        ("SINGLE_EQ", r"="),
        ("LET", r"let"),
        ("CLASS", r"class"),
        ("FN", r"fn"),
        ("DOT", r"\."),
        ("L_PAREN", r"\("),
        ("R_PAREN", r"\)"),
        ("L_BRACE", r"\{"),
        ("R_BRACE", r"\}"),
        ("L_BRACK", r"\["),
        ("R_BRACK", r"\]"),
        ("IF", r"if"),
        ("ELSE", r"else"),
        ("WHILE", r"while"),
        ("FOR", r"for"),
        ("IN", r"in"),
        ("DOUBLE_EQ", r"=="),
        ("NEQ", r"!="),
        ("LT", r"<"),
        ("GT", r">"),
        ("LTEQ", r"<="),
        ("GTEQ", r">="),
        ("PLUS", r"\+"),
        ("MINUS", r"-"),
        ("MUL", r"\*"),
        ("DIV", r"/"),
        ("MOD", r"%"),
        ("AND", r"and"),
        ("OR", r"or"),
        ("NOT", r"not"),
    ]

    def __init__(self, source):
        self.lg = LexerGenerator()
        self.lg.ignore(self.ignore)

        for rules, re in self.terminals:
            self.lg.add(rules, re)

        self.lexer = self.lg.build()
        self.source = source

    def build(self):
        return self.lexer.lex(self.source)

class Lexer(object):

    EOF = chr(0)

    INVALID_FLOAT_MSG = "Invalid floating point"
    INVALID_E_NOTATION = "Invalid standard form number"

    keywords = [ "return", "fn", "for", "while", "do"]

    def __init__(self, source):
            self.current_idx = 0
            self.column_num = 0
            self.source = source
            self.state = 0

    def peek(self):
        """ Read the next character in the source string but does not progress
        the current index (self.current_idx). """
        try:
            char = self.source[self.current_idx]
        except IndexError:
            char = self.EOF

        return char

    def read(self):
        """ Read the next character in the source string and progress the
        current index (self.current_idx) to the next character.
        Returns EOF if the Lexer has reached the end of the
        source string.  """
        char = self.peek()
        self.current_idx += 1
        self.column_num += 1
        return char

    def unread(self):
        self.current_idx -= 1
        assert self.current_idx >= 0
        self.column_num -= 1

    def handle_comment(self):
        while True:
            char = self.read()
            if char == EOF or char in "\r\n":
                self.unread()
                break

    def handle_number(self):
        floating_point_seen = False
        exponent_seen = False
        floating_point_in_exponent_seen = False
        num_start = True
        digits = ""
        while True:
            char = self.read()

            if char.isdigit():
                digits += char
            elif char == ".":

                # Test for the case where a member of a number is being accessed
                # For example the following is ok:
                # `12310.90.toint()`
                # Whereas the following is not syntactically ok:
                # `12310.90.12`

                next_char = self.peek()

                if floating_point_seen and next_char.isdigit():
                    raise LexerError(self.current_position(), self.INVALID_FLOAT_MSG)

                floating_point_seen = True
                digits += char

            elif char in "eE":

                if exponent_seen:
                    raise LexerError(self.current_position(), self.INVALID_E_NOTATION)

                exponent_seen = True
                digits += char

                # Check for a sign after the `e` symbol, for example:
                # `1e+12`
                # Here we also ensure a number follows the `e` symbol regardless
                # of any sign character.

                next_char = self.read()

                if next_char in "+-":
                    digits += next_char

                    # Since we've checked the sign exists move onto the next character
                    # after the + or - in order to check for a number
                    next_char = self.read()


                if next_char == ".":
                    if floating_point_in_exponent_seen or not self.peek().isdigit():
                        raise LexerError(self.current_position(), self.INVALID_FLOAT_MSG)

                    floating_point_in_exponent_seen = True
                    # Prefix with a 0 to avoid any ambiguity in the potential form: 1e.10 instead we
                    # should only get 1e0.10
                    digits += "0"
                    digits += next_char
                elif next_char.isdigit():
                    digits += next_char
            elif num_start and char in "+-":
                digits += char
            else:
                return NumberToken(digits, floating_point_seen or floating_point_in_exponent_seen, exponent_seen)

            # One iteration has occurred at this point, so we are no longer
            # parsing the first character (which means we will no longer allow a + or - symbol
            num_start = False

    def handle_plus_or_minus(self, sign):
        second_level = False
        symbol = sign
        while True:
            char = self.peek()

            if char.isdigit():

                # Unread twice so the next call to 'read' results in the plus symbol
                # that brought us into this method from tokenise.
                # We do this because the handle_number method will include
                # the sign in the resulting token.
                self.unread();
                return self.handle_number()
            elif not second_level and char == sign:
                second_level = True
                symbol += sign
            else:
                return SymbolToken(symbol)

    def handle_less_or_greater_than(self, symbol):
        char = self.read()
        if char == symbol or char == "=" or char == "-":
            return SymbolToken(symbol + char)

        self.unread()
        return SymbolToken(symbol)


    def handle_equals(self):
        char = self.read()

        if char == "=":
            return SymbolToken("==")

        self.unread()
        return SymbolToken("=")

    def handle_exclamation(self):
        char = self.read()

        if char == "=":
            return SymbolToken("!=")

        self.unread()
        return SymbolToken("!")

    def handle_multiply(self):
        char = self.read()

        if char == "*":
            return SymbolToken("**")

        self.unread()
        return SymbolToken("*")

    def handle_divide(self):
        return SymbolToken("/")

    def handle_mod(self):
        return SymbolToken("%")

    def handle_dot(self):
        next_char = self.read()

        if next_char.isdigit():
            self.unread()
            self.unread()
            return self.handle_number()

        self.unread()
        return SymbolToken(".")

    def handle_identifiers(self, start_char):
        current_symbol = start_char
        while True:

            # Run until next opchar or whitespace
            char = self.read()

            if char in "()=<> \t\r\n*+-%/!.":
                self.unread()
                if current_symbol in self.keywords:
                    return KeywordToken(current_symbol)
                else:
                    return SymbolToken(current_symbol)

            current_symbol += char


    def current_position(self):
        return None

    def build(self):
        space_seen = False
        newline_seen = False

        while True:
            char = self.read()

            if char == self.EOF:
                break
            elif char in " \t":
                space_seen = True
                newline_seen = False
                continue
            elif char == "#":
                self.handle_comment()
            elif char in "\r\n":
                space_seen = newline_seen = True
                yield SymbolToken("NEWLINE")
            elif char in "+-":
                yield self.handle_plus_or_minus(char)
            elif char == "*":
                yield self.handle_multiply()
            elif char == "/":
                yield self.handle_divide()
            elif char == "%":
                yield self.handle_mod()
            elif char in "<>":
                yield self.handle_less_or_greater_than(char)
            elif char == "=":
                yield self.handle_equals()
            elif char == "!":
                yield self.handle_exclamation()
            elif char == ".":
                yield self.handle_dot()
            elif char in ";":
                yield SymbolToken(char)
            elif char in "()":
                yield SymbolToken(char)
            elif char in "{}":
                yield SymbolToken(char)
            else:
                yield self.handle_identifiers(start_char=char)


class Token(object):
    pass

class KeywordToken(Token):
    def __init__(self, value):
        self.value = value

class SymbolToken(Token):
    def __init__(self, value):
        self.value = value

class NumberToken(Token):

    def __init__(self, value, floating_point=False, exponent=False):
        self.value = value
        self.floating_point = floating_point
        self.standard_form = exponent
