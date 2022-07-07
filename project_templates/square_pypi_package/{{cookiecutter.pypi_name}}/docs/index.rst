{{ "#" * cookiecutter.pypi_name|length }}
{{ cookiecutter.pypi_name }}
{{ "#" * cookiecutter.pypi_name|length }}

{{ cookiecutter.description }}

Install {{ cookiecutter.pypi_name }} from PyPI:

.. code-block:: bash

   pip install {{ cookiecutter.pypi_name }}

{{ cookiecutter.pypi_name }} is developed on GitHub at https://github.com/{{cookiecutter.github_org}}/{{cookiecutter.pypi_name}}.

User guide
==========

.. toctree::

   changelog
   api

Development guide
=================

.. toctree::

   dev/development
   dev/release
