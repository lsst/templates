# Change log

## 2018-07-13

- Deleted the `ups/*.build` file.
  It turns out that this file is not used by the build system.

- Added `pyList` argument to the `tests/Sconscript` file.
  This enables auto file detection.

- Updated the `setup.cfg` configuration file.
  This adds the N806 flake8 exception and the `[tool:pytest]` section.

- Updated the default `automodapi` usage in module documenation homepages.

  - `no-main-docstr` is something we always want to use since the main docstring in `__init__.py` shouldn't be used, in favour of writing topics in the `doc/` directory.

  - Most modules don't have interesting class inheritance, so it makes sense to default to `no-inheritance-diagram`.

([DM-15110](https://jira.lsstcorp.org/browse/DM-15110))

## 2018-07-06

- Add a `uses_python` configuration in `cookiecutter.json`.
  When both `uses_python` and `uses_cpp` are `False`, the package is data-only (like `afwdata` or `verify_metrics`, for example).
  See the `example_dataonly` example package.

- The package homepage (`doc/{{cookiecutter.package_name}}/index.rst`) now only appears for data-only packages.
  Similarly, the module homepage (`doc/{{cookiecutter.python_module}}/index.rst`) now only appears for packages that provide a Python module.

- Redesigned the package and module homepages to both have a Contributing section (replacing the project info section formerly in the package homepage).
  The contributing section links to the GitHub repository and Jira component.
  This section can be expanded with a toctree to link to topics about how to develop the module or package itself.
  The template also includes a commented-out "Using" section that provides a toctree for linking to topics related to using the package or module.

- The `statics` field in `doc/manifest.yaml` is now commented out by default.
  Most packages don't need a static content directory.

([DM-15024](https://jira.lsstcorp.org/browse/DM-15024))

## 2018-06-21

- Add `disableCc=True` argument to the `SConstruct` for Python-only packages.
  ([DM-14860](https://jira.lsstcorp.org/browse/DM-14860))

## 2018-06-04

- Remove version pinning from `ups/{{package_name}}.table`.
  Version pinning isn't used anymore since all packages are tagged together.
  ([DM-14668](https://jira.lsstcorp.org/browse/DM-14668))
