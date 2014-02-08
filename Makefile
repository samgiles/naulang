PYPYPATH=~/code/python/pypy/
PYTEST=py.test
PYTESTARGS=

all: test_compiler test_interpreter test_vmobjects test_vm

createdist:
	python setup.py sdist

test_compiler:
	@PYTHONPATH=$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/compiler/test_*.py

test_interpreter:
	@PYTHONPATH=$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/interpreter/test_*.py

test_vm:
	@PYTHONPATH=$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/vm/test_*.py

test_vmobjects:
	@PYTHONPATH=$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/vmobjects/test_*.py

test_full_run:
	@PYTHONPATH=$(PYPYPATH):. python wlvlang/targetstandalone.py tests/sources/test_simple.wl

clean:
	rm -rf MANIFEST
	rm -rf dist/
	rm -rf build/

.PHONY: createdist
