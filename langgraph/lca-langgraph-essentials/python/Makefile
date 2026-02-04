.PHONY: pytest pylint check
pylint:
	pylint --min-similarity-lines=100 *.py

pytest:
	pytest -s -v 

check: pytest pylint

clean:
	rm -rf __pycache__ faiss_index
