# Change log

## 2020-01-06

- Add a "Pipeline tasks" section to the module homepage template.

[DM-22520](https://jira.lsstcorp.org/browse/DM-22520)

## 2019-11-07

Added support for the [lsst-sitcom](https://github.com/lsst-sitcom) GitHub organization.

## 2019-11-05

Updated the AURA copyright to "Association of Universities for Research in Astronomy, Inc. (AURA)."

## 2019-11-04

Added a new `uses_dds` Cookiecutter variable.
When enabled, this variable adds a block to the `tests/SConscript` file that adds the contents of the  `OSPL_URI`, `OPENSPLICE_LOC`, and `ADLINK_LICENSE` environment variables to the PATH of the SCons environment.
These are necessary for T&S packages that work with OpenSplice DDS (the base technology used by SAL).

Slack-based users can trigger this variable by selecting a "DDS Package" item from the flavor menu.

## 2019-10-10

Packages that don't use C++ are now one file simpler:

- No `ups/*.cfg` file for non-C++ packages.
- The `SConstruct` file for non-C++ packages includes the `noCfgFile=True` argument.

[DM-21718](https://jira.lsstcorp.org/browse/DM-21718)

## 2019-09-20

- Added support for the https://github.com/lsst/lsst-verification-and-validation GitHub organization.

[DM-21376](https://jira.lsstcorp.org/browse/DM-21376)

## 2019-07-30

- Added a "Script reference" section to link to script topic pages (see [script_topic](../../file_templates/script_topic) and [argparse_script_topic](../../file_templates/argparse_script_topic)).

[DM-20821](https://jira.lsstcorp.org/browse/DM-20821)

## 2019-01-15

- Added a new template variable, `cookiecutter.stack_name`.
  This identifies what "stack" the package is part of, if at all.
  The current default is "LSST Science Pipelines," whose packages have documentation published at https://pipelines.lsst.io.
  If `cookiecutter.stack_name` is set to "None" then the package is considered to stand alone.
  In that case, the `doc/` directory is rearranged to support a standalone documentation site for the package.

- Added an `example_standalone/` package that demonstrates `cookiecutter.stack_name=="None"` and `cookiecutter.base_package=="sconsUtils"`.
  This example should be close to a typical Telescope & Site package starting point.

- Fixed an issue with the `cookiecutter.base_package` variable (the `sconsUtils` option was misspelled as `setupUtils`).

[DM-17191](https://jira.lsstcorp.org/browse/DM-17191)

## 2019-01-11

- Eliminated intermediate `__init__.py` files.
  In Python 3, `__init__.py` files are no longer needed to establish a package.
  This also means that the `pkgutil.extend_path` method call is no longer needed.
  Nor is the lsstimport package from the "base" EUPS package.

  The template still keeps the `__init__.py` of the module itself; this file is still commonly used for establishing public namespaces so it's good to keep it in the template.

- Added a new cookiecutter variable, `cookiecutter.base_package`.
  This selects the default package.
  Science Pipelines packages should use `base` as the base package (the effective outcome of [RFC-52](https://jira.lsstcorp.org/browse/RFC-52)), while other stacks that don't need `base` can use `sconsUtils`.

- Removed the `utils` package as a default dependency, reversing the change from 2018-11-05.
  Developers should add the `utils` dependency if their code uses it (for example, in tests).

[DM-17155](https://jira.lsstcorp.org/browse/DM-17155)

## 2018-11-05

- Added `bin/` and `.coverage` to `.gitignore`.
- Added `base` as a default EUPS dependency.
  This prevents packages that have not other dependencies from having errors about getting `lsstimport`.
  Packages that add high-level dependencies can drop the explicit dependency on `base`.
- Also add `utils` as a default EUPS dependency since it is necessary for unit tests, in most cases.
- Marked W504 (line break after binary operator) as an ignored Flake8 rule.
  This rule was introduced by pycodestyle 2.4.0, but is not part of the [DM Python Style Guide](https://developer.lsst.io/python/style.html).
  See the post [Changes to baseline software versions](https://community.lsst.org/t/changes-to-baseline-software-versions/3366).

[DM-16437](https://jira.lsstcorp.org/browse/DM-16437)

## 2018-10-10

- New "Task reference" section in the module homepages.
  The `has_tasks` configuration controls whether the "Task reference" section is included or not.

[DM-15422](https://jira.lsstcorp.org/browse/DM-15422)

## 2018-10-05

- `doc/SConscript` and `doc/doxygen.conf.in` are no longer included in packages that don't use C++.
- `conf.py` does not attempt to import a package if it doesn't not use Python.
- The package homepage no longer refers to the (nonexistent) Python module.
- The E251 rule exception is no longer included in `setup.cfg` since it is also not adopted by the [Python style guide](https://developer.lsst.io/python/style.html#exceptions-to-pep-8).

([DM-15973](https://jira.lsstcorp.org/browse/DM-15973), [DM-16040](https://jira.lsstcorp.org/browse/DM-16040))

## 2018-07-13

- Deleted the `ups/*.build` file.
  It turns out that this file is not used by the build system.

- Added `pyList` argument to the `tests/Sconscript` file.
  This enables auto file detection.

- Updated the `setup.cfg` configuration file.
  This adds the N806 flake8 exception and the `[tool:pytest]` section.

- Updated the default `automodapi` usage in module documentation homepages.

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
