"""Sphinx configuration file for an LSST stack package.

This configuration only affects single-package Sphinx documenation builds.
"""

from documenteer.sphinxconfig.stackconf import build_package_configs
import lsst.example.subpackage


_g = globals()
_g.update(build_package_configs(
    project_name='example_subpackage',
    version=lsst.example.subpackage.version.__version__))
