all: test doc

test:
	PYTHONPATH=src/:$(PYTHONPATH) pytest --junitxml=test_result.xml src/test/

docs:
	$(MAKE) -C docs/ html


.PHONY: src docs
