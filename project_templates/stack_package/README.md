# Stack package template

The directory structure and files in this package are intended to serve as a template for other LSST packages.
This package should never be installed or built.

## Using the example project

All occurrences of `TMPL` should be replaced by the name of the package, either in `a_b` form (for example, `pex_exceptions`) or `a/b` form (for example, `pex/exceptions`) as appropriate.
These include the following:

- `SConstruct` contents
- `include/lsst/TMPL` directory
- `python/lsst/TMPL` directory
- `python/lsst/TMPL/SConscript` contents
- `python/lsst/TMPL/TMPLLib.i` filename and contents
- `ups/TMPL.table filename` and contents
- `ups/TMPL.cfg` filename and contents

The following files need to be modified with information about packages that this one depends on (its dependencies):

- `python/lsst/TMPL/TMPLLib.i`
- `ups/TMPL.table`
- `ups/TMPL.cfg`

For more information on the SCons files, please see the `sconsUtils` documentation.

## File documentation

This section describes the roles of individual files in the project template, and how they should be developed.
Refer to sections here as you populate and develop individual files in the template.

### doc/index.rst

The root `index.rst` file's purpose is to provide links to the *package* and *Python module* documentation sub-directories for single package documentation builds.
It is not used for integrated builds with [pipelines_lsst_io](https://github.com/lsst/pipelines_lsst_io).

The title should include the EUPS package name, and content should be a `toctree` pointing to the `index.rst` files of each module and package documentation subdirectory (as defined in the `doc/manifest.yaml` file.

### doc/manifest.yaml

The `doc/manifest.yaml` file defines what documentation sub-directories exist in `doc/` and are used to link documentation content into the parent [pipelines_lsst_io](https://github.com/lsst/pipelines_lsst_io) documentation repository at build time.
The fields of the YAML file are:

- `modules`: a **list** Python module names that the EUPS package implements.
  For example, `'lsst.afw.table'`.
  Each of these list items corresponds to the name of a directory in `doc/`.
  For example, a `doc/lsst.afw.table`.
  This field is a list because a single EUPS package can host multiple distinct Python modules.

  These subdirectories are for *python module* documentation.
  See `doc/lsst.TMPL/index.rst` for the seed content of that directory.

- `packages`: a single string that is the EUPS package name itself.
  This string corresponds to the name of a directory in `doc/`.
  For example, `'afw'`.

  This subdirectory is for *package* documentation.
  See `doc/TMPL/index.rst` for the seed content for that directory.

- `statics`: This is an optional **list** of Sphinx-standard static content directory for that package.
  Usually this list has a single item that is formatted as `'_static/<package name>'`.
  It is required that the first directory be `_static` and the subdirectory is typically the EUPS package name.
  These list items correspond to directories within the repository's `doc` directory.

  These directories are linked into the `_static` directory of the parent [pipelines_lsst_io](https://github.com/lsst/pipelines_lsst_io) repository at build time.

  The purpose of the static directory is to host static content that simply copied into the built site, such as PDF downloads.

For more information about how this file is used by the documentation build process, see [Documenteer](https://github.com/lsst/documenteer) and the `build-stack-docs` command-line program in particular.

### doc/lsst.TMPL/index.rst

This is the sub-site homepage for the Python module documentation (see `modules` field in `doc/manifest.yaml`).

#### Title

The title is labeled by the full Python module namespace.
For example,

```rst
.. _lsst.TMPL:
```

The title itself is the Python module name:

```rst
#########
lsst.TMPL
#########
```

#### Summary

Directly below the title write a paragraph (likely a few sentences) that describes what the module does.
This is your opportunity to grab the attention of someone quickly browsing documentation trying to find relevant APIs.
If the module provides key classes, you can mention those.
If the module is part of a framework, you could link to that framework page.
Also mention and link to closely related, or easily confused, Python modules.

#### User guide subsections

After the summary, but above the *Python API reference* section, you can include one or more subsections with `toctrees` to user guide topics.
User guide topics can take the form of how-tos (practical task-focused documentation), discussions of concepts, or tutorials.

Organize the topics by audience, with different subsections for each.
Topics intended for end-users should appear in the first sections, while those for internal developers or that cover more advanced concepts should appear later.
For example, in `lsst.pipe.base` one of the first user guide sections is called "Using command-line tasks."
A later section is called "Developing command-line tasks."

Avoid putting content in the module `index.rst` page.
Instead, focus on organizing `toctrees` to other topic pages in the python module documentation subdirectory.

#### Python API reference

The Python API reference section is populated with `automodapi` directives that do the work on generating API reference tables and sub-pages .

For example:

```rst
Python API reference
====================

.. automodapi:: lsst.TMPL
```

### doc/TMPL/index.rst

This is the sub-site homepage for the EUPS package documentation (see `modules` field in `doc/manifest.yaml`).
This documentation describes the Git repository itself and can cover data repositories, ad hoc scripts, or internal development information.
Any information associated with a Python or C++ API appears in the Python module documentation directory instead.

#### Title

The title is labeled by the EUPS package name, with a `'-package'` suffix.

The title itself is named after the EUPS package.

#### Summary

The summary paragraph should describe what the package is for.

#### Project info section

In this section, update the path to the GitHub repository.
Also update the link to the relevant JIRA component.

#### Modules

In this section, link to the homepages (`index.rst`) of Python module documentation.
Use the `ref` role to make these links so that they work in both single-package documentation builds and integrated builds with [pipelines_lsst_io](https://github.com/lsst/pipelines_lsst_io).

## Issues

- `doc`
  - `doxygen.conf` needs work
- `python`
  - `__init__.py` in both python/lsst/A and python/lsst/A/B?
  - `SConscript`
  - `TMPLLib.i`
- `tests`
  - `SConscript`
  - `boost::test` examples
  - Python unittest examples
