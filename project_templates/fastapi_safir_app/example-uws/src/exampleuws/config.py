"""Configuration definition."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import SettingsConfigDict
from safir.logging import LogLevel, Profile
from safir.uws import UWSApplication, UWSAppSettings, UWSConfig, UWSRoute

from .dependencies import post_params_dependency
from .models import ExampleuwsParameters

__all__ = ["Config", "config"]


class Config(UWSAppSettings):
    """Configuration for example-uws."""

    name: str = Field("example-uws", title="Name of application")

    path_prefix: str = Field(
        "/example-uws", title="URL prefix for application"
    )

    profile: Profile = Field(
        Profile.development, title="Application logging profile"
    )

    log_level: LogLevel = Field(
        LogLevel.INFO, title="Log level of the application's logger"
    )

    model_config = SettingsConfigDict(
        env_prefix="EXAMPLE_UWS_", case_sensitive=False
    )

    @property
    def uws_config(self) -> UWSConfig:
        """Corresponding configuration for the UWS subsystem."""
        return self.build_uws_config(
            parameters_type=ExampleuwsParameters,
            worker="example_uws",
            async_post_route=UWSRoute(
                dependency=post_params_dependency,
                summary="Create async example-uws job",
                description="Create a new UWS job for example-uws",
            ),
        )


config = Config()
"""Configuration for example-uws."""

uws = UWSApplication(config.uws_config)
"""The UWS application for this service."""
