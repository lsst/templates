"""The {{ cookiecutter.package_name }} service."""

__all__ = ["__version__", "metadata"]

import sys

if sys.version_info < (3, 8):
    from importlib_metadata import version, PackageNotFoundError
else:
    from importlib.metadata import version, PackageNotFoundError


__version__: str
"""The application version string of (PEP 440 / SemVer compatible)."""

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # package is not installed
    __version__ = "0.0.0"
