# latex_lsstdoc

**General purpose LaTeX document template that features the [lsstdoc class from lsst-texmf](https://lsst-texmf.lsst.io/lsstdoc.html).**

Use this template to create any type of Rubin Observatory LaTeX document, especially ones that have a pre-assigned DocuShare document handle (technical notes should still use the [technote_latex](../technote_latex) template)).

## Template variables

### cookiecutter.handle

The document's handle (as assigned by DocuShare).
This becomes the name of the document's repository on GitHub.

### cookiecutter.series

The document's series, such as "LPM" or "LSE."

If the document does not belong to a series (because its handle is free-form), leave the series empty.

### cookiecutter.serial_number

The numeric suffix of the document handle.
The handle is assigned by DocuShare.

If the document does not belong to a series (because its handle is free-form), leave the series empty.

### cookiecutter.github_org

The GitHub organization where this document's repository is hosted.

### cookiecuttter.lsstdoc_org

The organization parameter for the lsstdoc LaTeX class file.

### cookiecutter.title

The title of the document.

### cookiecutter.author

The name of the author or curator.

## Examples

### EXAMPLE-0/

The [EXAMPLE-0](EXAMPLE-0) directory is an example of a document with a conventionally-structured DocuShare handle.

### EXAMPLE/

The [EXAMPLE](EXAMPLE) directory is an example of a document with a free-form handle (it does not have a series or serial number).
