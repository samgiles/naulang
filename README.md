# naulang

[![Build Status](https://travis-ci.org/samgiles/naulang.svg?branch=master)](https://travis-ci.org/samgiles/naulang)

In process of renaming from naulang to naulang.

naulang is an experimental language and interpreter implementation written in RPython.

It is a piece of software complementing an undergraduate computer science dissertation.



## Building

There are two build targets for naulang, a standard, non-JITed interpreter build and a build that includes a tracing JIT compiler and optimiser.  Instructions for building each of these is presented below.


### Prerequisites

To build you need a copy of the [PyPy project](http://pypy.org/) source code obtained from [here](https://bitbucket.org/pypy/pypy "PyPy Bitbucket").


You should then set a `PYPYPATH` environment variable to your downloaded copy when running `make`.

You should also run `pip install -r requirements.txt`

### Interpreter

To build the plain interpreter run:

`make compile PYPYPATH=path/to/your/pypy`

This takes ~60s on an Intel 4770k processor with 8GB RAM on Ubuntu 13.10.

### JIT compiler enabled Interpreter

To build the JITed interpreter run:

`make naulang-jit PYPYPATH=path/to/your/pypy`

This takes ~250s on an Intel 4770k processor with 8GB RAM on Ubuntu 13.10.
