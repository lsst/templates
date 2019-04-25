# LSST code templates

This repository provides standardized templates for LSST software projects.
Use the `templatekit` command line app to start a new file or project from these templates.

Refer to these templates when creating new projects (such as stack packages) and when adding new files to existing repositories.
We're continuously updating these templates with our adopted standards and best practices.

## Contents

- [Getting started](#getting-started)
- [List of project templates](#list-of-project-templates)
- [List of file templates](#list-of-file-templates)
- [Contributions](#contributions)
- [Troubleshooting](#troubleshooting)

## Getting started

Clone this repository and install the `templatekit` app:

```bash
git clone https://github.com/lsst/templates
cd templates
pip install -r requirements.txt
```

List the templates in this repository:

```bash
templatekit list
```

Try filling in a file/snippet template:

```bash
templatekit make stack_license_preamble_py -c
```

Then answer the prompts to fill in the license preamble.
Behind the scenes, `templatekit` uses [Cookiecutter](https://cookiecutter.readthedocs.io).
If you have any questions about what the variables are, check out the [template's README](file_templates/stack_license_preamble_py).

With the `-c` (`--copy`) option, `templatekit` copies the rendered text to the clipboard.
You can write the text to a file with the `-o` (`--output`) option.

You can create project templates the same way.
For example, create a new stack package:

```bash
templatekit make stack_package -o ../
```

The `-o` option makes sure the stack package is created next to the `templates/` repo, not inside it.

You can get more information about `templatekit` and its commands by running:

```bash
templatekit -h
```

See [Troubleshooting](#troubleshooting) for solutions to common issues.

## List of project templates

**Project templates** have multiple files and are intended to bootstrap new Git repositories.
Find these templates in the `project_templates/` directory:

- [example_project](project_templates/example_project/)
- [nbreport](project_templates/nbreport/)
- [stack_package](project_templates/stack_package/)
- [technote_latex](project_templates/technote_latex/)
- [technote_rst](project_templates/technote_rst/)

## List of file templates

**File templates** are either entire files or snippets you can add to files.
Find these templates in the `file_templates` directory:

- [config_topic](file_templates/config_topic)
- [copyright](file_templates/copyright)
- [license_gplv3](file_templates/license_gplv3)
- [stack_license_preamble_cpp](file_templates/stack_license_preamble_cpp)
- [stack_license_preamble_py](file_templates/stack_license_preamble_py)
- [stack_license_preamble_txt](file_templates/stack_license_preamble_txt)
- [task_topic](file_templates/task_topic)

## Contributions

See the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidance on adding and maintaining templates in this repository.

## Troubleshooting

### ASCII shell encoding

Depending on how your shell is set up, you may get this error when running `templatekit`:

> RuntimeError: Click will abort further execution because Python 3 was configured to use ASCII as encoding for the environment.  Either run this under Python 2 or consult http://click.pocoo.org/python3/ for mitigation steps.

To solve this, you need to set your shell's *locale* to use UTF-8.
For example, type these lines into your shell and add them to a start-up file such as ``.bashrc``:

```bash
export LC_ALL=en_US.utf-8
export LANG=en_US.utf-8
```

After the locale is set, re-try the `templatekit` command.

Keep in mind that different platforms have different locales.
To find available UTF-8 locales on your platform, run:

```bash
locale -a
```
