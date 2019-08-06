# script_topic

**Documentation topic template for creating reference pages about scripts.**

This documentation topic template is intended to work with any script and relies on manual documentation of a script's options and arguments.
If the script is built with [argparse](https://docs.python.org/3/library/argparse.html), use the [argparse_script_topic](../argparse_script_topic) template instead to take advantage of automatic documentation tooling.

Script topic pages go in the `scripts/` subdirectory of the [module documentation directory](https://developer.lsst.io/stack/layout-of-doc-directory.html#module-documentation-directories) in the package that implements the task.
These script pages are referenced from the [module documentation homepage](https://developer.lsst.io/stack/module-homepage-topic-type.html).
The file itself is named after the executable script.
For example, a script called `runPipeline.sh` is documented in a file called `runPipeline.sh.rst`.

[More documentation is available in the DM Developer Guide.](https://developer.lsst.io/stack/script-topic-type.html)

## Template variables

### cookiecutter.script_name

The name of the command-line executable.
For example: `runPipeline.sh`.

## Examples

### exampleScript.sh.rst

[exampleScript.sh.rst](exampleScript.sh.rst) is an example of a script topic for a shell script named `exampleScript.sh`.

## Related templates

- [stack_package](../../project_templates/stack_package)
- [argparse_script_topic](../argparse_script_topic)
