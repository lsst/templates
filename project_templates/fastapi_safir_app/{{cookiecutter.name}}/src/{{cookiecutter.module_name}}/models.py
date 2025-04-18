"""Models for {{ cookiecutter.name }}."""

{% if cookiecutter.flavor == "UWS" -%}
from typing import Self

{% endif -%}
from pydantic import BaseModel, Field
from safir.metadata import Metadata as SafirMetadata
{%- if cookiecutter.flavor == "UWS" %}
from safir.uws import ParametersModel
from vo_models.uws import Parameters

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
{%- if cookiecutter.flavor == "UWS" %}


class {{ cookiecutter.module_name | capitalize}}XmlParameters(Parameters):
    """XML representation of job parameters.

    Add fields here for all the input parameters to the job in the format
    suitable for the IVOA UWS standard (key/value parameters). If a key can be
    repeated, use ``MultiValuedParameter`` as its type. Otherwise, use
    ``Parameter``.
    """


class {{ cookiecutter.module_name | capitalize }}Parameters(ParametersModel[Worker{{ cookiecutter.module_name | capitalize }}Model, {{ cookiecutter.module_name | capitalize}}XmlParameters]):
    """Model for job parameters.

    Add fields here for all the input parameters to a job, and then update
    ``to_worker_parameters`` and ``to_xml_model`` to do the appropriate
    conversions.
    """

    def to_worker_parameters(self) -> Worker{{ cookiecutter.module_name | capitalize }}Model:
        return Worker{{ cookiecutter.module_name | capitalize }}Model()

    def to_xml_model(self) -> {{ cookiecutter.module_name | capitalize}}XmlParameters:
        return {{ cookiecutter.module_name | capitalize}}XmlParameters()
{%- endif %}
