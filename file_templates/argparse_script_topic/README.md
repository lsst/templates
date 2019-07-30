# argparse_script_topic

**Documentation topic template for creating reference pages about an argparse-based Python script.**

This documentation topic template is intended to create reference pages for [argparse](https://docs.python.org/3/library/argparse.html)-based Python scripts that are packaged with LSST software.
It takes advantage of tooling to automatically extract documentation about the command-line interface from the code itself.
For scripts that **aren't** built with `argparse`, use the more generic [script_topic](../script_topic) template instead.

Script topic pages go in the `scripts/` subdirectory of the [module documentation directory](https://developer.lsst.io/stack/layout-of-doc-directory.html#module-documentation-directories) in the package that implements the task.
These script pages are referenced from the [module documentation homepage](https://developer.lsst.io/stack/module-homepage-topic-type.html).
The file itself is named after the executable script.
For example, a script called `plotSkyMap.py` is documented in a file called `plotSkyMap.py.rst`.

[More documentation is available in the DM Developer Guide.](https://developer.lsst.io/stack/argparse-script-topic-type.html)

## Template variables

### cookiecutter.module_name

The Python module containing a function (called `build_argparser` by default) that generates the script's `argparse.ArgumentParser` instance.
For example: `lsst.verify.bin.dispatchverify`.

### cookiecutter.script_name

The name of the command-line executable.
For example: `dispatch_verify.py`.

## Examples

### exampleScript.py.rst

[exampleScript.py.rst](exampleScript.py.rst) is an example of a script topic for a `argparse`-based script named `exampleScript.py` that is implemented in a module called `lsst.example.bin.examplescript`.

## Related templates

- [stack_package](../../project_templates/stack_package)
- [script_topic](../script_topic)
