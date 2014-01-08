import pytest
from wlvlang.compiler.parser import parse_wlvlang

def test_parse_if():
    ifexpression = """
    fn test() {
        if x == y and x == b {
            "hello";
        } else {
            "goodbye";
        }
    }"""

    parse_wlvlang(ifexpression)
    assert True
