# technote_typst

**Rubin technical note repository, based on Typst.**

This template generates a new technical note (technote) repository that is written in [Typst](https://typst.app) and published as a PDF, in the style of Rubin's LaTeX technotes.
Rubin technotes, in general, let you document technical designs, proposals, product overviews, results of prototyping experiments, and other types of documentation that doesn't fit in either the change-controlled document tree, or in user documentation.
See [Technotes for stand-alone technical documentation in the Developer Guide](https://developer.lsst.io/project-docs/technotes.html).

The document metadata lives in `technote.toml`, using the same schema as Markdown and reStructuredText technotes, so `documenteer technote add-author` and `sync-authors` manage the author list from the central author database.
The Rubin document template is consumed as the `rubin-technote` Typst package, which the Makefile fetches from [lsst-texmf](https://github.com/lsst/lsst-texmf) as a vendored package, and the shared Rubin bibliographies are downloaded by a `sync-bibs` make target.

## Template variables

### cookiecutter.title

The title of the technote.

### cookiecutter.description

A short description of the technote's content and purpose, used as the initial abstract.

### cookiecutter.series

The identifier of the technote series.

### cookiecutter.serial_number

The serial number, assigned by the Slack bot or the next available number in the series.

### cookiecutter.author_id

The author's ID in lsst-texmf's [authordb.yaml](https://github.com/lsst/lsst-texmf/blob/main/etc/authordb.yaml) file.

### cookiecutter.first_author_given, first_author_family, first_author_orcid, first_author_affil_name, first_author_affil_internal_id, first_author_affil_address

The first author's name, ORCID iD, and affiliation, written into `technote.toml`.

### cookiecutter.github_org

The GitHub organization where the technote resides.

### cookiecutter.copyright_year, copyright_holder

The copyright statement written into the COPYRIGHT file.
