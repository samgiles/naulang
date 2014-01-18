PYPYPATH=~/code/python/pypy/
JUNITSTYLE=
PYTEST=py.test $(JUNITSTYILE)

all: test_parser test_interpreter test_vmobjects

createdist:
	python setup.py sdist

generate_parser:
	cd ./wlvlang/compiler && PYPYPATH=$(PYPYPATH) WORKSPACE=i$(CURDIR)./generateparser.sh

test_parser: generate_parser
	PYTHONPATH=$(PYPYPATH):. $(PYTEST) tests/parser/test_parser.py
	PYTHONPATH=$(PYPYPATH):. $(PYTEST) tests/parser/test_ast.py

test_interpreter:
	PYTHONPATH=$(PYPYPATH):. $(PYTEST) tests/interpreter/test_activationrecord.py

test_vmobjects:
	PYTHONPATH=$(PYPYPATH):. $(PYTEST) tests/vmobjects/test_symbol.py

clean:
	rm MANIFEST
	rm -rf dist/

.PHONY: createdist
