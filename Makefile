all:
	@echo 'Usage:'
	@echo '   make dev         make test and docs'
	@echo '   make test        run unit and integration tests'
	@echo '   make docs        generate documentation'


build: flake8 mypy test docs

flake8:
	flake8 src/

mypy:
	MYPYPATH=src mypy -p sphinx_testify -p tests

test:
	PYTHONPATH=.:src/:$(PYTHONPATH) pytest --junitxml=test_results.xml tests/

docs:
	$(MAKE) -C docs/ html


.PHONY: src docs
