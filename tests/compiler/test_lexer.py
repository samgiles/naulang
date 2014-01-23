import pytest

from rply.errors import LexingError

from wlvlang.compiler import lexer

def test_handle_number_integer():
    l = lexer.Lexer("100")

    number_token = l.handle_number()

    assert isinstance(number_token, lexer.NumberToken)
    assert number_token.value == "100"
    assert number_token.floating_point == False
    assert number_token.standard_form == False

def test_handle_number_float():
    l = lexer.Lexer("100.2")
    number_token = l.handle_number()

    assert isinstance(number_token, lexer.NumberToken)
    assert number_token.value == "100.2"
    assert number_token.floating_point == True
    assert number_token.standard_form == False

def test_handle_number_standard_form():
    l = lexer.Lexer("100e+10")
    number_token = l.handle_number()

    assert isinstance(number_token, lexer.NumberToken)
    assert number_token.value == "100e+10"
    assert number_token.floating_point == False
    assert number_token.standard_form == True

    l = lexer.Lexer("100e-10")
    number_token = l.handle_number()

    assert isinstance(number_token, lexer.NumberToken)
    assert number_token.value == "100e-10"
    assert number_token.floating_point == False
    assert number_token.standard_form == True

    l = lexer.Lexer("100e10")
    number_token = l.handle_number()

    assert isinstance(number_token, lexer.NumberToken)
    assert number_token.value == "100e10"
    assert number_token.floating_point == False
    assert number_token.standard_form == True

    l = lexer.Lexer("100e.10")
    number_token = l.handle_number()

    assert isinstance(number_token, lexer.NumberToken)
    assert number_token.value == "100e0.10"
    assert number_token.floating_point == True
    assert number_token.standard_form == True

def test_handle_number_signed():
    l = lexer.Lexer("+1000")
    number_token = l.handle_number()

    assert isinstance(number_token, lexer.NumberToken)
    assert number_token.value == "+1000"
    assert number_token.floating_point == False
    assert number_token.standard_form == False

    l = lexer.Lexer("-1000")
    number_token = l.handle_number()

    assert isinstance(number_token, lexer.NumberToken)
    assert number_token.value == "-1000"
    assert number_token.floating_point == False
    assert number_token.standard_form == False

def test_handle_invalid_float():
    l = lexer.Lexer("10.00.12")

    with pytest.raises(lexer.LexerError) as exceptinfo:
        number_token = l.handle_number()

    assert exceptinfo.value.msg == lexer.Lexer.INVALID_FLOAT_MSG

def test_handle_invalid_standard_form():
    l = lexer.Lexer("10e00e12")

    with pytest.raises(lexer.LexerError) as exceptinfo:
        number_token = l.handle_number()

    assert exceptinfo.value.msg == lexer.Lexer.INVALID_E_NOTATION

def test_handle_plus_or_minus_plus_integer():
    l = lexer.Lexer("+100")

    # Advance past the + (in normal operation we would have found the plus,
    # then called into handle_plus_or_minus).
    l.read()

    number_token = l.handle_plus_or_minus("+")

    assert isinstance(number_token, lexer.NumberToken)
    assert number_token.value == "+100"
    assert number_token.floating_point == False
    assert number_token.standard_form == False

def test_handle_plus_or_minus_minus_integer():
    l = lexer.Lexer("-100")

    # Advance past the + (in normal operation we would have found the minus,
    # then called into handle_plus_or_minus).
    l.read()

    number_token = l.handle_plus_or_minus("-")

    assert isinstance(number_token, lexer.NumberToken)
    assert number_token.value == "-100"
    assert number_token.floating_point == False
    assert number_token.standard_form == False

def test_handle_plus_or_minus_symbol():
    l = lexer.Lexer("+a")

    # Advance past the + (in normal operation we would have found the minus,
    # then called into handle_plus_or_minus).
    l.read()

    number_token = l.handle_plus_or_minus("+")

    assert isinstance(number_token, lexer.SymbolToken)
    assert number_token.value == "+"

def test_handle_plus_or_minus_preincrement():
    l = lexer.Lexer("++100")

    # Advance past the + (in normal operation we would have found the minus,
    # then called into handle_plus_or_minus).
    l.read()

    number_token = l.handle_plus_or_minus("+")
    assert isinstance(number_token, lexer.SymbolToken)
    assert number_token.value == "++"

def test_handle_plus_or_minus_predecrement():
    l = lexer.Lexer("--100")

    # Advance past the + (in normal operation we would have found the minus,
    # then called into handle_plus_or_minus).
    l.read()

    number_token = l.handle_plus_or_minus("-")
    assert isinstance(number_token, lexer.SymbolToken)
    assert number_token.value == "--"

