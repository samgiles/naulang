PYPYPATH?=~/code/python/pypy/
PYTEST?=py.test
PYTESTARGS=
RPYTHON?=$(PYPYPATH)/rpython/bin/rpython
PEP8SCRIPT?=/usr/local/bin/pep8

all: test_all

compile: bin/naulang-python naulang-no-jit

naulang-no-jit:
	@mkdir -p bin/
	PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(RPYTHON) --batch naulang/targetstandalone.py
	@mv ./naulang-nojit ./bin/

naulang-jit:
	@mkdir -p bin/
	PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(RPYTHON) --batch -Ojit naulang/targetstandalone.py
	@mv ./naulang-jit ./bin/

bin/naulang-python:
	@mkdir -p bin/
	@cat ./naulang/naulang-python.template | sed 's,{PYTHON_PATH},$(PYTHONPATH):$(PYPYPATH):.,g' > ./bin/naulang-python
	@chmod +x bin/naulang-python

createdist:
	python setup.py sdist

test_all: bin/naulang-python
	PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/**/test_*.py
	tests/functional/nautest.py ./bin/naulang-python ./tests/functional

test_all_compiled:
	PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/**/test_*.py
	tests/functional/nautest.py ./bin/naulang-nojit ./tests/functional

test_all_jit:
	PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/**/test_*.py
	tests/functional/nautest.py ./bin/naulang-jit ./tests/functional

test_compiler:
	@PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/compiler/test_*.py

test_interpreter:
	PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/interpreter/test_*.py

test_objectspace:
	@PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/objectspace/test_*.py

test_runtime:
	@PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/runtime/test_*.py

test_functional: bin/naulang-python
	tests/functional/nautest.py --xml ./bin/naulang-python ./tests/functional

pep8:
	@echo `find . -name \*.py -exec $(PEP8SCRIPT) {} \; | wc -l` PEP8 violations in this repository

pep8_verbose:
	@find . -name \*.py -exec $(PEP8SCRIPT) {} \;

build_extras:
	go build -ldflags='-s' tests/benchmarks/baselines/tokenring.go
	mv ./tokenring ./tokenring-go
	which kroc && kroc tests/benchmarks/baselines/tokenring.occ
	mv ./tokenring ./tokenring-occam

clean:
	rm -rf MANIFEST
	rm -rf dist/
	rm -rf build/

.PHONY: createdist pep8 pep8_verbose clean build build_extras all compile \
	naulang-nojit naulang-jit test_all test_all_compiled test_all_jit \
	test_compiler test_interpreter test_functional test_objectspace test_runtime
