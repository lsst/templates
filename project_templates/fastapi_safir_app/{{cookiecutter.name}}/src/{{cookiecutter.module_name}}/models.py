"""Models for {{ cookiecutter.name }}."""

{% if cookiecutter.uws_service == "True" -%}
from typing import Self

{% endif -%}
from pydantic import BaseModel, Field
from safir.metadata import Metadata as SafirMetadata
{%- if cookiecutter.uws_service == "True" %}
from safir.uws import ParametersModel, UWSJobParameter

from .domain import Worker{{ cookiecutter.module_name | capitalize }}Model
{%- endif %}

__all__ = ["Index"]


class Index(BaseModel):
    """Metadata returned by the external root URL of the application.

    Notes
    -----
    As written, this is not very useful. Add additional metadata that will be
    helpful for a user exploring the application, or replace this model with
    some other model that makes more sense to return from the application API
    root.
    """

    metadata: SafirMetadata = Field(..., title="Package metadata")
{%- if cookiecutter.uws_service == "True" %}


class {{ cookiecutter.module_name | capitalize }}Parameters(ParametersModel[Worker{{ cookiecutter.module_name | capitalize }}Model]):
    """Model for job parameters.

    Add fields here for all the input parameters to a job, and then update
    ``from_job_parameters`` and ``to_worker_parameters`` to do the appropriate
    conversions.
    """

    @classmethod
    def from_job_parameters(cls, params: list[UWSJobParameter]) -> Self:
        return cls()

    def to_worker_parameters(self) -> Worker{{ cookiecutter.module_name | capitalize }}Model:
        return Worker{{ cookiecutter.module_name | capitalize }}Model()
{%- endif %}
