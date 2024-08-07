"""Configuration definition."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import {% if cookiecutter.flavor != "UWS" %}BaseSettings, {% endif %}SettingsConfigDict
from safir.logging import LogLevel, Profile
{%- if cookiecutter.flavor == "UWS" %}
from safir.uws import UWSApplication, UWSAppSettings, UWSConfig, UWSRoute

from .dependencies import post_params_dependency
from .models import {{ cookiecutter.module_name | capitalize }}Parameters
{%- endif %}

__all__ = ["Config", "config"]


class Config({% if cookiecutter.flavor == "UWS" %}UWSAppSettings{% else %}BaseSettings{% endif %}):
    """Configuration for {{ cookiecutter.name }}."""

    name: str = Field("{{ cookiecutter.name }}", title="Name of application")

    path_prefix: str = Field(
        "/{{ cookiecutter.name | lower }}", title="URL prefix for application"
    )

    profile: Profile = Field(
        Profile.development, title="Application logging profile"
    )

    log_level: LogLevel = Field(
        LogLevel.INFO, title="Log level of the application's logger"
    )

    model_config = SettingsConfigDict(
        env_prefix="{{ cookiecutter.name | upper | replace('-', '_') }}_", case_sensitive=False
    )
{%- if cookiecutter.flavor == "UWS" %}

    @property
    def uws_config(self) -> UWSConfig:
        """Corresponding configuration for the UWS subsystem."""
        return self.build_uws_config(
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
