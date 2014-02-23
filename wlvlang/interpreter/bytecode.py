class Bytecode(object):
    HALT = 0
    LOAD_CONST = 1
    LOAD = 21
    STORE = 2
    OR = 3
    AND = 4
    EQUAL = 5
    NOT_EQUAL = 6
    LESS_THAN = 7
    LESS_THAN_EQ = 8
    GREATER_THAN = 9
    GREATER_THAN_EQ = 22
    ADD = 10
    SUB = 11
    MUL = 12
    DIV = 13
    NOT = 14
    NEG = 15
    JUMP_IF_FALSE = 16
    JUMP_BACK = 17
    PRINT = 18
    INVOKE = 19
    RETURN = 20

    """
    ARRAY_LOAD
    Stack:

        array, index -> value
    """
    ARRAY_LOAD = 23

    """
    ARRAY_STORE
    Stack:

        array, index, value ->
    """
    ARRAY_STORE = 24

    STORE_DYNAMIC = 25

    LOAD_DYNAMIC = 26

    INVOKE_GLOBAL = 27
    MOD = 28

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
