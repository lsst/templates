# LSST code templates

This repository provides standardized templates for LSST software projects.
Refer to these templates when creating new projects (such as stack packages) and when adding new files to existing repositories.
We're continuously updating these templates with our adopted standards and best practices.

Two classes of templates are available in separate directories:

1. `file_templates/`.
   **File templates** are either entire files or snippets you can add to files.
   Examples of templates are license statements, documentation pages, and test module boilerplate.
2. `project_templates/`.
   **Project templates** have multiple files and are intended to bootstrap new Git repositories.
   An example of a project is an EUPS stack package.
   Projects often inherit from standalone content in `templates/`.

**Contributors.** See the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidance on adding and maintaining the templates and projects in this repository.

## List of project templates

- [example_project](project_templates/example_project/)
- [stack_package](project_templates/stack_package/)

## List of file templates

- [stack_license_preamble_cpp](file_templates/stack_license_preamble_cpp)
- [stack_license_preamble_py](file_templates/stack_license_preamble_py)
- [stack_license_preamble_txt](file_templates/stack_license_preamble_txt)
