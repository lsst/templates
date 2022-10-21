{{ "#" * cookiecutter.name|length }}
{{ cookiecutter.name }}
{{ "#" * cookiecutter.name|length }}

{{ cookiecutter.description }}

Install {{ cookiecutter.name }} from PyPI:

.. code-block:: bash

   pip install {{ cookiecutter.name }}

{{ cookiecutter.name }} is developed on GitHub at https://github.com/{{cookiecutter.github_org}}/{{cookiecutter.name}}.

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
