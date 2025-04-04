.PHONY: check
check: pylint test

.PHONY: pylint
pylint:
	pylint --recursive=y ./kafka

.PHONY: test
test:
	pytest test_repository.py