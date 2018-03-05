"""Sphinx configuration file for an LSST stack package.

This configuration only affects single-package Sphinx documenation builds.
"""

from documenteer.sphinxconfig.stackconf import build_package_configs
import {{ cookiecutter.python_module }}


_g = globals()
_g.update(build_package_configs(
    project_name='{{ cookiecutter.package_name }}',
    version={{ cookiecutter.python_module }}.version.__version__))
