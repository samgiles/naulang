PYPYPATH=~/code/python/pypy/

createdist:
	python setup.py sdist

generate_parser:
	cd ./wlvlang/compiler && PYPYPATH=$(PYPYPATH) WORKSPACE=i$(CURDIR)./generateparser.sh

test_parser: generate_parser
	PYTHONPATH=$(PYPYPATH):. py.test tests/parser/test_parser.py
	PYTHONPATH=$(PYPYPATH):. py.test tests/parser/test_ast.py

test_interpreter:
	PYTHONPATH=$(PYPYPATH):. py.test tests/interpreter/test_activationrecord.py

clean:
	rm MANIFEST
	rm -rf dist/

.PHONY: createdist
