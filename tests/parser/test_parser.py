import pytest
from rpython.rlib.parsing.parsing import ParseError
from wlvlang.compiler.parser import parse_wlvlang

def test_assignment_statement():

    immutable_assignment = """
    let x = 10;
    let y = true;
    """
    try:
        s = parse_wlvlang(immutable_assignment)
    except ParseError, e:
        pytest.fail(e.nice_error_message(source=immutable_assignment))

    repr(s)
    assert True
