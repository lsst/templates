"""{{cookiecutter.description}}"""

__all__ = ["__version__"]

from importlib.metadata import PackageNotFoundError, version

__version__: str
"""The version string of {{cookiecutter.module_name}}
(PEP 440 / SemVer compatible).
"""

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # package is not installed
    __version__ = "0.0.0"
