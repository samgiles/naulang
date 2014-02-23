import sys

from wlvlang.main import main
from wlvlang.tools.interp_debugger.debug_interpreter import get_debugger

debugger = get_debugger()
main(sys.argv)
