# stack_package

**LSST DM EUPS Stack package.**

## Template variables

### cookiecutter.package_name

EUPS package name.
This is the name of the repository and the directory.

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

### cookiecutter.python_module

The package's Python namespace.
Normally this is a sub-package of `lsst`, and based on the EUPS package name.
For example, the Python namespace of the `pipe_base` package is `lsst.pipe.base`.

A default for this variable is automatically computed from `cookiecutter.package_name`.

### cookiecutter.python_sub_dirs

The directory path where the Package's Python code is located.
For example, this variable is `lsst/pipe/base` for the `pipe_base` package.

A default for this variable is automatically computed from `cookiecutter.package_name`.

## Examples

This project template has multiple examples that demonstrate different configurations.

### example/

The [example](example) directory is a Stack package created using only the template defaults.

### example_subpackage/

The [example_subpackage](example_subpackage) directory shows a Stack package with a three-level Python namespace (`lsst.example.subpackage`).
Packages with deep namespaces need [`__init__.py` files](example_subpackage/python/lsst/example/__init__.py) at each level that extend the namespace.

### example_pythononly/

The [example_pythononly](example_pythononly) directory shows a Stack package that only includes Python code (and no C++ sources).
Such packages don't have `lib`, `include`, and `src` directories.
Some of the dependencies configured in the [`ups` directory](example_pythononly/ups) are also different.

## Files

### COPYRIGHT

Example: [COPYRIGHT](example/COPYRIGHT).

Record copyright claims in this file, one line per institution.
See the [copyright](../../file_templates/copyright) template.

### LICENSE

Example: [LICENSE](example/LICENSE).

The license for all DM Stack package is GPL v3.0 (see the [license_gplv3](../../file_templates/license_gplv3) template).
The license should not be modified.

### README.rst

Example: [README.rst](example/README.rst).

Beyond the templated structure, you'll need to customize this README with a short (one sentence) description of what the package is for.
(*Tip:* this sentence should also be used for the GitHub repo description).

We keep the README fairly minimal, providing just enough information to help a person browsing packages via GitHub.
Put the bulk of the documentation in the `doc/` directory.

### SConstruct

Example: [SConstruct](example/SConstruct).

Scons (extended by sconsUtils) uses this `SConstruct` file.
The only customization is the package name argument for the `lsst.sconsUtils.scripts.BasicSConstruct` builder.

### setup.cfg

Example: [setup.cfg](example/setup.cfg).

Python utilities, like the flake8 linter, use `setup.cfg` for configuration.
This file is generally standardized across all packages and shouldn't be customized.

### bin.src/SConscript

Example: [bin.src/SConscript](example/bin.src/SConscript).

Scons (extended by sconsUtils) uses this `SConstruct` file.
You shouldn't need to modify this file.

The `bin.src/` directory is where you put Python scripts (including command-line task executables) that are installed for users.

### doc/{{cookiecutter.package_name}}/index.rst

Example: [doc/example/index.rst](example/doc/example/index.rst).

This is the main documentation page for the *package* (as opposed from the Python module, see below).
The purpose of this page is to document the Git repository itself, and anything that exists outside the normal codebase.
An example use of this package index page (or pages linked from it) is to document datasets in a Git LFS-based data package.

At a minimum, this page should be customized with a description of the package.
This copy can be shared with the description in the README.

### doc/{{cookiecutter.python_module}}/index.rst

Example: [doc/lsst.example/index.rst](example/doc/lsst.example/index.rst).

This is the main documentation page for the Python module provided by the package.
Most documentation will be linked through this page.
Packages that provide multiple Python modules (like `afw`) can have several of these directories, each named after the public module's namespace.

Separate documentation is forthcoming on how to format this page.

### doc/conf.py

Example: [doc/conf.py](example/doc/conf.py).

This `conf.py` file is only used for single-package documentation builds during development.
You shouldn't modify this file beyond the basic templated customization.
If you need to modify the Sphinx configuration, post a message in the #dm-docs Slack channel so it can be included in [documenteer](https://github.com/lsst-sqre/documenteer).

