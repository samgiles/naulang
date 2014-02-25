class Bytecode(object):
    HALT = 0
    LOAD_CONST = 1
    LOAD = 3
    STORE = 4
    OR = 5
    AND = 6
    EQUAL = 7
    NOT_EQUAL = 8
    LESS_THAN = 9
    LESS_THAN_EQ = 10
    GREATER_THAN = 11
    GREATER_THAN_EQ = 12
    ADD = 13
    SUB = 14
    MUL = 15
    DIV = 16
    NOT = 17
    NEG = 18
    JUMP_IF_FALSE = 19
    JUMP_BACK = 20
    PRINT = 21
    INVOKE = 22
    RETURN = 23

    """
    ARRAY_LOAD
    Stack:

        array, index -> value
    """
    ARRAY_LOAD = 24

    """
    ARRAY_STORE
    Stack:

        array, index, value ->
    """
    ARRAY_STORE = 25

    STORE_DYNAMIC = 26

    LOAD_DYNAMIC = 27

    INVOKE_GLOBAL = 28
    MOD = 29
    COPY_LOCAL = 30
    DUP = 31

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
