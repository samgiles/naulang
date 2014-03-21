from rpythonex.rcircular import CircularArray

def test_size():
    array = CircularArray(3)
    assert array.size() == 8

def test_get_and_put():
    array = CircularArray(3)
    array.put(0, "Hello")
    assert array.get(0) == "Hello"

def test_grow():
    array = CircularArray(3)
    array.put(0, "Hello")
    new_array = array.grow(1, 0)
    assert new_array.size() == 16
    assert new_array.get(0) == "Hello"
