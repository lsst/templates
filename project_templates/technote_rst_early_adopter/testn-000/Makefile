.PHONY:
init:
	pip install tox pre-commit
	pre-commit install

.PHONY:
html:
	tox run -e html

.PHONY:
lint:
	tox run -e lint,link-check

.PHONY:
clean:
	rm -rf _build
	rm -rf .technote
	rm -rf .tox
