# {{cookiecutter.pypi_name}}

{{cookiecutter.description}}
Learn more at https://{{cookiecutter.pypi_name}}.lsst.io

Install from PyPI:

```sh
pip install {{cookiecutter.pypi_name}}
```

{{cookiecutter.pypi_name}} is developed by Rubin Observatory at https://github.com/{{cookiecutter.github_org}}/{{cookiecutter.pypi_name}}.

## Features

<!-- A bullet list with things that this package does -->

## Developing {{cookiecutter.pypi_name}}

The best way to start contributing to {{cookiecutter.pypi_name}} is by cloning this repository, creating a virtual environment, and running the `make init` command:

```sh
git clone https://github.com/{{cookiecutter.github_org}}/{{cookiecutter.pypi_name}}.git
cd {{cookiecutter.pypi_name}}
make init
```

You can run tests and build documentation with [tox](https://tox.wiki/en/latest/):

```sh
tox
```

To learn more about the individual environments:

```sh
tox -av
```

[See the docs for more information.](https://{{cookiecutter.pypi_name}}.lsst.io/dev/development.html)
