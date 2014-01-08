from wlvlang.compiler.parser import parse_wlvlang
import pytest


class TestParser():

    def test_parse_if(self):
        ifexpression = """
        fn test() {
            if x == y and x == b {
                "hello";
            } else {
                "goodbye";
            }
        }"""

        parse_wlvlang(ifexpression)
