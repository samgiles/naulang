from naulang.compiler.sourcemap import SourceMap


class DummyCodePosition:

    def __init__(self, val):
        self.val = val


def test_get_and_add():
    sourcemap = SourceMap()
    sourcemap.add(12, DummyCodePosition(909))
    assert sourcemap.get(12).val == 909
