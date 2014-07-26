#!/usr/bin/env python
import sys
import argparse
import os
import glob

from junit_xml import TestSuite, TestCase

from os import kill
from signal import alarm, signal, SIGALRM, SIGKILL
from subprocess import PIPE, Popen


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Run a suite of programs in a naulang interpreter and test output against expected values.')
    parser.add_argument('naulang_interpreter', nargs=1,
                        help='the interpreter executable to use to run the programs against')
    parser.add_argument('test_directory', nargs=1, help='the directory in which the .wlt files exist')
    parser.add_argument("--xml", help="output JUnit style XML", action="store_true")
    args = parser.parse_args()
    return args


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
    test_directory = args.test_directory[0]
    xml_out = args.xml
    test_cases = []

    # TODO: Timing on the test cases in XML
    def log_errord(test_name, stderr, stdout):
        if xml_out:
            tc = TestCase(test_name, executable, 0, stdout, stderr)
            tc.add_error_info(message="Test Error\n", output=stdout)
            test_cases.append(tc)
        else:
            print "Test %s failed:\nstderr:\n %s\nstdout:\n%s\n----------\n" % (test_name, stderr, stdout)

    def log_failed(test_name, actual, expected):
        if xml_out:
            tc = TestCase(test_name, executable, 0, actual, "")
            tc.add_failure_info(message="Test Failed\nExpected:\n%s\nActual:\n%s" % (expected, actual))
            test_cases.append(tc)
        else:
            print "Test %s failed:\nexpected:\n%s\nactual:\n%s\n---------\n" % (test_name, expected, actual)

    def log_passed(test_name):
        if xml_out:
            test_cases.append(TestCase(test_name, executable, 0, "", ""))
        else:
            print "Test %s passed\n" % test_name

    test_files = glob.glob1(test_directory, "*.wl")

    failed = False
    for test_file in test_files:

        # Get the test_name from the file name so we can determine which spec file we should test it against
        test_name = os.path.splitext(test_file)[0]
        expected_output = test_directory + os.sep + test_name + ".spec"

        if not os.path.isfile(expected_output):
            raise Exception("Could not find expected_output file for test %r" % test_name)

        # Actually run the test
        code, sout, serr = run_with_timeout([executable, test_directory + os.sep + test_file], os.getcwd(), timeout=10)

        if code != 0:
            failed = True
            log_errord(test_name, serr, sout)
        else:
            with open(expected_output, "r") as f:
                expected = f.read()

            if sout != expected:
                failed = True
                log_failed(test_name, sout, expected)
            else:
                log_passed(test_name)

    if xml_out:
        test_suite = TestSuite("Functional Tests", test_cases)
        print TestSuite.to_xml_string([test_suite])

    if failed and not xml_out:
        sys.exit(1)
    else:
        sys.exit(0)
