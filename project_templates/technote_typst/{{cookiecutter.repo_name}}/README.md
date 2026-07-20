[![Website](https://img.shields.io/badge/{{ cookiecutter.repo_name|replace("-", "--") }}-lsst.io-brightgreen.svg)]({{ cookiecutter.url }})
[![CI](https://github.com/{{ cookiecutter.github_namespace }}/actions/workflows/ci.yaml/badge.svg)](https://github.com/{{ cookiecutter.github_namespace }}/actions/workflows/ci.yaml)

# {{ cookiecutter.title }}

## {{ cookiecutter.series }}-{{ cookiecutter.serial_number }}

{{ cookiecutter.description }}

**Links:**

- Publication URL: {{ cookiecutter.url }}
- GitHub repository: https://github.com/{{ cookiecutter.github_namespace }}
- Build system: https://github.com/{{ cookiecutter.github_namespace }}/actions/
{% if cookiecutter.docushare_url|length > 0 %}
- LSST Docushare: {{ cookiecutter.docushare_url }}.
{% endif %}

## Build this technical note

You can clone this repository and build the technote locally if your system has [Typst](https://typst.app) 0.15 or later and Python 3.11 or later:

```sh
git clone https://github.com/{{ cookiecutter.github_namespace }}
cd {{ cookiecutter.series.lower() }}-{{ cookiecutter.serial_number }}
make init
make pdf
```

The first `make pdf` downloads the `rubin-technote` Typst template and the shared Rubin bibliographies; set `LSST_TEXMF_DIR` to a local [lsst-texmf](https://github.com/lsst/lsst-texmf) checkout to copy the template from there instead.
Repeat the `make pdf` command to rebuild the technote after making changes.
If you need to delete any intermediate files for a clean build, run `make clean`.

The built technote is located at `{{ cookiecutter.series }}-{{ cookiecutter.serial_number }}.pdf`.

## Publishing changes to the web

This technote is published to {{ cookiecutter.url }} whenever you push changes to the `main` branch on GitHub.
When you push changes to another branch, a preview of the technote is published to {{ cookiecutter.url }}/v.

## Editing this technical note

The main content of this technote is in `index.typ` (a [Typst](https://typst.app/docs) file).
Metadata, authors, and the document status are in the `technote.toml` file; run `make add-author` to add an author from the central author database and `make sync-authors` to refresh existing author entries.
Run `make sync-bibs` to refresh the shared Rubin bibliographies in `lsstbib/`.
