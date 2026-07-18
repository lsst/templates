[![Website](https://img.shields.io/badge/testn--000-lsst.io-brightgreen.svg)](https://testn-000.lsst.io)
[![CI](https://github.com/lsst/testn-000/actions/workflows/ci.yaml/badge.svg)](https://github.com/lsst/testn-000/actions/workflows/ci.yaml)

# Document Title

## TESTN-000

A short description of this document

**Links:**

- Publication URL: https://testn-000.lsst.io
- GitHub repository: https://github.com/lsst/testn-000
- Build system: https://github.com/lsst/testn-000/actions/


## Build this technical note

You can clone this repository and build the technote locally if your system has [Typst](https://typst.app) 0.15 or later and Python 3.11 or later:

```sh
git clone https://github.com/lsst/testn-000
cd testn-000
make init
make pdf
```

The first `make pdf` downloads the `rubin-technote` Typst template and the shared Rubin bibliographies; set `LSST_TEXMF_DIR` to a local [lsst-texmf](https://github.com/lsst/lsst-texmf) checkout to copy the template from there instead.
Repeat the `make pdf` command to rebuild the technote after making changes.
If you need to delete any intermediate files for a clean build, run `make clean`.

The built technote is located at `TESTN-000.pdf`.

## Publishing changes to the web

This technote is published to https://testn-000.lsst.io whenever you push changes to the `main` branch on GitHub.
When you push changes to another branch, a preview of the technote is published to https://testn-000.lsst.io/v.

## Editing this technical note

The main content of this technote is in `index.typ` (a [Typst](https://typst.app/docs) file).
Metadata, authors, and the document status are in the `technote.toml` file; run `make add-author` to add an author from the central author database and `make sync-authors` to refresh existing author entries.
Run `make sync-bibs` to refresh the shared Rubin bibliographies in `lsstbib/`.
