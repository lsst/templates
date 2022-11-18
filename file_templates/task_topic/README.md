# task_topic

**Documentation topic template for `lsst.pipe.base.Task` classes.**

A task topic is the canonical reference for a given task.
Whether the task is used from the command line, triggered through the LSST Science Platform, or called from Python, the task topic page describes the task's algorithm, inputs, outputs, and configurations.
Tasks are also documented in the API reference (docstrings), but those docstrings should focus on pragmatic details needed by Python API users (such as parameters, return types, and exceptions).

Task topic pages go in the `tasks/` subdirectory of the module documentation directory in the package that implements the task.
The file itself is named after the full Python namespace of the task's class with a `.rst` extension.
For example: `lsst.pipe.tasks.processCcd.ProcessCcdTask.rst`.

## Template variables

### cookiecutter.task_class

The Task class's name.
For example: `ProcessCcdTask`.

### cookiecutter.task_module

The Python module containing the task class.
For example: `lsst.pipe.tasks.processCcd`.

## Examples

This file template has multiple examples that demonstrate different configurations.

### lsst.example.ExampleTask.rst

[lsst.example.ExampleTask.rst](lsst.example.ExampleTask.rst) is a minimal example of a task topic for a regular Task class.

## Related templates

- [stack_package](../../project_templates/stack_package)
- [config_topic](../config_topic)
