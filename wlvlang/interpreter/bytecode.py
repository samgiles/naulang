class Bytecode(object):
    HALT = chr(0)
    LOAD_CONST = chr(1)
    LOAD = chr(21)
    STORE = chr(2)
    OR = chr(3)
    AND = chr(4)
    EQUAL = chr(5)
    NOT_EQUAL = chr(6)
    LESS_THAN = chr(7)
    LESS_THAN_EQ = chr(8)
    GREATER_THAN = chr(9)
    GREATER_THAN_EQ = chr(22)
    ADD = chr(10)
    SUB = chr(11)
    MUL = chr(12)
    DIV = chr(13)
    NOT = chr(14)
    NEG = chr(15)
    JUMP_IF_FALSE = chr(16)
    JUMP_BACK = chr(17)
    PRINT = chr(18)
    INVOKE = chr(19)
    RETURN = chr(20)

    """
    ARRAY_LOAD
    Stack:

        array, index -> value
    """
    ARRAY_LOAD = chr(23)

    """
    ARRAY_STORE
    Stack:

        array, index, value ->
    """
    ARRAY_STORE = chr(24)

    STORE_DYNAMIC = chr(25)

    LOAD_DYNAMIC = chr(26)

    INVOKE_GLOBAL = chr(27)

def _bytecode_names(cls):
    "NOT_RPYTHON"
    """This function is only called a single time, at load time of this module.
    For RPypthon, this means, during translation of the module.
    """
    names = [attr for attr in dir(cls) if not callable(attr) and not attr.startswith("__")]
    vals = {}
    for name in names:
        vals[getattr(cls, name)] =  name

    return vals


bytecode_names = _bytecode_names(Bytecode)
