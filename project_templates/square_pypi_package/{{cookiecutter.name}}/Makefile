.PHONY: init
init:
	pip install --upgrade pip tox pre-commit
	pip install --upgrade -e ".[dev]"
	pre-commit install
	rm -rf .tox

.PHONY: clean
clean:
	rm -rf .tox
	rm -rf docs/_build
	rm -rf docs/api
