.. _{{ cookiecutter.package_name }}-package:

.. Title is the EUPS package name

{{ "#" * cookiecutter.package_name|length }}
{{ cookiecutter.package_name }}
{{ "#" * cookiecutter.package_name|length }}

.. Add a sentence/short paragraph describing what the package is for.

The ``{{ cookiecutter.package_name }}`` package provides [...].

.. .. _{{ cookiecutter.python_module }}-using:

.. Using {{ cookiecutter.package_name }}
.. {{ "=" * (cookiecutter.package_name|length + 6) }}

.. toctree linking to topics related to using the package's data.

.. .. toctree::
..    :maxdepth: 1

.. _{{ cookiecutter.package_name }}-contributing:

Contributing
============

``{{ cookiecutter.python_module }}`` is developed at https://github.com/{{ cookiecutter.github_org }}/{{ cookiecutter.package_name }}.
You can find Jira issues for this module under the `{{ cookiecutter.package_name }} <https://jira.lsstcorp.org/issues/?jql=project%20%3D%20DM%20AND%20component%20%3D%20{{ cookiecutter.package_name }}>`_ component.

.. If there are topics related to developing this package (rather than using it), link to this from a toctree placed here.

.. .. toctree::
..    :maxdepth: 1
