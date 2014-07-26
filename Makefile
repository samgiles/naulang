PYPYPATH?=~/code/python/pypy/
PYTEST?=py.test
PYTESTARGS=
RPYTHON?=$(PYPYPATH)/rpython/bin/rpython

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

build_extras:
	go build -ldflags='-s' tests/benchmarks/baselines/tokenring.go
	mv ./tokenring ./tokenring-go
	which kroc && kroc tests/benchmarks/baselines/tokenring.occ
	mv ./tokenring ./tokenring-occam

clean:
	rm -rf MANIFEST
	rm -rf dist/
	rm -rf build/

.PHONY: createdist
