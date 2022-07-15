# SQuaRE PyPI Package

**Develop a Python package for PyPI following SQuaRE's standard practices.**

Technologies:

- setuptools for packaging
- setuptools_scm for version string management
- Tox for development task orchestration
- Pre-commit for linting, with black, isort, flake8, and more
- Pytest for unit testing
- Mypy for type checking
- GitHub Actions for continuous integration and releases
- Sphinx for documentation

## Template variables

### cookiecutter.pypi_name

This is the name of the Python package on PyPI and also the name of the GitHub repository.
Formatting tips:

- Use lower case.
- A single word is best (i.e. ``documenteer`` or ``safir``).
- If you need multiple words, use a hyphen as a separator rather than an underscore (i.e. ``rubin-gizmo``).

### cookiecutter.module_name

This is the name of the package's Python module, based on its PyPI package name.
This should be all lower case, and ideally a single word.
If there are multiple words in the PyPI name, consider squishing those words into a single word for the module name.
If that doesn't work, as a last resort, use an underscore to concatenate words (however, we view underscores in package names as un-pythonic).

### cookiecutter.description

A one-sentence description of the package.
This is used as the GitHub repository summary, in the README, and in the PyPI package summary.

### cookiecutter.copyright_year

The year, or years that the named institution made contributions.
For consecutive years, use a dash (`2016-2018`).
For nonconsecutive years, use a comma (`2016, 2018`).

The default is the current year.

### cookiecutter.copyright_holder

Legal name of the institution that claims copyright.
The choice list covers all DM institutions.
If you need to assign a copyright to a different institution, you can modify the search-and-replace after the package is created.
For more details, see [Managing license and copyright in Stack packages](https://developer.lsst.io/stack/license-and-copyright.html).

### cookiecutter.github_org

The GitHub organization where the app resides.
For SQuaRE workers, this should be `lsst-sqre`.
To test template production, use `lsst-sqre-testing`.

## Examples

The [example](example) directory is a package created using only the template defaults.
