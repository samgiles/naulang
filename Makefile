PYPYPATH?=~/code/python/pypy/
PYTEST?=py.test
PYTESTARGS=
RPYTHON?=$(PYPYPATH)/rpython/bin/rpython

all: test_compiler test_interpreter test_vmobjects test_vm

compile: wlvlang-no-jit

wlvlang-no-jit:
	mkdir -p bin/
	PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(RPYTHON) --batch wlvlang/targetstandalone.py
	mv ./wlvlang-nojit ./bin/

wlvlang-jit:
	mkdir -p bin/
	PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(RPYTHON) --batch -Ojit wlvlang/targetstandalone.py
	mv ./wlvlang-jit ./bin/

wlvlang-python:
	mkdir -p bin/
	cat ./wlvlang/wlvlang-python | sed 's,{PYTHON_PATH},$(PYTHONPATH):$(PYPYPATH):.,g' > ./bin/wlvlang-python
	chmod +x bin/wlvlang-python

createdist:
	python setup.py sdist

test_compiler:
	@PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/compiler/test_*.py

test_interpreter:
	PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/interpreter/test_*.py

test_vm:
	@PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/vm/test_*.py

test_vmobjects:
	@PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/vmobjects/test_*.py

test_full_run:
	PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. python wlvlang/targetstandalone.py tests/sources/test_simple_function.wl

clean:
	rm -rf MANIFEST
	rm -rf dist/
	rm -rf build/

.PHONY: createdist
