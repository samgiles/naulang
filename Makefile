PYPYPATH=~/code/python/pypy/

createdist:
	python setup.py sdist

generate_parser:
	cd ./wlvlang/compiler && PYPYPATH=$(PYPYPATH) WORKSPACE=i$(CURDIR)./generateparser.sh

test_parser: generate_parser
	PYTHONPATH=$(PYPYPATH):. py.test tests/parser/test_parser.py

clean:
	rm MANIFEST
	rm -rf dist/

.PHONY: createdist
