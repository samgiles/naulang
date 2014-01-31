class Bytecode(object):

    HALT       = 0
    SEND       = 1
    BRANCH     = 2
    ADD     = 3
    SUB     = 4
    MUL     = 5
    DIV     = 6
    MOD     = 7
    PUSH    = 8
    POP     = 9


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
