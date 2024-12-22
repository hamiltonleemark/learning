.PHONY: check
check: pylint

.PHONY: pylint
pylint:
	pylint --recursive=y ./kafka
