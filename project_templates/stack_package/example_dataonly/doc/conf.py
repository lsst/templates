"""Sphinx configuration file for an LSST stack package.

This configuration only affects single-package Sphinx documenation builds.
"""

from documenteer.sphinxconfig.stackconf import build_package_configs
import lsst.example.dataonly


_g = globals()
_g.update(build_package_configs(
    project_name='example_dataonly',
    version=lsst.example.dataonly.version.__version__))
