"""Configuration definition."""

from __future__ import annotations

from pydantic import Field, SecretStr
from pydantic_settings import {% if cookiecutter.flavor != "UWS" %}BaseSettings, {% endif %}SettingsConfigDict
from safir.logging import LogLevel, Profile
{%- if cookiecutter.flavor == "UWS" %}
from safir.uws import UWSApplication, UWSAppSettings, UWSConfig, UWSRoute
from vo_models.uws import JobSummary

from .dependencies import post_params_dependency
from .models import {{ cookiecutter.module_name | capitalize }}Parameters, {{ cookiecutter.module_name | capitalize }}XmlParameters
{%- endif %}

__all__ = ["Config", "config"]


class Config({% if cookiecutter.flavor == "UWS" %}UWSAppSettings{% else %}BaseSettings{% endif %}):
    """Configuration for {{ cookiecutter.name }}."""

    model_config = SettingsConfigDict(
        env_prefix="{{ cookiecutter.name | upper | replace('-', '_') }}_", case_sensitive=False
    )

    log_level: LogLevel = Field(
        LogLevel.INFO, title="Log level of the application's logger"
    )

    name: str = Field("{{ cookiecutter.name }}", title="Name of application")

    path_prefix: str = Field(
        "/{{ cookiecutter.name | lower }}", title="URL prefix for application"
    )

    profile: Profile = Field(
        Profile.development, title="Application logging profile"
    )

    slack_webhook: SecretStr | None = Field(
        None,
        title="Slack webhook for alerts",
        description="If set, alerts will be posted to this Slack webhook",
    )
{%- if cookiecutter.flavor == "UWS" %}

    @property
    def uws_config(self) -> UWSConfig:
        """Corresponding configuration for the UWS subsystem."""
        return self.build_uws_config(
            job_summary_type=JobSummary[{{ cookiecutter.module_name | capitalize }}XmlParameters],
            parameters_type={{ cookiecutter.module_name | capitalize }}Parameters,
            worker="{{ cookiecutter.name | replace('-', '_') }}",
            async_post_route=UWSRoute(
                dependency=post_params_dependency,
                summary="Create async {{ cookiecutter.name }} job",
                description="Create a new UWS job for {{ cookiecutter.name }}",
            ),
        )
{%- endif %}


config = Config()
"""Configuration for {{ cookiecutter.name }}."""
{%- if cookiecutter.flavor == "UWS" %}

uws = UWSApplication(config.uws_config)
"""The UWS application for this service."""
{%- endif %}
