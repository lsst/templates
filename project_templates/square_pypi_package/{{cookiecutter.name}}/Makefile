.PHONY: help
help:
	@echo "Make targets for {{cookiecutter.name}}:"
	@echo "make clean - Remove generated files"
	@echo "make init - Set up dev environment (install pre-commit hooks)"
	@echo "make update - Update pre-commit dependencies and run make init"
	@echo "make update-deps - Update pre-commit dependencies"

.PHONY: clean
clean:
	rm -rf .nox
	rm -rf docs/_build
	rm -rf docs/api

.PHONY: init
init:
	uv sync --frozen --all-groups
	uv run prek install

.PHONY: update
update: update-deps init

.PHONY: update-deps
update-deps:
	uv lock --upgrade
	uv run --only-group=lint prek autoupdate
