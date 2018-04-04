{{ "#" * (cookiecutter.package_name|length + 22) }}
{{ cookiecutter.package_name}} documentation preview
{{ "#" * (cookiecutter.package_name|length + 22) }}

.. This page is for local development only. It isn't published to pipelines.lsst.io.

.. Link the index pages of package and module documentation directions (listed in manifest.yaml).

.. toctree::
   :maxdepth: 1

   {{ cookiecutter.package_name }}/index
   {{ cookiecutter.python_module }}/index
