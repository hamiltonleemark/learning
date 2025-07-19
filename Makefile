.PHONY: check
check: pylint test

.PHONY: pylint
pylint:
	pylint --recursive=y ./kafka ./machine

.PHONY: test
test:
	pytest ./machine/
