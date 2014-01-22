PYPYPATH=~/code/python/pypy/
PYTEST=py.test
PYTESTARGS=

all: test_parser test_interpreter test_vmobjects test_vm

createdist:
	python setup.py sdist

generate_parser:
	WORKSPACE=$(CURDIR) PYPYPATH=$(PYPYPATH) $(CURDIR)/wlvlang/compiler/generateparser.sh

test_parser: generate_parser
	@PYTHONPATH=$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/parser/test_*.py

test_compiler:
	@PYTHONPATH=$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/compiler/test_ast.py

test_interpreter:
	@PYTHONPATH=$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/interpreter/test_*.py

test_vm:
	@PYTHONPATH=$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/vm/test_*.py

test_vmobjects:
	@PYTHONPATH=$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/vmobjects/test_*.py

clean:
	rm -rf MANIFEST
	rm -rf dist/
	rm -rf build/

.PHONY: createdist
