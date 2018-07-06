{{ "#" * cookiecutter.package_name|length }}
{{ cookiecutter.package_name }}
{{ "#" * cookiecutter.package_name|length }}

``{{ cookiecutter.package_name }}`` is a package in the `LSST Science Pipelines <https://pipelines.lsst.io>`_.

.. Add a brief (few sentence) description of what this package provides.

{%- if cookiecutter.uses_python == 'False' %}
Package documentation: https://pipelines.lsst.io/packages/{{ cookiecutter.package_name }}.
{% endif %}
