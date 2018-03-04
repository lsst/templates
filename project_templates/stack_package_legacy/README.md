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
