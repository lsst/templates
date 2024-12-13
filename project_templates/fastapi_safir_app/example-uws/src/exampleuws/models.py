"""Models for example-uws."""

from typing import Self

from pydantic import BaseModel, Field
from safir.metadata import Metadata as SafirMetadata
from safir.uws import ParametersModel
from vo_models.uws import Parameters

from .domain import WorkerExampleuwsModel

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


class ExampleuwsXmlParameters(Parameters):
    """XML representation of job parameters.

    Add fields here for all the input parameters to the job in the format
    suitable for the IVOA UWS standard (key/value parameters). If a key can be
    repeated, use ``MultiValuedParameter`` as its type. Otherwise, use
    ``Parameter``.
    """


class ExampleuwsParameters(ParametersModel[WorkerExampleuwsModel, ExampleuwsXmlParameters]):
    """Model for job parameters.

    Add fields here for all the input parameters to a job, and then update
    ``to_worker_parameters`` and ``to_xml_model`` to do the appropriate
    conversions.
    """

    def to_worker_parameters(self) -> WorkerExampleuwsModel:
        return WorkerExampleuwsModel()

    def to_xml_model(self) -> ExampleuwsXmlParameters:
        return ExampleuwsXmlParameters()
