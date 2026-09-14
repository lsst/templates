#################
Development guide
#################

This page provides procedures and guidelines for developing and contributing to {{cookiecutter.name}}.

Scope of contributions
======================

{{cookiecutter.name}} is an open source package, meaning that you can contribute to {{cookiecutter.name}} itself, or fork {{cookiecutter.name}} for your own purposes.

Since {{cookiecutter.name}} is intended for internal use by Rubin Observatory, community contributions can only be accepted if they align with Rubin Observatory's aims.
For that reason, it's a good idea to propose changes with a new `GitHub issue`_ before investing time in making a pull request.

{{cookiecutter.name}} is developed by the Rubin Observatory SQuaRE team.

.. _GitHub issue: https://github.com/{{cookiecutter.github_org}}/{{cookiecutter.name}}/issues/new

.. _dev-environment:

Setting up a local development environment
==========================================

{{cookiecutter.name}} is developed using uv_.
You will therefore need uv installed to set up a development environment.
See the `uv installation instructions <https://docs.astral.sh/uv/getting-started/installation/>`__ for details.

Once you have those prerequisites installed, get started by cloning the repository and setting up a virtual environment:

.. code-block:: sh

   git clone https://github.com/{{cookiecutter.github_org}}/{{cookiecutter.name}}.git
   cd {{cookiecutter.name}}
   make init

This init step does three things:

1. Creates a Python virtual environment in the :file:`.venv` subdirectory with the packages needed to do {{cookiecutter.name}} development installed.
2. Installs {{cookiecutter.name}} in an editable mode in that virtual environment.
3. Installs the pre-commit hooks (run by prek_).

You can activate the {{cookiecutter.name}} virtual environment if you wish with:

.. code-block:: sh

   source .venv/bin/activate

This is optional; you do not have to activate the virtual environment to do development.
However, if you do, you can omit :command:`uv run` from the start of all commands described below.
Also, editors with Python integration, such as VSCode, may work more smoothly if you activate the virtualenv before starting them.

.. _pre-commit-hooks:

Pre-commit hooks
================

The pre-commit hooks, which are automatically installed by running the :command:`make init` command on :ref:`set up <dev-environment>`, ensure that files are valid and properly formatted.
Some pre-commit hooks automatically reformat code:

``ruff``
    Automatically formats Python code and applies safe fixes to lint issues.

``blacken-docs``
    Automatically formats Python code in reStructuredText documentation and docstrings.

When these hooks fail, your Git commit will be aborted.
To proceed, stage the new modifications and proceed with your Git commit.

If you have to commit changes that fail pre-commit checks, pass the ``--no-verify`` flag to :command:`git commit`.
This will have to be temporary, though, since the change will fail GitHub CI checks.

Despite the name, {{cookiecutter.name}} uses prek_ to run pre-commit hooks rather than the package named pre-commit.

.. _dev-run-tests:

Running tests
=============

{{cookiecutter.name}} uses nox_ as its automation tool for testing.

To run all {{cookiecutter.name}} tests, run:

.. code-block:: sh

   uv run nox

This will run several nox sessions to lint and type-check the code, run the test suite, and build the documentation.

To list the available sessions, run:

.. prompt:: bash

   uv run nox --list

To run a specific test or list of tests, you can add test file names (and any other pytest_ options) after ``--`` when executing the ``test`` nox session.
For example:

.. prompt:: bash

   uv run nox -s test -- tests/example_test.py

{{cookiecutter.name}} uses the `Safir test data library <https://safir.lsst.io/user-guide/test-data.html>`__ to manage test data.
If you change the code in a way that would change test output, run:

.. prompt:: bash

   uv run nox -s test -- --update-test-data

This will update any test output files to match the current output of the test suite.
Review any changes with :command:`git diff` and ensure they match the expected changes.

.. _dev-build-docs:

Building documentation
======================

Documentation is built with Sphinx_.
It is built as part of a normal test run to check that the documentation can still build without warnings, or can be built explicitly with:

.. _Sphinx: https://www.sphinx-doc.org/en/master/

.. code-block:: sh

   uv run nox -s docs

