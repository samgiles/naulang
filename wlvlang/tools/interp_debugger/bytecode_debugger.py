import sys
import curses
import signal
from wlvlang.main import main
from wlvlang.tools.interp_debugger.debug_interpreter import get_debugger

from wlvlang.tools.interp_debugger.debugger_ui import View


def _run(stdscr):
    debugger = get_debugger()
    debugger.set_view(View(stdscr))
    main(sys.argv)

curses.wrapper(_run)

