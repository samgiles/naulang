from wlvlang.interpreter.bytecode import bytecode_names

class Disassembler(object):

    def disassemble(self, method):
        bytecodes = method._bytecodes
        self.print_bytecodes(bytecodes)

    def print_bytecodes(self, bytecodes):
        codes = []
        for bc in bytecodes:
            try:
                codes.append(bytecode_names[bc])
            except KeyError:
                codes.append(bc)

        print repr(codes)

