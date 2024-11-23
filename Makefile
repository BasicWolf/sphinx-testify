BUILD_DIR=dist/
TEST_RESULTS_FILE=test_results.xml

all: flake8 mypy docs build

flake8:
	flake8 src/

mypy:
	MYPYPATH=src mypy -p sphinx_testify -p tests

test:
	PYTHONPATH=.:src/:$(PYTHONPATH) pytest --junitxml=$(TEST_RESULTS_FILE) tests/

docs: test
	$(MAKE) -C docs/ html

build:
	python3 -m build

clean:
	$(MAKE) -C docs/ clean
	rm $(BUILD_DIR) $(TEST_RESULTS_FILE)


help:
	@echo 'Usage:'
	@echo ''
	@echo '===DEVELOPMENT==='
	@echo '   make             run static checks, tests and build docs'
	@echo '   make flake8      run flake8 style checker'
	@echo '   make mypy        run mypy static type cheker'
	@echo '   make test        run unit and integration tests'
	@echo '   make docs        generate documentation'
	@echo '   make clean       remove all build artifacts '
	@echo ''
	@echo '===RELEASE==='
	@echo '   make dev-release     builds the package, bumps development version and uploads to PyPI'

.PHONY: docs
