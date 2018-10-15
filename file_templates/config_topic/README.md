# config_topic

**Documentation topic template for `lsst.pex.config.Config` classes.**

A config topic is the canonical reference for a given standalone Config class.
Most Config classes are directly tied to a Task class and are documented in the [task_topic](../task_topic) type.
Some Config classes stand alone, such as as `lsst.pipe.tasks.colorterms.Colorterm` and those are the types of Config classes that need to be documented with a config topic.

Config topic pages go in the `configs/` subdirectory of the module documentation directory in the package that implements the config.
The file itself is named after the full Python namespace of the config's class with a `.rst` extension.
For example: `lsst.pipe.tasks.colorterms.Colorterm.rst`.

## Template variables

### cookiecutter.config_class

The Config class's name.
For example: `Colorterm`.

### cookiecutter.config_module

The Python module containing the Config class.
For example: `lsst.pipe.tasks.colorterms`.

## Examples

### lsst.example.ExampleConfig.rst

[lsst.example.ExampleConfig.rst](lsst.example.ExampleConfig.rst) is a minimal example of a config topic for a standalone Config class.

## Related templates

- [stack_package](../../project_templates/stack_package)
- [task_topic](../task_topic)
