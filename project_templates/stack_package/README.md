# stack_package

**LSST DM EUPS Stack package.**

## Template variables

### cookiecutter.package_name

EUPS package name.
This is the name of the repository and the directory.

### cookiecutter.python_module

The package's Python namespace.
Normally this is a sub-package of `lsst`, and based on the EUPS package name.
For example, the Python namespace of the `pipe_base` package is `lsst.pipe.base`.

This variable is automatically computed from `cookiecutter.package_name`.

### cookiecutter.python_sub_dirs

The directory path where the Package's Python code is located.
For example, this variable is `lsst/pipe/base` for the `pipe_base` package.

This variable is automatically computed from `cookiecutter.python_module`.

### cookiecutter.copyright_year

The year, or years that the named institution made contributions.
For consecutive years, use a dash (`2016-2018`).
For nonconsecutive years, use a comma (`2016, 2018`).

The default is the current year.

### cookiecutter.copyright_holder

Legal name of the institution that claims copyright.
The choice list covers all DM institutions.
If you need to assign a copyright to a different institution, you can modify the search-and-replace after the package is created.

### cookiecutter.github_org

GitHub organization where the repository is located.
Supported Stack packages are always located in the `lsst` organization.

### cookiecutter.uses_cpp

If `true` (default), the package is configured to support C++ and pybind11 code.
If `false`, the generated package is Python-only.
