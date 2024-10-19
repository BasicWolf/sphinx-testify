all:
	@echo 'Usage:'
	@echo '   make dev         make test and docs'
	@echo '   make test        run unit and integration tests'
	@echo '   make docs        generate documentation'


dev: test docs

test:
	PYTHONPATH=src/:$(PYTHONPATH) pytest --junitxml=test_result.xml src/test/

docs:
	$(MAKE) -C docs/ html


.PHONY: src docs
