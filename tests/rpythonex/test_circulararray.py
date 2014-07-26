from rpythonex.rcircular import CircularArray


class TestCircularArray(CircularArray):

    """ CircularArray is a _mixin_ RPython class.
    We therefore need to create a concrete version to make
    the annotator happy """

    def _create_new_instance(self, new_size):
        return TestCircularArray(new_size)


def test_size():
    array = TestCircularArray(3)
    assert array.size() == 8


def test_get_and_put():
    array = TestCircularArray(3)
    array.put(0, "Hello")
    assert array.get(0) == "Hello"


def test_grow():
    array = TestCircularArray(3)
    array.put(0, "Hello")
    new_array = array.grow(1, 0)
    assert new_array.size() == 16
    assert new_array.get(0) == "Hello"
