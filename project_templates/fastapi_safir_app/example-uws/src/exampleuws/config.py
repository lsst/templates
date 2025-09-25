"""Configuration definition."""

from __future__ import annotations

from pydantic import Field, SecretStr
from pydantic_settings import SettingsConfigDict
from safir.logging import LogLevel, Profile
from safir.uws import UWSApplication, UWSAppSettings, UWSConfig, UWSRoute
from vo_models.uws import JobSummary

from .dependencies import post_params_dependency
from .models import ExampleuwsParameters, ExampleuwsXmlParameters

__all__ = ["Config", "config"]


class Config(UWSAppSettings):
    """Configuration for example-uws."""

    model_config = SettingsConfigDict(
        env_prefix="EXAMPLE_UWS_", case_sensitive=False
    )

    log_level: LogLevel = Field(
        LogLevel.INFO, title="Log level of the application's logger"
    )

    log_profile: Profile = Field(
        Profile.development, title="Application logging profile"
    )

    name: str = Field("example-uws", title="Name of application")

    path_prefix: str = Field(
        "/example-uws", title="URL prefix for application"
    )

    slack_webhook: SecretStr | None = Field(
        None,
        title="Slack webhook for alerts",
        description="If set, alerts will be posted to this Slack webhook",
    )

    @property
    def uws_config(self) -> UWSConfig:
        """Corresponding configuration for the UWS subsystem."""
        return self.build_uws_config(
            job_summary_type=JobSummary[ExampleuwsXmlParameters],
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