The built documentation is located in the :file:`docs/_build/html` directory.

Additional dependencies required for the documentation build should be added to the ``docs`` dependency group in :file:`pyproject.toml`.

Documentation builds are incremental, and generate and use cached descriptions of the internal Python APIs.
If you see errors in building the Python API documentation or have problems with changes to the documentation (particularly diagrams) not showing up, try a clean documentation build with:

.. prompt:: bash

   uv run nox -s docs-clean

This will be slower, but it will ensure that the documentation build doesn't rely on any cached data.

To check the documentation for broken links, run:

.. code-block:: sh

   uv run nox -s docs-linkcheck

Update pinned dependencies
==========================

All dependencies of {{cookiecutter.name}} are pinned to specific versions for local development and for GitHub Actions CI jobs to ensure reproducible results.
These dependency pins do not affect use of {{cookiecutter.name}} as a library.
They are only used during development.

To update the pinned dependencies, including the versions of the pre-commit hooks, run:

.. code-block:: sh

   make update-deps

You may wish to do this at the start of a development cycle so that you're using the latest versions of the linters.

You can instead run :command:`make update` to also update the installed dependencies in the development virtual environment.

.. _dev-change-log:

Updating the change log
=======================

{{cookiecutter.name}} uses scriv_ to maintain its change log.

When preparing a pull request, run :command:`scriv create`.
This will create a change log fragment in :file:`changelog.d`.
Edit that fragment, removing the sections that do not apply and adding entries fo this pull request.
You can pass the ``--edit`` flag to :command:`scriv create` to open the created fragment automatically in an editor.

Change log entries use the following sections:

.. rst-class:: compact

- **Backward-incompatible changes**
- **New features**
- **Bug fixes**
- **Other changes** (for minor, patch-level changes that are not bug fixes, such as logging formatting changes or updates to the documentation)

The change log entries should be written in imperative tense and describe to the user the change in behavior or the impact on the user at a high level.
Changes that are not visible to the user, including minor documentation changes, should not have a change log fragment.
Technical descriptions of how the change was implemented belong in commit messages, not change log entries.

Formatting change log entries
-----------------------------

These entries will eventually be cut and pasted into the release description for the next release, so the Markdown for the change descriptions must be compatible with GitHub's Markdown conventions for the release description.
Specifically:

- Each bullet point should be entirely on one line, even if it contains multiple sentences.
  This is an exception to the normal documentation convention of a newline after each sentence.
  Unfortunately, GitHub interprets those newlines as hard line breaks, so they would result in an ugly release description.
- Be cautious with complex markup, such as nested bullet lists, since the formatting in the GitHub release description may not be what you expect and manually repairing it is tedious.

.. _style-guide:

Style guide
===========

Code
----

- The code style follows :pep:`8`, though in practice lean on Black and isort to format the code for you.

- Use :pep:`484` type annotations.
  The :command:`uv run nox -s typing` session, which runs mypy_, ensures that the project's types are consistent.

- {{cookiecutter.name}} uses the Ruff_ linter with most checks enabled.
  Try to avoid ``noqa`` markers except for issues that need to be fixed in the future.
  Tests that generate false positives should normally be disabled, but if the lint error can be avoided with minor rewriting that doesn't make the code harder to read, prefer the rewriting.

- Write tests for Pytest_.

Documentation
-------------

- Follow the `LSST DM User Documentation Style Guide`_, which is primarily based on the `Google Developer Style Guide`_.

- Document the Python API with numpydoc-formatted docstrings.
  See the `LSST DM Docstring Style Guide`_.

- Follow the `LSST DM ReStructuredTextStyle Guide`_.
  In particular, ensure that prose is written **one-sentence-per-line** for better Git diffs.

.. _`LSST DM User Documentation Style Guide`: https://developer.lsst.io/user-docs/index.html
.. _`Google Developer Style Guide`: https://developers.google.com/style/
.. _`LSST DM Docstring Style Guide`: https://developer.lsst.io/python/style.html
.. _`LSST DM ReStructuredTextStyle Guide`: https://developer.lsst.io/restructuredtext/style.html
