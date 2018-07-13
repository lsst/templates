.. py:currentmodule:: {{ cookiecutter.python_module }}

.. _{{ cookiecutter.python_module }}:

{{ "#" * cookiecutter.python_module|length }}
{{ cookiecutter.python_module }}
{{ "#" * cookiecutter.python_module|length }}

.. Paragraph that describes what this Python module does and links to related modules and frameworks.

.. .. _{{ cookiecutter.python_module }}-using:

.. Using {{ cookiecutter.python_module }}
.. {{ "=" * (cookiecutter.python_module|length + 6) }}

.. toctree linking to topics related to using the module's APIs.

.. .. toctree::
..    :maxdepth: 1

.. _{{ cookiecutter.python_module }}-contributing:

Contributing
============

``{{ cookiecutter.python_module }}`` is developed at https://github.com/{{ cookiecutter.github_org }}/{{ cookiecutter.package_name }}.
You can find Jira issues for this module under the `{{ cookiecutter.package_name }} <https://jira.lsstcorp.org/issues/?jql=project%20%3D%20DM%20AND%20component%20%3D%20{{ cookiecutter.package_name }}>`_ component.

.. If there are topics related to developing this module (rather than using it), link to this from a toctree placed here.

.. _{{ cookiecutter.python_module }}-pyapi:

Python API reference
====================

.. automodapi:: {{ cookiecutter.python_module }}
   :no-main-docstr:
   :no-inheritance-diagram:
