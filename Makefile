TEST_RESULTS_FILE=test_results.xml

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
	PYTHONPATH=.:src/:$(PYTHONPATH) pytest --junitxml=$(TEST_RESULTS_FILE) tests/

docs:
	$(MAKE) -C docs/ html

clean:
	$(MAKE) -C docs/ clean
	rm $(TEST_RESULTS_FILE)

.PHONY: src docs
