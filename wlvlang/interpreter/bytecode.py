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
