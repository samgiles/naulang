import sys
from wlvlang.main import main

def entry_point(argv):
    return main(argv)

def target(driver, args):
    if driver.config.translation.jit:
        driver.exe_name = "wlvlang-jit"
    else:
        driver.exe_name = "wlvlang-nojit"
    driver.config.translation.thread = True
    return entry_point

def jitpolicy(driver):
    from rpython.jit.codewriter.policy import JitPolicy
    return JitPolicy()


if __name__ == '__main__':
    from rpython.translator.driver import TranslationDriver
    entry = target(TranslationDriver(), sys.argv)
    sys.exit(entry(sys.argv))
