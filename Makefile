createdist:
	python setup.py sdist

clean:
	rm MANIFEST
	rm -rf dist/

.PHONY: createdist
