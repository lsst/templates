# technote_latex

**LSST technical note repository, formatted as LaTeX (lsstdoc class).**

This template generates a new paper repository based on aastex.
This uses the bib files from the lsst-texmf setip.
See [Technotes for stand-alone technical documentation in the Developer Guide](https://developer.lsst.io/project-docs/technotes.html).

## Template variables

### cookiecutter.org

The organization responsible for the document.

### cookiecutter.series

The identifier of the technote series which will be used ot name the repo
Choose the series that fits the document's purpose or aligns with the organization creating the document:

- `DMTN` for Data Management technical notes. See [DMTN-000](https://dmtn-000.lsst.io).
- `OPSTN` for LSST Operations technical notes.
- `PSTN` for Project Science Team technical notes.
- `SMTN` for Simulations Group technical notes. See [SMTN-000](https://smtn-000.lsst.io).
- `SITCOMTN` for Systems Integration, Testing, and Commissioning notes.
- `SQR` for SQuaRE technical notes. See [SQR-000](https://sqr-000.lsst.io).
- `TSTN` for Telescope & Site technical notes.
- `TESTN` for testing the technical system. *These notes may be purged at any time.*

### cookiecutter.serial_number

The serial number. Use three digits padded with zeros.
If you are creating a technical note manually with this template, see the [Create a technote](https://developer.lsst.io/project-docs/technotes.html#create-a-technote) instructions for how to determine the serial number.

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
- `lsst-tstn` for the TSTN series.

### cookiecutter.title

The title of the technote.

### cookiecutter.first_author

The name of the first author, formatted as `First Last`.
Additional authors can be added later in the LaTeX source itself.

### cookiecutter.abstract

A short description of the technote's content and purpose.
This description is used in the repository's README and the abstract in the document itself.

### cookiecutter.copyright_year

The year of the initial copyright claim.
Cookiecutter will automatically populate the current year.

### cookiecutter.copyright_holder

The initial copyright holder.
See [Copyrights for LSST DM work and the COPYRIGHT file](https://developer.lsst.io/legal/copyright-overview.html) for more information.

## Examples

### testn-000/

The [testn-000](testn-000) directory is an example of a LaTeX-formatted technote.

## Files

## .gitignore

Example: [.gitignore](testn-000/.gitignore).

The gitignore file ignores the built PDF product (which is persisted on LSST the Docs), as well as intermediate LaTeX build files (including `meta.tex`).
The `acronyms.tex` file is not ignored so that `make acronyms.tex` does not need to be run for every document build.

## .travis.yml

Example: [.travis.yml](testn-000/.travis.yml).

The Travis CI configuration file.
You shouldn't have to modify this file unless you have a novel preprocessing build step (see below).

**Tip:** Travis CI provides a flexible Python environment.
It's likely easier to run preprocessing scripts directly from the Travis CI environment, rather than within the lsst-texmf Docker container:

- Install additional Python dependencies in the `install` phase of the `.travis.yml` file.
- Add bash command for the preprocessing steps to the `script` list of the `.travis.yml` file, before the `docker run` command.
- Structure your `Makefile` so that files built in advance in the Travis CI environment are automatically used as-is by the `docker run` command.

For more information about using the CI environment, see the [Travis CI documentation](https://docs.travis-ci.com).

## acronyms.tex

Example: [acronyms.tex](testn-000/acronyms.tex).

This file is generated and updated by the `make acronyms.tex` command.

### COPYRIGHT

Example: [COPYRIGHT](testn-000/COPYRIGHT).

Record copyright claims in this file, one line per institution.
See the [copyright](../copyright) template and [Copyrights for LSST DM work and the COPYRIGHT file](https://developer.lsst.io/legal/copyright-overview.html).

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

The built-in targets are:

- `make`: compiles the PDF document by running `xelatex` and `bibtex` iteratively.
  This command is used by the CI environment that pushes the PDF to LSST the Docs (lsst.io).
  See the [.travis.yml](#travisyml) file.
- `make acronyms.tex`: regenerates the [acronyms.tex](#acronymstex) file.

Add additional make targets to do preprocessing steps (such as running a Python script to generate tables or figures).

### myacronyms.txt

Example: [Makefile](testn-000/Makefile).

List acronyms in this file that are not found in lsst-texmf's [lsstacronyms.txt](https://github.com/lsst/lsst-texmf/blob/master/etc/lsstacronyms.txt) or [glossary.txt](https://github.com/lsst/lsst-texmf/blob/master/etc/glossary.txt), or that have multiple definitions (put the one you want in the local `myacronyms.txt` file).

The format for each line of this file is:

```
ACRONYM:Definition
```

For example:

```
MIA:Missing In Action
```

### README.rst

Example: [README.rst](testn-000/README.rst).

The README advertises the technote to GitHub visitors and provides instructions for authors.

You can update the abstract in the README and add author instructions as necessary.

### skipacronyms.txt

Example: [skipacronyms.txt](testn-000/skipacronyms.txt).

This file contains a list acronyms that should be ignored by `generateAcronyms.py` (the script behind `make acronyms.txt`).
If your document contains acronym-like strings that aren't acronyms, you can add them to `skipacronyms.txt`.

### {{cookiecutter.series.upper()}}-{{cookiecutter.serial_number}}.tex

Example: [TESTN-000.tex](testn-000/TESTN-000.tex)

This file contains the content of the technote itself.
Either write directly in this file, or use the `\input` command to include content from other files.

For more information about writing a LaTeX document with the `lsstdoc` class file, see [Using the lsstdoc document class](https://lsst-texmf.lsst.io/lsstdoc.html).
