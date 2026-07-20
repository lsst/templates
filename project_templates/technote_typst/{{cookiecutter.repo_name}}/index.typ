#import "@preview/rubin-technote:0.1.0": citeds, citedsp, lsstdoc, note, technote-args, warning

// Shared Rubin bibliographies are materialized into lsstbib/ by
// `make sync-bibs` (run automatically by `make pdf`).
#let bibliographies = (
  read("local.bib", encoding: none),
  read("lsstbib/lsst.bib", encoding: none),
  read("lsstbib/lsst-dm.bib", encoding: none),
  read("lsstbib/refs.bib", encoding: none),
  read("lsstbib/refs_ads.bib", encoding: none),
  read("lsstbib/books.bib", encoding: none),
)

// Metadata, authors, and document status come from technote.toml, which
// `make add-author` and `make sync-authors` keep up to date.
#show: lsstdoc.with(
  ..technote-args(toml("technote.toml")),
  title: "{{ cookiecutter.title }}",
  abstract: [
    {{ cookiecutter.description }}
  ],
  bibliography: bibliographies,
)

= Introduction

Add content here.
Other Rubin documents can be referenced by their handles, for example
the science requirements #citeds("LPM-17"), and ordinary citations use
Typst's `@` syntax against the shared bibliographies or `local.bib`.
