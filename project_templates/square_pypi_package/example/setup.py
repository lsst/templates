"""Legacy setuptools build front-end (pre PEP 517).

Although this project follows PEP 517, a setup.py is included for backwards
compatibility for older setuptools and editabable pip installs.
"""

from setuptools import setup

setup(use_scm_version=True)
