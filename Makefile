PYPYPATH=~/code/python/pypy/

createdist:
	python setup.py sdist


test_parser:
	PYTHONPATH=$(PYPYPATH):. py.test tests/parser/test_parser.py

clean:
	rm MANIFEST
	rm -rf dist/

.PHONY: createdist
