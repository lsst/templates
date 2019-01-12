# stack_package

**LSST DM EUPS Stack package.**

This template generates an LSST Stack package, which is part of the `lsst` namespace in Python and C++, is managed by [EUPS](https://github.com/RobertLuptonTheGood/eups), and is built by [SCons](https://scons.org) (with LSST's [sconsUtils](https://github.com/lsst/sconsUtils)).
For more documentation about developing packages, see the [DM Stack](https://developer.lsst.io/#part-dm-stack) section of the Developer Guide.

## Template variables

### cookiecutter.package_name

EUPS package name.
This is the name of the repository and the directory.

### cookiecutter.stack_name

The name of the EUPS stack that this package is part of (if at all).
This variable determines the layout of the `doc/` directory and seed content for the README.
Options are:

- "LSST Science Pipelines" — documentation for the package is expected to be published at https://pipelines.lsst.io.
- "None" — the package is not part of an EUPS stack. In this case, the documentation is structured so that it can be deployed to its own site.

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

GitHub organization where the repository is located.
Supported Stack packages are always located in the `lsst` organization.

### cookiecutter.base_package

This is the default EUPS dependency.
Besides itself, this base package also implicitly provides common third-party dependencies.
The choices are:

- [base](https://github.com/lsst/base): used by the LSST Science Pipelines. This is the default.
- [sconsUtils](https://github.com/lsst/sconsUtils): used by Telescope & Site and other stacks that don't need all the features of `base`.

### cookiecutter.uses_cpp

If `true` (default), the package is configured to support C++ and pybind11 code.
If `false`, the generated package is Python-only.

### cookiecutter.has_tasks

If `true` (default), a "Task reference" section is added to the module homepage.
Packages that don't provide Tasks or Config classes can skip this section.

To learn more about these topic pages, see the [Task topic page](../../file_templates/task_topic) and [Config topic page](../../file_templates/config_topic).

### cookiecutter.uses_python

If `true` (default), the package is configured to support Python code.
When both `uses_cpp` and `uses_python` are `false`, the generated package is a *data-only package.*

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

### example_pythononly/

The [example_pythononly](example_pythononly) directory shows a Stack package that only includes Python code (and no C++ sources).
Such packages don't have `lib`, `include`, and `src` directories.
Some of the dependencies configured in the [`ups` directory](example_pythononly/ups) are also different.

### example_dataonly/

The [example_dataonly](example_pythononly) directory shows a Stack package that does not include any Python or C++ code.
This type of package might be used for datasets (see [afwdata](https://github.com/lsst/afwdata) and [verify_metrics](https://github.com/lsst/verify_metrics)).

### example_standalone/

The [example_standalone](example_standalone) directory shows a package that does not belong to an integrated stack by setting [cookiecutter.stack_name](#cookiecutterstack_name) to ``"None"``.
Principally, this means that its documentation is designed to be deployed alone, to its own site, rather than a site like https://pipelines.lsst.io.
This example also demonstrates setting [cookiecutter.base_package](#cookiecutterbase_package) to ``"sconsUtils"``.
This type of package is commonly used by LSST Telescope & Site.

## Files

### COPYRIGHT

Example: [COPYRIGHT](example/COPYRIGHT).

Record copyright claims in this file, one line per institution.
See the [copyright](../../file_templates/copyright) template and [Managing license and copyright in Stack packages](https://developer.lsst.io/stack/license-and-copyright.html).

### LICENSE

Example: [LICENSE](example/LICENSE).

The license for all DM Stack package is GPL v3.0 (see the [license_gplv3](../../file_templates/license_gplv3) template).
The license should not be modified.
See [Managing license and copyright in Stack packages](https://developer.lsst.io/stack/license-and-copyright.html).

### README.rst

Example: [README.rst](example/README.rst).

Beyond the templated structure, you'll need to customize this README with a short (one sentence) description of what the package is for.
(*Tip:* this sentence should also be used for the GitHub repo description).

We keep the README fairly minimal, providing just enough information to help a person browsing packages via GitHub.
Put the bulk of the documentation in the `doc/` directory.

### SConstruct

Example: [SConstruct](example/SConstruct).

Scons (extended by [sconsUtils](https://github.com/lsst/sconsUtils)) uses this `SConstruct` file.
The only customization is the package name argument for the `lsst.sconsUtils.scripts.BasicSConstruct` builder.

### setup.cfg

Example: [setup.cfg](example/setup.cfg).

Python utilities, like [pytest](https://pytest.readthedocs.io/en/latest/) and [flake8](http://flake8.pycqa.org/en/latest/), use `setup.cfg` for configuration.
This file is generally standardized across all packages and shouldn't be customized.

### bin.src/SConscript

Example: [bin.src/SConscript](example/bin.src/SConscript).

Scons (extended by sconsUtils) uses this `SConstruct` file.
You shouldn't need to modify this file.

The `bin.src/` directory is where you put Python scripts (including command-line task executables) that are installed for users.

### doc/{{cookiecutter.package_name}}/index.rst

Example: [doc/example/index.rst](example_dataonly/doc/example_dataonly/index.rst).

This is the **package homepage**.
Package homepages, and their package documentation directories, are only available for data-only packages.
Packages with Python code have **module documentation directories** instead (see below).

The purpose of this page is to document the Git repository itself.
An example use of this package index page (or pages linked from it) is to document datasets in a Git LFS-based data package.

At a minimum, this page should be customized with a description of the package.
This copy can be shared with the description in the README.

See the [Package homepage topic type](https://developer.lsst.io/stack/package-homepage-topic-type.html) for more information.

### doc/{{cookiecutter.python_module}}/index.rst

Example: [doc/lsst.example/index.rst](example/doc/lsst.example/index.rst).

This is the **module homepage.**
This is the main documentation page for the Python module provided by the package.
Most documentation is linked through this page.

Packages that provide multiple Python modules (like `afw`) can have several of these directories, each named after the module's public namespace.

See the [Module homepage topic type](https://developer.lsst.io/stack/module-homepage-topic-type.html) for more information.

### doc/conf.py

Example: [doc/conf.py](example/doc/conf.py).

This `conf.py` file is only used for single-package documentation builds during development.
You shouldn't modify this file beyond the basic templated customization.
If you need to modify the Sphinx configuration, post a message in the [#dm-docs](https://lsstc.slack.com/archives/dm-docs) Slack channel so it can be included in [documenteer](https://github.com/lsst-sqre/documenteer).

See [Layout of the doc/ directory](https://developer.lsst.io/stack/layout-of-doc-directory.html) for more information.

### doc/doxygen.conf.in

Example: [doc/doxygen.conf.in](example/doc/doxygen.conf.in).

This file configures the Doxygen build.
Per package Doxygen builds are necessary to generate the C++ API reference.

*Only necessary for packages developed in C++.*

See [Layout of the doc/ directory](https://developer.lsst.io/stack/layout-of-doc-directory.html) for more information.

### doc/index.rst

Example: [doc/index.rst](example/doc/index.rst).

This file is the root page for single-package documentation builds.
It is not used at all for the published site (https://pipelines.lsst.io).
This page's `toctree` should link to the `index.rst` files at the root of both the package and Python module documentation directories.

See [Layout of the doc/ directory](https://developer.lsst.io/stack/layout-of-doc-directory.html) for more information.

### doc/manifest.yaml

Example: [doc/manifest.yaml](example/doc/manifest.yaml).

This YAML file is used by the Sphinx documentation build tool (included in the [documenteer](https://github.com/lsst-sqre/documenteer) package).
It defines what package and Python module documentation directories this package provides.
The Cookiecutter template should configure this file for you out-of-the box.

See [Layout of the doc/ directory](https://developer.lsst.io/stack/layout-of-doc-directory.html) for more information.

### doc/SConscript

Example: [doc/SConscript](example/doc/SConscript).

Scons (extended by sconsUtils) uses this `SConstruct` file for the Doxygen build.
You shouldn't need to modify this file.

*Only necessary for packages developed in C++.*

### examples/SConscript

Example: [examples/SConscript](example/examples/SConscript).

Scons (extended by sconsUtils) uses this `SConstruct` file.
You shouldn't need to modify this file.

You can put example Python modules in this `examples` directory.
Keep in mind that these examples aren't tested by continuous integration and we may change our usage of the examples directory in the future.

### include/root.h

Example: [include/lsst/example.h](example/include/lsst/example.h)

This is the root C++ header file.
Typically you will only `#include` other header files from this root header.

Note: the name `root.h` is only used by the template source.
When the template is built, a post-generate hook moves this header into place, based on the package's namespace.

*Only necessary for packages developed in C++.*

### lib/SConscript

Example: [lib/SConscript](example/lib/SConscript).

Scons (extended by sconsUtils) uses this `SConstruct` file.
You shouldn't need to modify this file.

### `python/{{cookiecutter.python_namespace}}/__init__.py`

Example: [`python/lsst/example/__init__.py`](example/python/lsst/example/__init__.py).

This `__init__.py` file defines the root of the Python namespace provided by this package.

At a minimum, this `__init__.py` imports objects from the `version.py` module created by `sconsUtils` at build time.
It's also customary to import objects from other modules here to craft the public API that users import.

### src/

Example: [src/Starter.cc](example/src/Starter.cc).

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

### ups/{{cookiecutter.package_name}}.cfg

Example: [ups/example.cfg](example/ups/example.cfg).

EUPS uses this file to configure the build.
Packages that compile C++ may need to customize the dependencies listed here.

See documentation in sconsUtils for details.

### ups/{{cookiecutter.package_name}}.table

Example: [ups/example.table](example/ups/example.table).

EUPS uses this file to establish dependencies of this package to other EUPS-distributed package.
When you import an API from another Stack package, make sure it is listed in this table file.

By convention, a "base" package is responsible for implicitly including common-third party packages, like Python itself.
The [cookiecutter.base_package](#cookiecutterbase_package) variable defines this base package.
