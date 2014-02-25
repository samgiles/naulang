import curses
from wlvlang.interpreter.bytecode import bytecode_names, Bytecode

class StackViewWindow(object):

    def __init__(self, stdscreen):
        width_height = stdscreen.getmaxyx()

        self._win = curses.newwin(width_height[0], width_height[1] / 2, 0, width_height[1] / 2 )
        self._win.box()

    def update_value(self, value):
        self._win.erase()
        try:
            self._win.addstr(1, 5, "Stack")
            self._win.addstr(2, 5, "=====")
            i = 4
            for line in value.split("\n"):
                try:
                    self._win.addstr(i, 3, line.rstrip())
                except curses.error:
                    pass
                i += 1
        except curses.error:
            pass

        self.refresh()

    def refresh(self):
        self._win.box()
        self._win.refresh()

class BytecodeViewWindow(object):
    def __init__(self, stdscreen):
        width_height = stdscreen.getmaxyx()

        self._stdscreen = stdscreen
        self._win = curses.newwin(width_height[0] / 2, width_height[1] / 2, width_height[0] / 2, 0)
        self._win.box()
        self.refresh()


    def draw_bytecodes(self, current_pc, method, interp):
        self._win.erase()
        height_width = self._stdscreen.getmaxyx()

        # Find a segment to display
        segment = min(len(method.bytecodes), (height_width[0] / 2) - 2)

        i = 1
        pc = current_pc
        while i < segment:

            if pc >= len(method.bytecodes):
                break

            bc = method.get_bytecode(pc)
            bytecode, offset = self.get_bytecode_info(pc, method, interp)

            if pc == current_pc:
                try:
                    self._win.addstr(i, 2, "->")
                except curses.error:
                    pass
            try:
                self._win.addstr(i, 5, bytecode.rstrip())
            except curses.error:
                pass
            pc += offset
            i += 1

        self.refresh()


    def get_bytecode_info(self, pc, method, interp):
        current_bytecode = method.get_bytecode(pc)
        current_bytecode_name = bytecode_names[current_bytecode]
        pc_offset = 0
        bytecode = "%03d: " % (pc)
        if current_bytecode == Bytecode.LOAD:
            bytecode += current_bytecode_name + ", local=" + str(method.get_bytecode(pc + 1))
            pc_offset = 2
        elif current_bytecode == Bytecode.LOAD_CONST:
            bytecode += current_bytecode_name + ", literal=" + str(method.get_bytecode(pc + 1))
            pc_offset = 2
        elif current_bytecode == Bytecode.STORE:
            bytecode += current_bytecode_name + ", local=" + str(method.get_bytecode(pc + 1))
            pc_offset = 2
        elif current_bytecode == Bytecode.JUMP_IF_FALSE or current_bytecode == Bytecode.JUMP_BACK:
            bytecode += current_bytecode_name + ", jump_to=" + str(method.get_bytecode(pc + 1))
            pc_offset = 2
        elif current_bytecode == Bytecode.INVOKE:
            bytecode += current_bytecode_name + ", local=" + str(method.get_bytecode(pc + 1))
            pc_offset = 2
        elif current_bytecode == Bytecode.INVOKE_GLOBAL:
            bytecode += current_bytecode_name + ", "
            globul = method.get_bytecode(pc + 1)
            name = interp.space.get_builtin_function(globul).identifier
            bytecode += "global=" + str(globul) + " (" + name + ")"
            pc_offset = 2
        elif current_bytecode == Bytecode.LOAD_DYNAMIC:
            bytecode += current_bytecode_name + ", local=" + str(method.get_bytecode(pc + 1)) + ", level=" + str(method.get_bytecode(pc + 2))
            pc_offset = 3
        elif current_bytecode == Bytecode.STORE_DYNAMIC:
            bytecode += current_bytecode_name + ", local=" + str(method.get_bytecode(pc + 1)) + ", level=" + str(method.get_bytecode(pc + 2))
            pc_offset = 3
        else:
            bytecode += current_bytecode_name
            pc_offset = 1

        return bytecode, pc_offset

    def refresh(self):
        self._win.box()
        self._win.refresh()

class View(object):

    def __init__(self, stdscreen):
        self._stdscreen = stdscreen
        self._stackview = StackViewWindow(stdscreen)
        self._bytecodeviews = []
        self._bytecodeview = None

    def get_key_press(self):
        self.refresh()
        return self._bytecodeview._win.getch()

    def load_method_bytecode(self, method, interp):
        if self._bytecodeview is not None:
            self._bytecodeviews.append(self._bytecodeview)

        self._bytecodeview = BytecodeViewWindow(self._stdscreen)
        self._bytecodeview.draw_bytecodes(0, method, interp)

    def update_stack_value(self, value):
        self._stackview.update_value(value)

    def update_bytecode_position(self, pc, method, interp):
        self._bytecodeview.draw_bytecodes(pc, method, interp)


    def refresh(self):
        self._stdscreen.refresh()
