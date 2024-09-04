# technote_ascomtex

**LSST technical note repository, formatted as a AASTeX paper preprint.**

This template generates a new paper repository based on [Elsevier cas Tex](https://mirrors.ctan.org/macros/latex/contrib/elsarticle.zip).
This template also uses bib and author metadata from [lsst-texmf](https://lsst-texmf.lsst.io).
See [Technotes for stand-alone technical documentation in the Developer Guide](https://developer.lsst.io/project-docs/technotes.html).

## Template variables

### cookiecutter.org

The organization responsible for the document.

### cookiecutter.series

The identifier of the technote series which will be used to name the repo
Choose the series that fits the document's purpose or aligns with the organization creating the document.
For now to make this simpler we assume Papers are DMTN or PSTN. 

- `DMTN` for Data Management technical notes. 
- `PSTN` for Project Science Team technical notes.
- `TSTN` for Telescope and Site Team technical notes.

### cookiecutter.serial_number

The serial number. Use three digits padded with zeros.
If you are creating a technical note manually with this template, see the [Create a technote](https://developer.lsst.io/project-docs/technotes.html#create-a-technote) instructions for how to determine the serial number.

### cookiecutter.github_org

The GitHub organization where this technote resides.
Choose a GitHub organization that matches the [series](#cookiecutter_series):

- `lsst-dm` for the  DMTN series.
- `lsst-pst` for the PSTN series.
- `lsst-ts` for the TSTN series.

### cookiecutter.title

The title of the technote.

### cookiecutter.author_id

The ID of the first author.
Author IDs may be found in the [https://github.com/lsst/lsst-texmf/blob/main/etc/authordb.yaml](authorsdb.yaml) file in lsst-texmf - this YAML database contains all LSST authors.
Additional authors can be added later in the `authors.yaml` file.
The file `authors.tex` is generated from the list of author codes in `authors.yaml`. 

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

## .github/workflows/ci.yaml

Example: [.github/workflows/ci.yaml](testn-000/.github/workflows/ci.yaml).

The GitHub Actions workflow file.
You shouldn't have to modify this file unless you have a novel preprocessing build step (see below).

**Tip:** GitHub Actions provides a flexible Python environment.
It's likely easier to run preprocessing scripts directly from the GitHub actions environment, rather than within the lsst-texmf Docker container:

- Install additional Python dependencies in the `Python install` step.
- Add additional bash commands for preprocessing steps to run before the `docker run` step.
- Structure your `Makefile` so that files built in advance in the GitHub actions environment are automatically used as-is by the `docker run` command.

For more information about using the CI environment, see the [GitHub actions workflow documentation](https://help.github.com/en/actions/reference/workflow-syntax-for-github-actions).

## .gitignore

Example: [.gitignore](testn-000/.gitignore).

The gitignore file ignores the built PDF product (which is persisted on LSST the Docs), as well as intermediate LaTeX build files (including `meta.tex`).
The `acronyms.tex` file is not ignored so that `make acronyms.tex` does not need to be run for every document build.

## acronyms.tex

Example: [acronyms.tex](testn-000/acronyms.tex).

This file is generated and updated by the `make acronyms.tex` command.

## authors.tex

Example: [authors.tex](testn-000/authors.tex).

The file `authors.tex` is generated from the list of author codes in `authors.yaml`.
This file is normally generated through the regular `make` command, but can also be regenerated individually by running `make authors.tex`.

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
  See the [.github/workflows/ci.yaml](#githubworkflowsciyaml) file.
- `make acronyms.tex`: regenerates the [acronyms.tex](#acronymstex) file.
- `make authors.tex`: regenerates the [authors.tex](#authorstex) file.

Add additional make targets to do preprocessing steps (such as running a Python script to generate tables or figures).

### myacronyms.txt

Example: [Makefile](testn-000/Makefile).

List acronyms in this file that are not found in lsst-texmf's [lsstacronyms.txt](https://github.com/lsst/lsst-texmf/blob/main/etc/lsstacronyms.txt) or [glossary.txt](https://github.com/lsst/lsst-texmf/blob/main/etc/glossary.txt), or that have multiple definitions (put the one you want in the local `myacronyms.txt` file).

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

For more information about writing a LaTeX document with the `elsarticle` class file, see the [Elsvier Author Guide](https://www.elsevier.com/latex).
