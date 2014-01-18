PYPYPATH=~/code/python/pypy/
PYTEST=py.test
PYTESTARGS=

all: test_parser test_interpreter test_vmobjects

createdist:
	python setup.py sdist

generate_parser:
	cd ./wlvlang/compiler && PYPYPATH=$(PYPYPATH) WORKSPACE=i$(CURDIR)./generateparser.sh

test_parser: generate_parser
	@PyTHONPATH=$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/parser/test_parser.py
	@PYTHONPATH=$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/parser/test_ast.py

test_interpreter:
	@PYTHONPATH=$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/interpreter/test_activationrecord.py

test_vmobjects:
	@PYTHONPATH=$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/vmobjects/test_symbol.py

clean:
	rm MANIFEST
	rm -rf dist/

.PHONY: createdist
