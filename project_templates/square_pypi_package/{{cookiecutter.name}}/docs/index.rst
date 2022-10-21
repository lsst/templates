:og:description: {{ cookiecutter.description }}
:html_theme.sidebar_secondary.remove:

{{ "#" * cookiecutter.name|length }}
{{ cookiecutter.name }}
{{ "#" * cookiecutter.name|length }}

{{ cookiecutter.description }}

Install {{ cookiecutter.name }} from PyPI:

.. code-block:: bash

   pip install {{ cookiecutter.name }}

{{ cookiecutter.name }} is developed on GitHub at https://github.com/{{cookiecutter.github_org}}/{{cookiecutter.name}}.

.. toctree::
   :hidden:

   User guide <user-guide/index>
   API <api>
   Change log <changelog>
   Contributing <dev/index>
