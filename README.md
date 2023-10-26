# Vera C. Rubin Observatory code templates

This repository provides standardized templates for Rubin software projects.
The best way to create new projects and files is through the `@sqrbot-jr` bot in the LSSTC Slack workspace ([see how](#creating-projects-and-files-through-slack)).
Alternatively, you can create projects locally using the `templatekit` command line app.

Refer to these templates when creating new projects (such as stack packages) and when adding new files to existing repositories.
We're continuously updating these templates with our adopted standards and best practices.

To contribute new templates, or to update existing ones, see the [contributing guide](CONTRIBUTING.md).

## Contents

- [Project templates](#project-templates)
- [File templates](#file-templates)
- [Creating projects and files through Slack](#creating-projects-and-files-through-slack)
- [Creating projects and files without Slack](#creating-projects-and-files-without-slack)
- [Contributions](#contributions)
- [Troubleshooting](#troubleshooting)

## Project templates

**Project templates** have multiple files and are intended to bootstrap new Git repositories.
Find these templates in the `project_templates/` directory:

- [fastapi_safir_app](project_templates/fastapi_safir_app/)
- [latex_lsstdoc](project_templates/latex_lsstdoc/)
- [nbreport](project_templates/nbreport/)
- [roundtable_aiohttp_bot](project_templates/roundtable_aiohttp_bot/)
- [sitcom_personal_notebooks](project_templates/sitcom_personal_notebooks/)
- [stack_package](project_templates/stack_package/)
- [square_pypi_package](project_templates/square_pypi_package/)
- [technote_aastex](project_templates/technote_aastex/)
- [technote_latex](project_templates/technote_latex/)
- [technote_rst](project_templates/technote_rst/)
- [technote_rst_early_adopter](project_templates/technote_rst_early_adopter/)
- [test_report](project_templates/test_report/)

## File templates

**File templates** are either entire files or snippets you can add to files.
Find these templates in the `file_templates` directory:

- [argparse_script_topic](file_templates/argparse_script_topic)
- [config_topic](file_templates/config_topic)
- [copyright](file_templates/copyright)
- [license_gplv3](file_templates/license_gplv3)
- [script_topic](file_templates/script_topic)
- [stack_license_preamble_cpp](file_templates/stack_license_preamble_cpp)
- [stack_license_preamble_py](file_templates/stack_license_preamble_py)
- [stack_license_preamble_txt](file_templates/stack_license_preamble_txt)
- [task_topic](file_templates/task_topic)

## Creating projects and files through Slack

Rubin staff are members of the LSSTC Slack workspace.
To create a file or project:

1. [Open a DM with sqrbot-jr](https://slack.com/app_redirect?app=AF2U6ADV3&team=T06D204F2)
2. Enter a command through the chat:

   - For file templates, enter:

     ```
     create file
     ```

     Fill out the fields in the window, and then copy the resulting text file that sqrbot-jr returns.

   - For project templates, enter:

     ```
     create project
     ```

     Fill out the fields in the window.
     For projects with complex set up, watch for a message thread with information about the Git repository that is created for you.

## Creating projects and files without Slack

You can create files and projects from these templates on you local machine, without using the `@sqrbot-jr` Slack app, by running [templatekit](https://templatekit.lsst.io).
**Note the caveat that the `@sqrbot-jr` app performs many administrative set-up tasks that are critically important when creating new documents. In almost all cases, using the `@sqrbot-jr` is recommended or required.**

First, clone this repository and install the `templatekit` app:

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
