{{ "#" * cookiecutter.package_name|length }}
{{ cookiecutter.package_name }}
{{ "#" * cookiecutter.package_name|length }}

{% if cookiecutter.stack_name == "LSST Science Pipelines" %}``{{ cookiecutter.package_name }}`` is a package in the `LSST Science Pipelines <https://pipelines.lsst.io>`_.{%- endif %}

.. Add a brief (few sentence) description of what this package provides.

{%- if cookiecutter.stack_name == "LSST Science Pipelines" and cookiecutter.uses_python == 'False' and cookiecutter.uses_cpp == 'False' %}
Package documentation: https://pipelines.lsst.io/packages/{{ cookiecutter.package_name }}.
{% endif %}
