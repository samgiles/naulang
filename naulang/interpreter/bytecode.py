from rpython.rlib import jit


class Bytecode(object):
    # Halt the current function activation.
    # This is analogous to a 'return' statement
    # without a return expression.
    # HALT;
    HALT = 0

    # Load Constant loads a constant literal from the
    # stack frame for the currently executing frame.
    # The value is placed on the top of the stack.
    # It takes a single argument pointing to the
    # offset in the literal array for the frame.
    # LOAD_CONST [literal];
    LOAD_CONST = 1

    # Load loads the data stored in a name.  At compile
    # time a name is assigned a numeric value within each
    # function, then, at runtime these names are referred
    # to using its offset.
    # LOAD [variable];
    LOAD = 2
    STORE = 3
    OR = 4
    AND = 5
    EQUAL = 6
    NOT_EQUAL = 7
    LESS_THAN = 8
    LESS_THAN_EQ = 9
    GREATER_THAN = 10
    GREATER_THAN_EQ = 11
    ADD = 12
    SUB = 13
    MUL = 14
    DIV = 15
    NOT = 16
    NEG = 17
    JUMP_IF_FALSE = 18
    JUMP = 19
    PRINT = 20
    INVOKE = 21
    RETURN = 22
    ARRAY_LOAD = 23
    ARRAY_STORE = 24
    STORE_DYNAMIC = 25
    LOAD_DYNAMIC = 26
    INVOKE_GLOBAL = 27
    MOD = 28
    COPY_LOCAL = 29
    DUP = 30
    INVOKE_ASYNC = 31
    CHAN_OUT = 32
    CHAN_IN = 33

_stack_effect_depends_on_args = -9999

_stack_effects = [
    0,  # halt
    1,  # load_const
    1,  # load
    -1,  # store
    -1,  # or
    -1,  # and
    -1,  # equal
    -1,  # not_equal
    -1,  # less_than
    -1,  # less_than_eq
    -1,  # greater_than
    -1,  # greater_than_eq
    -1,  # add
    -1,  # sub
    -1,  # mul
    -1,  # div
    0,  # not
    0,  # neg
    -1,  # jump_if_false
    0,  # jump_back
    -1,  # print
    _stack_effect_depends_on_args,  # invoke
    -1,  # return
    -1,  # array_load
    -3,  # array_store
    -1,  # store_dynamic
    1,  # load_dynamic
    _stack_effect_depends_on_args,  # invoke_global
    -1,  # mod
    0,  # copy_local
    1,  # dup
    _stack_effect_depends_on_args,  # invoke async
    0,  # chan out
    -2,  # chan in
]


_bytecode_lengths = [
    1,  # halt
    2,  # load_const
    2,  # load
    2,  # store
    1,  # or
    1,  # and
    1,  # equal
    1,  # not_equal
    1,  # less_than
    1,  # less_than_eq
    1,  # greater_than
    1,  # greater_than_eq
    1,  # add
    1,  # sub
    1,  # mul
    1,  # div
    1,  # not
    1,  # neg
    2,  # jump_if_false
    2,  # jump_back
    1,  # print
    1,  # invoke
    1,  # return
    1,  # array_load
    1,  # array_store
    3,  # store_dynamic
    3,  # load_dynamic
    2,  # invoke_global
    1,  # mod
    1,  # copy_local
    1,  # dup
    1,  # invoke async
    1,  # chan out
    1,  # chan in
]


@jit.elidable
def get_bytecode_length(bytecode):
    assert bytecode >= 0 and bytecode < len(_bytecode_lengths)
    return _bytecode_lengths[bytecode]


@jit.elidable
def get_stack_effect(bytecode, number_of_arguments=0):
    assert bytecode >= 0 and bytecode < len(_stack_effects)
    if _stack_effects[bytecode] == _stack_effect_depends_on_args:
        return -number_of_arguments + 1

    return _stack_effects[bytecode]


@jit.elidable
def stack_effect_depends_on_args(bytecode):
    assert bytecode >= 0 and bytecode < len(_stack_effects)
    return _stack_effects[bytecode] == _stack_effect_depends_on_args


def disassemble(bytecodes):
    index = 0
    values = []
    while index < len(bytecodes):
        bytecode = bytecodes[index]
        values.append(bytecode_names[bytecode])
        length = get_bytecode_length(bytecode)
        arg = 1
        while arg < length:
            values.append(str(bytecodes[index + arg]))
            arg += 1

        index += length

    return values


def _bytecode_names(cls):
    "NOT_RPYTHON"
    """This function is only called a single time, at load time of this module.
    For RPypthon, this means, during translation of the module.
    """
    names = [attr for attr in dir(cls) if not callable(attr) and not attr.startswith("__")]
    vals = {}
    for name in names:
        vals[getattr(cls, name)] = name

    return vals


bytecode_names = _bytecode_names(Bytecode)

# These assertions will be enforced at compile time.
# They exist purely to catch programmer errors
assert len(_stack_effects) == len(bytecode_names)
assert len(_bytecode_lengths) == len(bytecode_names)
