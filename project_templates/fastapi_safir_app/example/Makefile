.PHONY: help
help:
	@echo "Make targets for Gafaelfawr"
	@echo "make init - Set up dev environment"
	@echo "make run - Start a local development instance"
	@echo "make update - Update pinned dependencies and run make init"
	@echo "make update-deps - Update pinned dependencies"
	@echo "make update-deps-no-hashes - Pin dependencies without hashes"

.PHONY: init
init:
	pip install --upgrade pip
	pip install --upgrade pre-commit tox
	pip install --editable .
	pip install --upgrade -r requirements/main.txt -r requirements/dev.txt
	rm -rf .tox
	pre-commit install

.PHONY: run
run:
	tox run -e run

.PHONY: update
update: update-deps init

# The dependencies need --allow-unsafe because kubernetes-asyncio and
# (transitively) pre-commit depends on setuptools, which is normally not
# allowed to appear in a hashed dependency file.
.PHONY: update-deps
update-deps:
	pip install --upgrade pip
	pip install --upgrade pre-commit
	pre-commit autoupdate
	pip install --upgrade pip-tools pip setuptools
	pip-compile --upgrade --resolver=backtracking --build-isolation	\
	    --allow-unsafe --generate-hashes				\
	    --output-file requirements/main.txt requirements/main.in
	pip-compile --upgrade --resolver=backtracking --build-isolation	\
	    --allow-unsafe --generate-hashes				\
	    --output-file requirements/dev.txt requirements/dev.in

# Useful for testing against a Git version of Safir.
.PHONY: update-deps-no-hashes
update-deps-no-hashes:
	pip install --upgrade pip-tools pip setuptools
	pip-compile --upgrade --resolver=backtracking --build-isolation	\
	    --allow-unsafe						\
	    --output-file requirements/main.txt requirements/main.in
	pip-compile --upgrade --resolver=backtracking --build-isolation	\
	    --allow-unsafe						\
	    --output-file requirements/dev.txt requirements/dev.in
