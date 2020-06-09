..
  This is a template for documentation that will accompany each CSC.
  It consists of a user guide and development guide, however, cross linking between the guides is expected.
  This template is provided to ensure that the documentation remains similar in look, feel, and contents to users.
  The headings below are expected to be present for all CSCs, but for many CSCs, additional fields will be required.
  An example case can be found at https://ts-athexapod.lsst.io/v/develop/

  ** All text in square brackets [] must be re-populated accordingly **

  See https://developer.lsst.io/restructuredtext/style.html
  for a guide to reStructuredText writing.

  Use the following syntax for sections:

  Sections
  ========

  and

  Subsections
  -----------

  and

  Subsubsections
  ^^^^^^^^^^^^^^

  To add images, add the image file (png, svg or jpeg preferred) to the
  images/ directory. The reST syntax for adding the image is

  .. figure:: /images/filename.ext
   :name: fig-label

  Caption text.

  Feel free to delete this instructional comment.

.. Fill out data so contacts section below is auto-populated
.. add name and email between the *'s below e.g. *Marie Smith <msmith@lsst.org>*
.. |CSC_developer| replace::  *Replace-with-name-and-email*
.. |CSC_product_owner| replace:: *Replace-with-name-and-email*

.. Note that the "ts_" prefix is omitted from the title

############
Barracuda
############
.. update the following links to point to your CSC (rather than the athexapod)
.. image:: https://img.shields.io/badge/GitHub-ts_barracuda-green.svg
    :target: https://github.com/lsst-ts/ts_barracuda
.. image:: https://img.shields.io/badge/Jenkins-ts_barracuda-green.svg
    :target: https://tssw-ci.lsst.org/job/LSST_Telescope-and-Site/job/ts_barracuda/
.. image:: https://img.shields.io/badge/Jira-ts_barracuda-green.svg
    :target: https://jira.lsstcorp.org/issues/?jql=labels+%3D+ts_barracuda
.. image:: https://img.shields.io/badge/ts_xml-{cookiecutter.csc_name}}-green.svg
    :target: https://ts-xml.lsst.io/sal_interfaces/Barracuda.html

.. TODO: Delete the note when the page becomes populated

.. Warning::

   **This CSC documentation is under development and not ready for active use.**

.. _Overview:

Overview
========

[This section is to present an overview of the CSC.
This should include a top-level description of the primary use-case(s) as well as any pertinent information.
Example information may be link(s) to the higher-level classes which may be used to operate it, or mention of other CSCs (with links) that it operates in concert with.]

.. note:: If you are interested in viewing other branches of this repository append a `/v` to the end of the url link. For example `https://ts-xml.lsst.io/v/`


.. _User_Documentation:

User Documentation
==================
User-level documentation, found at the link below, is aimed at personnel looking to perform the standard use-cases/operations with the Barracuda.

.. toctree::
    user-guide/user-guide
    :maxdepth: 2

.. _Configuration:

Configuring the Barracuda
=====================
.. For CSCs where configuration is not required, this section can contain a single sentence stating so.
   More introductory information can also be added here (e.g. CSC XYZ requires both a configuration file containing parameters as well as several look-up tables to be operational).

The configuration for the Barracuda is described at the following link.

.. toctree::
    configuration/configuration
    :maxdepth: 1


.. _Development_Documentation:

Development Documentation
=========================
This area of documentation focuses on the classes used, API's, and how to participate to the development of the Barracuda software packages.

.. toctree::
    developer-guide/developer-guide
    :maxdepth: 1

.. _Version_History:

Version History
===============

.. Version history/release notes are not yet standardized amongst CSCs. Depending upon the implementation, a single link to a file (e.g. release notes) may be sufficient.

The version history of the Barracuda is found at the following link.

.. toctree::
    version-history
    :maxdepth: 1


.. _Contact_Personnel:

Contact Personnel
=================

For questions not covered in the documentation, emails should be addressed to |CSC_developer| and |CSC_product_owner|.

This page was last modified |today|.

