.. _{{ cookiecutter.package_name }}-package:

.. Title is the EUPS package name

{{ "#" * cookiecutter.package_name|length }}
{{ cookiecutter.package_name }}
{{ "#" * cookiecutter.package_name|length }}

.. Add a sentence/short paragraph describing what the package is for.

The ``{{ cookiecutter.package_name }}`` package provides [...].

Project info
============

Repository
   https://github.com/{{ cookiecutter.github_org }}/{{ cookiecutter.package_name }}

JIRA component
   `{{ cookiecutter.package_name }} <https://jira.lsstcorp.org/issues/?jql=project%20%3D%20DM%20AND%20component%20%3D%20{{ cookiecutter.package_name }}>`_

Modules
=======

.. Link to Python module landing pages (same as in manifest.yaml)

- :ref:`{{ cookiecutter.python_module }} <{{ cookiecutter.python_module }}>`
