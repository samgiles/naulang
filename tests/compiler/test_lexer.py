import pytest

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
