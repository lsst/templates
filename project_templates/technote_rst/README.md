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

- ``SQR`` for SQuaRE technical notes. See [SQR-000](https://sqr-000.lsst.io).
- ``DMTN`` for Data Management technical notes. See [DMTN-000](https://dmtn-000.lsst.io).
- ``SMTN`` for Simulations Group technical notes. See [SMTN-000](https://smtn-000.lsst.io).
- ``SITCOMTN`` for Systems Integration, Testing, and Commissioning notes.
- ``TESTN`` for testing the technical system. *These notes may be purged at any time.*

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

- ``lsst-dm`` for the DM DMTN series
- ``lsst-sqre`` for the SQuaRE SQR series
- ``lsst-sims`` for the Simulations Group's SMTN series
- ``lsst-sitcom`` for the SITCOMTN series.
- ``lsst-sqre-testing`` for the TESTTN series.

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
