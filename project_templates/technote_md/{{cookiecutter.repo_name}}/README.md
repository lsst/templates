[![Website](https://img.shields.io/badge/{{ cookiecutter.repo_name|replace("-", "--") }}-lsst.io-brightgreen.svg)]({{ cookiecutter.url }})
[![CI](https://github.com/{{ cookiecutter.github_namespace }}/actions/workflows/ci.yaml/badge.svg)](https://github.com/{{ cookiecutter.github_namespace }}/actions/workflows/ci.yaml)

# {{ cookiecutter.title }}

## {{ cookiecutter.series }}-{{ cookiecutter.serial_number }}

{{ cookiecutter.description }}

**Links:**

- Publication URL: {{ cookiecutter.url }}
- Alternative editions: {{ cookiecutter.url }}/v
- GitHub repository: https://github.com/{{ cookiecutter.github_namespace }}
- Build system: https://github.com/{{ cookiecutter.github_namespace }}/actions/
{% if cookiecutter.docushare_url|length > 0 %}
- LSST Docushare: {{ cookiecutter.docushare_url }}.
{% endif %}

## Build this technical note

You can clone this repository and build the technote locally if your system has Python 3.11 or later:

```sh
git clone https://github.com/{{ cookiecutter.github_namespace }}
cd {{ cookiecutter.series.lower() }}-{{ cookiecutter.serial_number }}
make init
make html
```

Repeat the `make html` command to rebuild the technote after making changes.
If you need to delete any intermediate files for a clean build, run `make clean`.

The built technote is located at `_build/html/index.html`.

## Publishing changes to the web

This technote is published to {{ cookiecutter.url }} whenever you push changes to the `main` branch on GitHub.
When you push changes to a another branch, a preview of the technote is published to {{ cookiecutter.url }}/v.

## Editing this technical note

The main content of this technote is in `index.md` (a Markdown file parsed as [CommonMark/MyST](https://myst-parser.readthedocs.io/en/latest/index.html)).
Metadata and configuration is in the `technote.toml` file.
For guidance on creating content and information about specifying metadata and configuration, see the Documenteer documentation: https://documenteer.lsst.io/technotes.
