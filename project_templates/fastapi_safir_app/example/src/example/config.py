"""Configuration definition."""

from __future__ import annotations

from pydantic import BaseSettings, Field
from safir.logging import LogLevel, Profile

__all__ = ["Configuration", "config"]


class Configuration(BaseSettings):
    """Configuration for example."""

    name: str = Field(
        "example",
        title="Name of application",
        description="Doubles as the root HTTP endpoint path.",
        env="SAFIR_NAME",
    )

    profile: Profile = Field(
        Profile.development,
        title="Application logging profile",
        env="SAFIR_PROFILE",
    )

    log_level: LogLevel = Field(
        LogLevel.INFO,
        title="Log level of the application's logger",
        env="SAFIR_LOG_LEVEL",
    )


config = Configuration()
"""Configuration for example."""