def test_simple_tokenise():
    tokens = lexer.LexerWrapper("let a = 100\nlet b = 200\n let c = fn(a) { return a * b }", lexer=lexer.RplyLexer)

    assert "let" == tokens.next().getstr()
    assert "a" == tokens.next().getstr()
    assert "=" == tokens.next().getstr()
    assert "100" == tokens.next().getstr()
    assert "NEWLINE" == tokens.next().getstr()
    assert "let" == tokens.next().getstr()
    assert "b" == tokens.next().getstr()
    assert "=" == tokens.next().getstr()
    assert "200" == tokens.next().getstr()
    assert "NEWLINE" == tokens.next().getstr()
    assert "let" == tokens.next().getstr()
    assert "c" == tokens.next().getstr()
    assert "=" == tokens.next().getstr()
    assert "fn" == tokens.next().getstr()
    assert "("  == tokens.next().getstr()
    assert "a" == tokens.next().getstr()
    assert ")" == tokens.next().getstr()
    assert "{" == tokens.next().getstr()
    assert "return" == tokens.next().getstr()
    assert "a" == tokens.next().getstr()
    assert "*" == tokens.next().getstr()
    assert "b" == tokens.next().getstr()
    assert "}" == tokens.next().getstr()

def test_nested_tokenise():
    tokens = lexer.LexerWrapper("""let main = fn(args) {
    class Test(value) {
        let compare = fn(other) {
            return other.value - value
        }
    }

    let test1 = new Test(12)
    let test2 = new Test(13)
    let result = test1.compare(test2)
    print(result)
}
""", lexer=lexer.RplyLexer)


    try:
        assert "let" == tokens.next().getstr()
        assert "main" == tokens.next().getstr()
        assert "=" == tokens.next().getstr()
        assert "fn" == tokens.next().getstr()
        assert "(" == tokens.next().getstr()
        assert "args" == tokens.next().getstr()
        assert ")" == tokens.next().getstr()
        assert "{" == tokens.next().getstr()
        assert "NEWLINE" == tokens.next().getstr()
        assert "class" == tokens.next().getstr()
        assert "Test" == tokens.next().getstr()
        assert "(" == tokens.next().getstr()
        assert "value" == tokens.next().getstr()
        assert ")" == tokens.next().getstr()
        assert "{" == tokens.next().getstr()
        assert "NEWLINE" == tokens.next().getstr()
        assert "let" == tokens.next().getstr()
        assert "compare" == tokens.next().getstr()
        assert "=" == tokens.next().getstr()
        assert "fn" == tokens.next().getstr()
        assert "(" == tokens.next().getstr()
        assert "other" == tokens.next().getstr()
        assert ")" == tokens.next().getstr()
        assert "{" == tokens.next().getstr()
        assert "NEWLINE" == tokens.next().getstr()
        assert "return" == tokens.next().getstr()
        assert "other" == tokens.next().getstr()
        assert "." == tokens.next().getstr()
        assert "value" == tokens.next().getstr()
        assert "-" == tokens.next().getstr()
        assert "value" == tokens.next().getstr()
        assert "NEWLINE" == tokens.next().getstr()
        assert "}" == tokens.next().getstr()
        assert "NEWLINE" == tokens.next().getstr()
        assert "}" == tokens.next().getstr()
        assert "NEWLINE" == tokens.next().getstr()
        assert "NEWLINE" == tokens.next().getstr()
        assert "let" == tokens.next().getstr()
        assert "test1" == tokens.next().getstr()
        assert "=" == tokens.next().getstr()
        assert "new" == tokens.next().getstr()
        assert "Test" == tokens.next().getstr()
        assert "(" == tokens.next().getstr()
        assert "12" == tokens.next().getstr()
        assert ")" == tokens.next().getstr()
        assert "NEWLINE" == tokens.next().getstr()
        assert "let" == tokens.next().getstr()
        assert "test2" == tokens.next().getstr()
        assert "=" == tokens.next().getstr()
        assert "new" == tokens.next().getstr()
        assert "Test" == tokens.next().getstr()
        assert "(" == tokens.next().getstr()
        assert "13" == tokens.next().getstr()
        assert ")" == tokens.next().getstr()
        assert "NEWLINE" == tokens.next().getstr()
        assert "let" == tokens.next().getstr()
        assert "result" == tokens.next().getstr()
        assert "=" == tokens.next().getstr()
        assert "test1" == tokens.next().getstr()
        assert "." == tokens.next().getstr()
        assert "compare" == tokens.next().getstr()
        assert "(" == tokens.next().getstr()
        assert "test2" == tokens.next().getstr()
        assert ")" == tokens.next().getstr()
        assert "NEWLINE" == tokens.next().getstr()
        assert "print" == tokens.next().getstr()
        assert "(" == tokens.next().getstr()
        assert "result" == tokens.next().getstr()
        assert ")" == tokens.next().getstr()
        assert "NEWLINE" == tokens.next().getstr()
        assert "}" == tokens.next().getstr()
    except LexingError, e:
        print "Idx: %d; Line no: %d; Col no: %d;\n" % (e.getsourcepos().idx, e.getsourcepos().lineno, e.getsourcepos().colno)
        pytest.fail(msg=repr(e.getsourcepos()))
