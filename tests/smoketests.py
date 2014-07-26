#!/usr/bin/env python
import sys
import argparse
import os

from os import kill
from signal import alarm, signal, SIGALRM, SIGKILL
from subprocess import PIPE, Popen


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Run a suite of programs in a naulang interpreter and report on failure states.')
    parser.add_argument('naulang_interpreter', nargs=1,
                        help='the interpreter executable to use to run the programs against')
    args = parser.parse_args()
    return args

# Imported from https://github.com/smarr/ReBench/blob/master/rebench/SubprocessWithTimeout.py


def run_with_timeout(args, cwd=None, shell=False, kill_tree=True, timeout=-1, stdout=PIPE, stderr=PIPE):
    '''
Run a command with a timeout after which it will be forcibly
killed.
'''
    class Alarm(Exception):
        pass

    def alarm_handler(signum, frame):
        raise Alarm

    p = Popen(args, shell=shell, cwd=cwd, stdout=stdout, stderr=stderr)
    if timeout != -1:
        signal(SIGALRM, alarm_handler)
        alarm(timeout)
    try:
        stdout, stderr = p.communicate()
        if timeout != -1:
            alarm(0)
    except Alarm:
        pids = [p.pid]
        if kill_tree:
            pids.extend(get_process_children(p.pid))
        for pid in pids:
            kill(pid, SIGKILL)
        return -9, '', ''
    return p.returncode, stdout, stderr


def get_process_children(pid):
    p = Popen('ps --no-headers -o pid --ppid %d' % pid, shell=True,
              stdout=PIPE, stderr=PIPE)
    stdout, _stderr = p.communicate()
    return [int(word) for word in stdout.split()]


if __name__ == '__main__':
    args = parse_arguments()

    executable = args.naulang_interpreter[0]

    test_files = [
        "sources/test_simple.wl",
        "sources/test_simple_function_decl.wl",
        "sources/test_simple_function.wl"
    ]

    cwd = os.getcwd()
    current_dir = os.path.dirname(os.path.realpath(__file__))
    failed = False
    for test_file in test_files:
        code, sout, serr = run_with_timeout(
            [executable, (current_dir + os.sep + test_file).replace(cwd, '')], cwd, timeout=10)
        if code != 0:
            failed = True
            print ("File %s failed:\n stderr:\n %s\n stdout:\n%s\n---------\n" %
                   (current_dir + os.sep + test_file, serr, sout))
    if failed:
        sys.exit(1)
    else:
        sys.exit(0)