### doc/doxygen.conf.in

Example: [doc/doxygen.conf.in](example/doc/doxygen.conf.in).

This file configures the Doxygen build.
Per package Doxygen builds are necessary to generate the C++ API reference.

### doc/index.rst

Example: [doc/index.rst](example/doc/index.rst).

This file is the root page for single-package documentation builds.
It is not used at all for the published site (https://pipelines.lsst.io).
This page's `toctree` should link to the `index.rst` files at the root of both the package and Python module documentation directories.

### doc/manifest.yaml

Example: [doc/manifest.yaml](example/doc/manifest.yaml).

This YAML file is used by the Sphinx documentation build tool (included in the [documenteer](https://github.com/lsst-sqre/documenteer) package).
It defines what package and Python module documentation directories this package provides.
The Cookiecutter template should configure this file for you out-of-the box.

Separate documentation is forthcoming on how to use this file.

### doc/SConscript

Example: [doc/SConscript](example/doc/SConscript).

Scons (extended by sconsUtils) uses this `SConstruct` file for the Doxygen build.
You shouldn't need to modify this file.

### examples/SConscript

Example: [examples/SConscript](example/examples/SConscript).

Scons (extended by sconsUtils) uses this `SConstruct` file.
You shouldn't need to modify this file.

You can put example Python modules in this `examples` directory.
Keep in mind that these examples aren't tested by continuous integration and we may change our usage of the examples directory in the future.

### include/

This directory is for C++ header files.
*Only necessary for packages developed in C++.*

### lib/SConscript

Example: [lib/SConscript](example/lib/SConscript).

Scons (extended by sconsUtils) uses this `SConstruct` file.
You shouldn't need to modify this file.

### `python/lsst/__init__.py`

Example: [`python/lsst/__init__.py`](example/python/lsst/__init__.py).

This `__init__`.py file extends the `lsst` Python namespace for this package's Python modules.
You shouldn't modify this file.

Packages that provide a root Python namespace that is three or more layers deep need to include a copy of this `__init__.py` file at each intermediate namespace level.
For an example, see [`example_subpackage/python/lsst/example/__init__.py`](example_subpackage/python/lsst/example/__init__.py).

### `python/{{cookiecutter.python_namespace}}/__init__.py`

Example: [`python/lsst/example/__init__.py`](example/python/lsst/example/__init__.py).

This `__init__.py` file defines the root of the Python namespace provided by this package (and does not use `pkgutils` to extend the namespace further).

At a minimum, this `__init__.py` imports objects from the `version.py` module created by `sconsUtils` at build time.
It's also customary to import objects from other modules here to craft the public API that users import.

### src/

Add C++ source files to the `src/` directory.
The included `Starter.cc` shows how to create a namespace.
You should rename this file to suit your application.

*Only necessary for packages developed in C++.*

### tests/SConscript

Example: [tests/SConscript](example/tests/SConscript).

sconsUtils/scons use this `SConscript` file.
You shouldn't need to modify this file.

Place all unit test modules in the `tests` directory.
See the [Python Unit Testing](https://developer.lsst.io/python/testing.html) documentation in the Developer Guide for details.

### ups/{{cookiecutter.package_name}}.build

Example: [ups/example.build](example/ups/example.build).

This file is used by EUPS.
You shouldn't need to modify it.

### ups/{{cookiecutter.package_name}}.cfg

Example: [ups/example.cfg](example/ups/example.cfg).

EUPS uses this file to configure the build.
Packages that compile C++ may need to customize the dependencies listed here.

See documentation in sconsUtils for details.

### ups/{{cookiecutter.package_name}}.table

Example: [ups/example.table](example/ups/example.table).

EUPS uses this file to establish dependencies of this package to other EUPS-distributed package.
When you import an API from another Stack package, make sure it is listed in this table file.
