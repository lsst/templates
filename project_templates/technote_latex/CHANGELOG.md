# Change log

## 2020-12-10

- The RTN technote series is now hosted in the "lsst" GitHub organization.

## 2020-06-04

- Switch to GitHub Actions for continuous integration and deployment, replacing Travis CI.

## 2020-05-25

- Add support for the RTN technote series for operations.

## 2019-11-05

Updated the AURA copyright to "Association of Universities for Research in Astronomy, Inc. (AURA)."

## 2019-08-26

- Add support for the Telescope & Site technote series (TSTN).

## 2019-08-09

- Adopt latexmk for building the PDF and for doing most of the cleanup.
  This improves the initial experience of starting a new latex document where running bibtex would fail because the document didn't have any citations yet.

## 2019-07-29

- Add support for the ITTN technote series for LSST IT.

## 2019-04-29

This LaTeX document template is roughly based on the [`document` template](https://github.com/lsst/lsst-texmf/tree/master/templates/document) in the lsst-texmf repo, however it's customized in several ways to become a dedicated technote template:

- The lsstdoc class invocation is simplified to _not_ add a draft watermark and to always use author-year citations.
  Change-controlled documents use numbered citations and initially use the lsstdraft watermark too.
- The Makefile assumes that lsst-texmf is included as a Git submodule.
- The meta.tex method of adding Git-based metadata to the document is now the standard, pioneered by John Swinbank's documents.
- The README is now substantially more useful, with instructions on how to deal with the Git submodule, build the document, and manage acronyms.
- Adds a `templatekit.yaml` file to configure Slack-based usage.
