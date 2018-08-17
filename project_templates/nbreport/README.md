# nbreport

**Notebook-based report**

Notebook-based reports are templated Jupyter notebooks that can be computed and published with LSST's nbreport service.
Use notebook-based reports for Jupyter notebooks that are continuously rerun against new datasets.

See the [nbreport documentation](https://nbreport.lsst.io) for more information about notebook-based reports.

## Template variables

### cookiecutter.handle

The document handle adopted by this report.
Typically at LSST handles take the form of ``XYZ-N``.

### cookiecutter.title

This is the title of the report.
It should succinctly describe the purpose and content of the report.

### cookiecutter.git_repo

This is the URL of the GitHub repository that hosts the report.

### cookiecutter.git_repo_subdir

If the report **is not** hosted at the root of the Git repository, set the path of the report's base directory relative to the root of the Git repository with this variable.
Otherwise, leave as an empty string.

## Examples

### EXAMPLE-000/

The [EXAMPLE-000](EXAMPLE-000) directory is a notebook-based report built with the default configurations in `cookiecutter.json`.

## Files

### cookiecutter.json

Example: [cookiecutter.json](EXAMPLE-000/cookiecutter.json).

Add template variables to the mapping in the `cookiecutter.json` file.
The keys are parameter names and values are _defaults_.

For example:

```json
{
  "param1": "123",
  "param2": "abc"
}
```

In the notebook file you can use these template variables as `{{cookiecutter.param1}}` and `{{cookiecutter.param2}}`.
The default value of ``param1`` is `123`, and the default value of `param2` is `ABC`.

### nbreport.yaml

Example: [nbreport.yaml](EXAMPLE-000/nbreport.yaml).

This file provides configuration metadata for [nbreport](https://nbreport.lsst.io).
You shouldn't need to modify it yourself.

### README.md

Example: [README.md](EXAMPLE-000/README.md).

This template seeds a README for your report repository.
Feel free to expand on it as necessary.

### {{cookiecutter.handle}}.ipynb

Example: [EXAMPLE-000.ipynb](EXAMPLE-000/EXAMPLE-000.ipynb).

This is the templated Jupyter notebook that generates the report itself.
This template seeds the title cell; it's up to you to add more notebook cells with prose and code.

Keep these guidelines in mind when developing the report template:

- Don't commit the output. Always clear outputs before committing.
- Use Jinja syntax in code and Markdown cells to insert the values of variables.
- Use the [nbreport test](https://nbreport.lsst.io/cli-reference.html#nbreport-test) command to test your notebook template.
