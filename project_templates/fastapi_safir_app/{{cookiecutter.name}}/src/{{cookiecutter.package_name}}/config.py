"""Configuration definition."""

from __future__ import annotations

from pydantic import BaseSettings, Field
from safir.logging import LogLevel, Profile

__all__ = ["Configuration", "config"]


class Configuration(BaseSettings):
    """Configuration for {{ cookiecutter.package_name }}."""

    name: str = Field(
        "{{ cookiecutter.name | lower }}",
        title="Name of application",
        description="Doubles as the root HTTP endpoint path.",
        env="SAFIR_NAME",
    )

    profile: Profile = Field(
        Profile.development,
        title="Application logging profile",
        env="SAFIR_PROFILE",
    )

    logger_name: str = Field(
        "{{ cookiecutter.package_name }}",
        title="Root name of application's logger",
        env="SAFIR_LOGGER",
    )

    log_level: LogLevel = Field(
        LogLevel.INFO,
        title="Log level of the application's logger",
        env="SAFIR_LOG_LEVEL",
    )


config = Configuration()
"""Configuration for {{ cookiecutter.name }}."""
