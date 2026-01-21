.PHONY: check
check: pylint test

.PHONY: pylint
pylint:
	pylint --recursive=y ./bedrock

.PHONY: test
test:
	pytest ./bedrock
