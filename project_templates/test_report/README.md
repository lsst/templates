# test_report

**Test report template, formatted LaTeX (lsstdoc class), and compatible with [docsteady](https://github.com/lsst-dm/docsteady).**

Use this template to seed a GitHub repository for generating a test report that's built by GitHub Actions and published with LSST the Docs.
Use [docsteady](https://github.com/lsst-dm/docsteady) to replace the stub tex file with test report content.

Before using this template, the report's handle must be reserved in DocuShare.

## Template variables

### cookiecutter.series

The document's series:

- `DMTR` is the handle for test reports.
- `TESTTR` is a handle for testing the template.

### cookiecutter.serial_number

The numeric suffix of the document handle.
The handle is assigned by DocuShare.

### cookiecutter.github_org

The GitHub organization where this document's repository is hosted.

### cookiecutter.title

The milestone name of the report.

### cookiecutter.author

The name of the author or curator.

### cookiecutter.plan

The milestone ID or test plan (e.g. LVV-P73).

## Examples

### TESTTR-0/

The [TESTTR-0](TESTTR-000) directory is an example of test report.
