from csp.csp import *
import sys
import math

ChanType = Channel

@process
def sieve(count, cin, cout):
    n = cin.read()
    cout.write(n)
    if count == 0:
        return

    newchanin = ChanType()
    Par(_filter(n, cin, newchanin), sieve(count - 1, newchanin, cout)).start()

@process
def _from(start, step, c):
    count = start
    while True:
        c.write(count)
        count += step

@process
def _filter(n, cin, cout):
    while True:
        a = cin.read()
        if (a % n) != 0:
            cout.write(a)
@process
def primes(chanout, limit):
    c = ChanType()
    Par(_from(2, 1, c), sieve(limit, c, chanout)).start()

def sum_primes(n):
    chanout = ChanType()

    primes(chanout, n).start()
    _sum = 0
    for i in range(0, n):
        prime = chanout.read()
        _sum += prime

    chanout.poison()
    return _sum

if __name__ == '__main__':
    import time
    warmup = 10
    for i in range(0, warmup):
        sum_primes(100)


    t0 = time.time()
    sum_primes(100)
    t1 = time.time()

    print "pythoncsp-primesieve-sync(100): total: iterations=1 runtime=%dus" % int(math.ceil((t1 - t0) * 1000000))
    sys.exit(0)
