TEST_RESULTS_FILE=test_results.xml

all: build

build: flake8 mypy test docs

flake8:
	flake8 src/

mypy:
	MYPYPATH=src mypy -p sphinx_testify -p tests

test:
	PYTHONPATH=.:src/:$(PYTHONPATH) pytest --junitxml=$(TEST_RESULTS_FILE) tests/

docs:
	$(MAKE) -C docs/ html

clean:
	$(MAKE) -C docs/ clean
	rm $(TEST_RESULTS_FILE)

help:
	@echo 'Usage:'
	@echo '   make             run static checks, tests and build docs'
	@echo '   make flake8      run flake8 style checker'
	@echo '   make mypy        run mypy static type cheker'
	@echo '   make test        run unit and integration tests'
	@echo '   make docs        generate documentation'
	@echo '   make clean       remove all build artifacts '

.PHONY: docs
