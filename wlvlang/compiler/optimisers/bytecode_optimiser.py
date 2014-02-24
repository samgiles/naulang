from wlvlang.interpreter.bytecode import Bytecode


class Optimiser(object):

    def __init__(self, optimisers):
        self.optimisers = optimisers

    def optimise(self, bytecode):
        for optimiser in self.optimisers:
            bytecode = optimiser.optimise(bytecode)

        return bytecode

class BytecodeOptimiser(object):
    """ Takes a bytecode array and performs a transformation """

    def optimise(self, bytecode):

        i = 0
        new_bytecodes = []

        while i < len(bytecode):
            new_bytes, advance = self.process_bytecode(i, bytecode)
            new_bytecodes = new_bytecodes + new_bytes
            i = i + advance

        return new_bytecodes

    def process_bytecode(self, i, bytecode):
        """ Returns the values that should be inserted at offset i and an offset to increase by """

        if  bytecode[i] == Bytecode.LOAD_CONST or  bytecode[i] == Bytecode.STORE or bytecode[i] == Bytecode.LOAD  or bytecode[i] == Bytecode.INVOKE or bytecode[i] == Bytecode.INVOKE_GLOBAL or bytecode[i] == Bytecode.JUMP_BACK or bytecode[i] == Bytecode.JUMP_IF_FALSE:
            return [bytecode[i], bytecode[i + 1]], 2
        elif bytecode[i] == Bytecode.LOAD_DYNAMIC or bytecode[i] == Bytecode.STORE_DYNAMIC:
            return [bytecode[i], bytecode[i + 1], bytecode[i + 2]], 3

        return [bytecode[i]], 1

class LoadLoadOptimiser(BytecodeOptimiser):
    def process_bytecode(self, i, bytecode):
        if bytecode[i] == Bytecode.LOAD:
            local = bytecode[i + 1]
            if bytecode[i + 2] == Bytecode.LOAD and bytecode[i + 3] == local:
                return [Bytecode.LOAD, local, Bytecode.DUP], 4

        return BytecodeOptimiser.process_bytecode(self, i, bytecode)

class LoadAndStoreOptimiser(BytecodeOptimiser):
    """ Removes redundant load and store operations """


    def process_bytecode(self, i, bytecode):
        new_bytecode = [0] * 2
        if bytecode[i] == Bytecode.STORE:
            local = bytecode[i+1]
            if bytecode[i + 2] == Bytecode.LOAD:
                if bytecode[i + 3] == local:
                    # Do replace
                    new_bytecode[0] = Bytecode.COPY_LOCAL
                    new_bytecode[1] = local
                    return new_bytecode, 2

        return BytecodeOptimiser.process_bytecode(self, i, bytecode)
