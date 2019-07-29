# technote_rst

**LSST technical note repository, based on reStructuredText and Sphinx.**

This template generates a new technical note (technote) repository based on Sphinx.
LSST technotes, in general, let you document technical designs, proposals, product overviews, results of prototyping experiments, and other types of documentation that doesn't fit in either the change-controlled document tree, or in user documentation.
See [Technotes for stand-alone technical documentation in the Developer Guide](https://developer.lsst.io/project-docs/technotes.html).

Keep in mind that technotes are single-page websites.
Specifically, don't use `toctree` to create a multi-page site.
Technotes are constrained to single pages so that they can be archived to DocuShare, and as a result the technote infrastructure is designed specifically to support a single-page site.

## Template variables

### cookiecutter.first_author

The name of the first author, formatted as `First Last`.

Once the technote repository is generated you can add additional authors to the `authors` list in `metadata.yaml`.

### cookiecutter.series

The identifier of the technote series.
Choose the series that fits the document's purpose or aligns with the organization creating the document:

- `DMTN` for Data Management technical notes. See [DMTN-000](https://dmtn-000.lsst.io).
- `ITTN` for LSST IT technical notes.
- `OPSTN` for LSST Operations technical notes.
- `PSTN` for Project Science Team technical notes.
- `SMTN` for Simulations Group technical notes. See [SMTN-000](https://smtn-000.lsst.io).
- `SITCOMTN` for Systems Integration, Testing, and Commissioning notes.
- `SQR` for SQuaRE technical notes. See [SQR-000](https://sqr-000.lsst.io).
- `TESTN` for testing the technical system. *These notes may be purged at any time.*

### cookiecutter.serial_number

The serial number. Use three digits padded with zeros.
If you are creating a technical note manually with this template, see the [Create a technote](https://developer.lsst.io/project-docs/technotes.html#create-a-technote) instructions for how to determine the serial number.

### cookiecutter.title

The title of the technote.

### cookiecutter.repo_name

The name of the GitHub repository
Cookiecutter will automatically format this for you based on the [series](#cookiecutter_series) and [serial_number](#cookiecutter_serial_number) information.

### cookiecutter.github_org

The GitHub organization where this technote resides.
Choose a GitHub organization that matches the [series](#cookiecutter_series):

- `lsst-dm` for the DM DMTN series.
- `LSST-IT` for the ITTN series.
- `lsst-ops` for the OPSTN series.
- `lsst-sims` for the Simulations Group's SMTN series.
- `lsst-sitcom` for the SITCOMTN series.
- `lsst-sqre` for the SQuaRE SQR series.
- `lsst-sqre-testing` for the TESTN series.

### cookiecutter.github_namespace

Allow Cookiecutter to populate this variable.

### cookiecutter.docushare_url

This is the technote's URL in LSST's DocuShare archive.
Leave empty if the technote hasn't been registered with DocuShare yet (which is currently true in most cases).

### cookiecutter.url

The technote's public URL on LSST the Docs.
Allow cookiecutter to populate this variable.

### cookiecutter.description

A short description of the technote's content and purpose.
This description is used in the repository's README and may be used in the abstract in the document itself.

### cookiecutter.copyright_year

The year of the initial copyright claim.
Cookiecutter will automatically populate the current year.

### cookiecutter.copyright_holder

The initial copyright holder.
See [Copyrights for LSST DM work and the COPYRIGHT file](https://developer.lsst.io/legal/copyright-overview.html) for more information.

## Examples

### testn-000/

The [testn-000](testn-000) directory is an example of a technote generated from the template defaults.

## Files

### lsstbib/

Example: [lsstbib](testn-000/lsstbib).

This directory contains local copies of LSST BibTeX files that are maintained in [lsst-texmf](https://github.com/lsst/lsst-texmf).
See the README of the generated technote repository for information on how to update these BibTeX files during the lifetime of a technote.

### .travis.yml

Example: [.travis.yml](testn-000/.travis.yml).

The [Travis CI](https://travis-ci.org) configuration file.
CI is triggered whenever a technote is pushed to GitHub, and is responsible for deploying the technote to GitHub.

### conf.py

Example: [conf.py](testn-000/conf.py).

The Sphinx configuration file.
The basic Sphinx configuration comes our Documenteer package, but you can append the [typical configuration variables](http://www.sphinx-doc.org/en/master/usage/configuration.html) to the end of that ``conf.py`` to customize the Sphinx build.

### COPYRIGHT

Example: [COPYRIGHT](testn-000/COPYRIGHT).

Record copyright claims in this file, one line per institution.
See the [copyright](../copyright) template and [Copyrights for LSST DM work and the COPYRIGHT file](https://developer.lsst.io/legal/copyright-overview.html).

### index.py

Example: [index.rst](testn-000/index.rst).

This is the file that your technote's content should go into.
There are a few caveats:

- Don't add the top-level document title.
  This is added for you.
  Add section headers with `=` underscore symbols.
  See the [headers documentation in the DM ReStructuredText Style Guide](https://developer.lsst.io/restructuredtext/style.html#sections).

- Don't add `toctree` to incorporate additional pages.
  You can still spread your content across multiple source files by using the [include](http://docutils.sourceforge.net/docs/ref/rst/directives.html#include) directive.

### LICENSE

Example: [LICENSE](testn-000/LICENSE).

Generally speaking, LSST documentation is licensed under CC-BY 4.0.
See [Licensing LSST DM source code and content](https://developer.lsst.io/legal/licensing-overview.html) in the Developer Guide for more information.

### local.bib

Example: [local.bib](testn-000/local.bib).

Add BibTeX citations to this file that aren't already available in [lsst-texmf](https://lsst-texmf.lsst.io) (the [lsstbib/](#testn-000/local_bib).
See the [Updating bibliographies](https://lsst-texmf.lsst.io/developer.html#updating-bibliographies) documentation in lsst-texmf for how to migrate local bibliography data upstream into [lsst-texmf](https://lsst-texmf.lsst.io).

### Makefile

Example: [Makefile](testn-000/Makefile).

The Makefile runs the local Sphinx build for authors on their local machines, and is also used by Travis CI (see [.travis.yml](testn-000/.travis.yml)).

See ``make help`` for available targets.

### metadata.yaml

Example: [metadata.yaml](testn-000/metadata.yaml).

This metadata file is used by [Documenteer](https://documenteer.lsst.io), which runs the Sphinx build itself.
Editing the values in this file updates the title and author list in the built and published technote.
See the comments in that file for further information.

### README.rst

Example: [README.rst](testn-000/README.rst).

The README advertises the technote to GitHub visitors and provides instructions for authors.

### requirements.txt

Example: [requirements.txt](testn-000/requirements.txt).

The `requirements.txt` file defines build dependencies for both authors, on your local system, and for the CI system.
If your technote requires additional Python Packages and Sphinx extensions to build, add those requirements to this file.
Generally speaking, the [documenteer](https://documenteer.lsst.io) dependencies only needs to be updated if the build breaks or you need new features from [Documenteer](https://documenteer.lsst.io).
