.PHONY: check
check: pylint test

.PHONY: pylint
pylint:
	pylint --recursive=y ./*.py

.PHONY: test
test:
	pytest *.py
