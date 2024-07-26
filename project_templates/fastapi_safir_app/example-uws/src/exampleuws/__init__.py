"""The example-uws service."""

__all__ = ["__version__"]

from importlib.metadata import PackageNotFoundError, version

__version__: str
"""The application version string (PEP 440 / SemVer compatible)."""

try:
    __version__ = version("example-uws")
except PackageNotFoundError:
    # package is not installed
    __version__ = "0.0.0"
