"""Handlers for the app's external root, ``/{{ cookiecutter.package_name }}/``."""

from fastapi import APIRouter, Depends
from safir.dependencies.logger import logger_dependency
from safir.metadata import get_metadata
from structlog.stdlib import BoundLogger

from ..config import config
from ..models.metadata import Metadata

__all__ = ["get_index", "external_router"]

external_router = APIRouter()
"""FastAPI router for all external handlers."""


@external_router.get(
    "/",
    description=(
        "Document the top-level API here. By default it only returns metadata"
        " about the application."
    ),
    response_model=Metadata,
    response_model_exclude_none=True,
    summary="Application metadata",
)
async def get_index(
    logger: BoundLogger = Depends(logger_dependency),
) -> Metadata:
    """GET ``/{{ cookiecutter.package_name }}/`` (the app's external root).

    Customize this handler to return whatever the top-level resource of your
    application should return. For example, consider listing key API URLs.
    When doing so, also change or customize the response model in
    {{ cookiecutter.package_name }}.models.metadata.

    By convention, the root of the external API includes a field called
    ``metadata`` that provides the same Safir-generated metadata as the
    internal root endpoint.
    """
    # There is no need to log simple requests since uvicorn will do this
    # automatically, but this is included as an example of how to use the
    # logger for more complex logging.
    logger.info("Request for application metadata")

    metadata = get_metadata(
        package_name="{{ cookiecutter.package_name }}",
        application_name=config.name,
    )
    return Metadata(metadata=metadata)
