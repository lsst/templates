# Change log

## 2020-05-25

- Add support for the RTN technote series for operations.

## 2019-11-03

- Update to the current versions of Documenteer, >=0.5.4, <0.6.

## 2019-10-21

- Fix support for the TSTN series.

## 2019-10-08

- Template variables that are inserted into `metadata.yaml` are now fully escaped.
  This means that titles, authors, and descriptions can have characters like single and double quotes, and backslashes.

## 2019-08-26

- Add support for the Telescope & Site technote series (TSTN).

## 2019-07-29

- Add support for the ITTN technote series for LSST IT.

## 2019-04-17

- Ported from the [lsst-technote-bootstrap](https://github.com/lsst-sqre/lsst-technote-bootstrap) repository.
  This templates repository replaces that original project and is now the canonical template for Sphinx-based technotes.

- Added the `templatekit.yaml` configuration.

- Adopted the full text of the CC-BY license so that GitHub's licensee can detect the license for our technotes.

- Adopted the project-standard [COPYRIGHT file](https://developer.lsst.io/legal/copyright-overview.html).

- Switched to [LTD Conveyor](https://ltd-conveyor.lsst.io) as the upload client for LSST the Docs.
  [LTD Mason](https://ltd-mason.lsst.io) is deprecated.
