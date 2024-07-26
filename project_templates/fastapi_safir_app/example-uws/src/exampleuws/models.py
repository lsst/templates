"""Models for example-uws."""

from typing import Self

from pydantic import BaseModel, Field
from safir.metadata import Metadata as SafirMetadata
from safir.uws import ParametersModel, UWSJobParameter

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


class ExampleuwsParameters(ParametersModel[WorkerExampleuwsModel]):
    """Model for job parameters.

    Add fields here for all the input parameters to a job, and then update
    ``from_job_parameters`` and ``to_worker_parameters`` to do the appropriate
    conversions.
    """

    @classmethod
    def from_job_parameters(cls, params: list[UWSJobParameter]) -> Self:
        return cls()

    def to_worker_parameters(self) -> WorkerExampleuwsModel:
        return WorkerExampleuwsModel()
