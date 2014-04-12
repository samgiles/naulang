PYPYPATH?=~/code/python/pypy/
PYTEST?=py.test
PYTESTARGS=
RPYTHON?=$(PYPYPATH)/rpython/bin/rpython

all: test_all

compile: bin/wlvlang-python wlvlang-no-jit

wlvlang-no-jit:
	@mkdir -p bin/
	PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(RPYTHON) --batch wlvlang/targetstandalone.py
	@mv ./wlvlang-nojit ./bin/

wlvlang-jit:
	@mkdir -p bin/
	PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(RPYTHON) --batch -Ojit wlvlang/targetstandalone.py
	@mv ./wlvlang-jit ./bin/

bin/wlvlang-python:
	@mkdir -p bin/
	@cat ./wlvlang/wlvlang-python.template | sed 's,{PYTHON_PATH},$(PYTHONPATH):$(PYPYPATH):.,g' > ./bin/wlvlang-python
	@chmod +x bin/wlvlang-python

createdist:
	python setup.py sdist

test_all: bin/wlvlang-python
	PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/**/test_*.py
	tests/functional/wlvtest.py ./bin/wlvlang-python ./tests/functional

test_all_compiled:
	PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/**/test_*.py
	tests/functional/wlvtest.py ./bin/wlvlang-nojit ./tests/functional

test_all_jit:
	PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/**/test_*.py
	tests/functional/wlvtest.py ./bin/wlvlang-jit ./tests/functional

test_compiler:
	@PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/compiler/test_*.py

test_interpreter:
	PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/interpreter/test_*.py

test_objectspace:
	@PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/objectspace/test_*.py

test_runtime:
	@PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/runtime/test_*.py

test_functional: bin/wlvlang-python
	tests/functional/wlvtest.py --xml ./bin/wlvlang-python ./tests/functional

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
