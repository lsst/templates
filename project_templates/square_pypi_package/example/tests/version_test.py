"""Test the packaging."""

from __future__ import annotations

from example import __version__


def test_version() -> None:
    """Ensure that the version is set."""
    assert isinstance(__version__, str)
    # Indicates the package is not installed otherwise
    assert __version__ != "0.0.0"
