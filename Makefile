TEST_RESULTS_FILE=test_results.xml

all: flake8 mypy test docs

flake8:
	flake8 src/

mypy:
	MYPYPATH=src mypy -p sphinx_testify -p tests

test:
	PYTHONPATH=.:src/:$(PYTHONPATH) pytest --junitxml=$(TEST_RESULTS_FILE) tests/

docs:
	$(MAKE) -C docs/ html

release-dev: update-dev-version build upload

update-dev-version: _require_running_from_github_actions
	./script/update-dev-revision.sh pyproject.toml
	git config user.name 'github-actions[bot]'
	git config user.email 'github-actions[bot]@users.noreply.github.com'
	git add .
	git commit -m "Bump development version"
	git push

_require_running_from_github_actions:
ifneq ($(GITHUB_ACTIONS),true)
	@echo "Not running inside GitHub Actions."
	@exit 1
endif

build:
	python3 -m build

upload:
	python3 -m twine upload --repository testpypi dist/*


clean:
	$(MAKE) -C docs/ clean
	rm $(TEST_RESULTS_FILE)



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
