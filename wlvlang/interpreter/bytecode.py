class Bytecode(object):
    HALT = 0
    LOAD_CONST = 1
    STORE = 2
    OR = 3
    AND = 4
    EQUAL = 5
    NOT_EQUAL = 6
    LESS_THAN = 7
    LESS_THAN_EQ = 8
    GREATER_THAN = 9
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


def _sorted_bytecode_names(cls):
    "NOT_RPYTHON"
    """This function is only called a single time, at load time of this module.
    For RPypthon, this means, during translation of the module.

    Simple helper identical to https://github.com/SOM-st/RPySOM/blob/master/src/som/interpreter/bytecodes.py#L87
    """
    return [key.upper() for value, key in \
           sorted([(value, key) for key, value in cls.__dict__.items()]) \
           if isinstance(value, int) and key[0] != "_"
           ]

_bytecode_names = _sorted_bytecode_names(Bytecode)
