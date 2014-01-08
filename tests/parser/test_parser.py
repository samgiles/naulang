import unittest

class ParserTester(unittest.TestCase):

    def test_parse_if(self):
        ifexpression = """
        fn test() {
            if x == y and x == b {
                "hello";
            } else {
                "goodbye";
            }
        }"""
