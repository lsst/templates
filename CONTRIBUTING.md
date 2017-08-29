# Contributing to templates

This page describes how to maintain and contribute to this templates repository.
You'll learn about the structure of templates and how to document them.

Broadly, use the regular [Data Management Development Workflow](https://developer.lsst.io/processes/workflow.html) when contributing to this repository.
Because of the broad impact of these templates, a [Request for Comments (RFC)](https://developer.lsst.io/processes/decision_process.html) may be appropriate.

## Making a file template

Each **file template** has its own sub-directory in the `file_templates` root directory.
The standard components of a file template directory are:

- `README.md` file.
- `template.jinja`.
  This file is a [Jinja2 template](http://jinja.pocoo.org/docs/2.9/templates/).
  If the template is for a named file, use that name with a final `jinja` extension. For example, `COPYRIGHT.jinja`.
- `example.ext`.
  This file is a realistic example of a rendered template.
  The filename should include the word `example` to show that is not the template itself.

The next sections describe these files in more detail.

### File template README file

The title of the README is the same as the file template's directory name.

Provide a summary sentence or paragraph below the title.

Create a section called `Template variables`.
Name each subsection in `Template variables` after a Jinja variable.
Describe the use and format of each variable in these subsections.

### File template Jinja2 template file

The template file itself has a `jinja` extension.
For more information about the Jinja2 templating system, see the [Jinja2 template designer documentation](http://jinja.pocoo.org/docs/2.9/templates/).

The template file is designed to work with [Cookiecutter](https://cookiecutter.readthedocs.io/en/latest/).
This means that all template variables must be attributes of a `cookiecutter` variable.
For example:

```jinja
Copyright {{ cookiecutter.copyright_year }} {{ cookiecutter.copyright_holder }}
```

### Template example file

You can optionally include an example file that shows what the template looks like when rendered with realistic values.
Ensure that the example is updated whenever the template itself is updated.

## Making a project template

Each project template is its own sub-directory in the `project_templates` root directory.
The standard components of a project template directory are:

- `README.md` file.
- `cookiecutter.json` file.
- `{{cookiecutter.project_name}}` directory.
- `example` directory.

The next sections describe these files and directories in more detail.

### Project template README file

The title for a project's `README.md` should match the project's directory name.

Below the title, include a summary paragraph that describes what kinds of projects this project template can create.

Include a section called `Template variables`.
Subsections should match keys in the `cookiecutter.json` file and document each variable.

Include a section called `Files`.
Each subsection should be the name of a file (in a project cookiecutter directory).
Here you can document each component of that file, and describe how developers should extend the file for their own project.

### Project template cookiecutter.json file

The `cookiecutter.json` file is used by [Cookiecutter](https://cookiecutter.readthedocs.io/en/latest/) to get input from a user and create a project.

The JSON file contains a single JSON object.
Keys are names of Jinja templates and values are default values.
For example:

```json
{
  "copyright_year": 2017,
  "copyright_holder": "Association of Universities for Research in Astronomy, Inc.",
  "project_name": "my_project"
}
```

Besides scalar default values, you can instead specify [choice variables](https://cookiecutter.readthedocs.io/en/latest/advanced/choice_variables.html) and [dictionary variables](https://cookiecutter.readthedocs.io/en/latest/advanced/dict_variables.html).

See the [Cookiecutter documentation](https://cookiecutter.readthedocs.io/en/latest/), and other project templates, for more information and examples.

### Project template cookiecutter directory

In a cookiecutter project template, both the paths of files and directories, and the files's content, are Jinja2 template variables.

The root directory of a cookiecutter template is also a Jinja2 template.
For example, if the  `cookiecutter.json` file has a field `project_name`, and the directory of the project should be that name, the root directory of the cookiecutter template is:

```jinja
{{cookiecutter.project_name}}
```

### Project template example directory

You can optionally include an example project.
Unless projects of this type have meaningful naming schemas, the name of this directory can be `example`.

You should create the `example` directory from cookiecutter command execution alone.
Whenever the cookiecutter template is updated, the example should also be updated and committed.
Ideally, example re-generation should be scripted (for example, with a `Makefile`), but we don't have a suggested pattern for this yet.

## FAQ

### Why Markdown and why README.md?

The templates repository is meant to be used at the code level, either as a local clone or on GitHub.
Markdown is GitHub's best-supported markup syntax, it makes sense to use it here rather than reStructuredText.
See the [GitHub Flavored Markdown documentation](https://help.github.com/articles/basic-writing-and-formatting-syntax/) for guidance on what you can do.

GitHub features `README.md` files in its interface.
By using `README.md` we're able to show documentation alongside directories in GitHub repositories.

### Why are file templates distinguished from projects templates?

**Project templates** help you bootstrap a new Git repository.
They only contain the essential boilerplate though.
You shouldn't need to sort out and delete extraneous template files from a newly-created project.

To make a Git repository useful, though, you'll need to add new files like Python modules, tests, or documentation.
**File templates** provide the form of these files (or parts of files).

In other words, you *start* a new Git repository with a Project template and continue developing it by drawing from file templates.

By separating files from projects we better document those file templates, and also use file templates across many different types projects.

### How do I keep a project consistent with a template?

It's inevitable that projects (and templates) will duplicate content from other templates.
For example, Python modules in a project will contain license boilerplate that originates in a template.
This duplication can cause some maintenance concerns.
Here are some strategies for dealing with duplicate content:

1. Symlink the template Jinja file into the project template.
   This works if the template is for a whole file, and that template is used by multiple projects.

2. Document the dependency so that projects are updated when an underlying template changes.
   This documentation should appear in the describes of individual files in the project's `README.md`.
   Link to the template by name so that the dependency is searchable.
   Maintainers and reviewers should check for template consistency.
