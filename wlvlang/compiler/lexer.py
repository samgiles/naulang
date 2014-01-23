import string

from rpython.rlib.rstring import StringBuilder
from rpython.rlib.runicode import unicode_encode_utf_8

from rply import Token
from rply.token import SourcePosition

class LexerError(Exception):
    def __init__(self, pos, msg=None):
        self.pos = pos
        self.msg = "" if msg is None else msg


class Lexer(object):

    EOF = chr(0)

    INVALID_FLOAT_MSG = "Invalid floating point"
    INVALID_E_NOTATION = "Invalid standard form number"

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
                    raise LexerError(self.current_position(), self.INVALID_FLOAT_MSG)

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
                        raise LexerError(self.current_position(), self.INVALID_E_NOTATION)

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




    def current_position(self):
        return None

    def handle_plus(self):
        while True:
            char = self.read()

            if char.isdigit():
                self.unread();
                self.handle_number()


    def tokenise(self):
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
                #TODO
            elif char == "+":
                self.handle_plus()
            elif char == "-":
                pass

    def next(self):
        pass

class Token(object):
    pass

class NumberToken(Token):

    def __init__(self, value, floating_point=False, exponent=False):
        self.value = value
        self.floating_point = floating_point
        self.standard_form = exponent
