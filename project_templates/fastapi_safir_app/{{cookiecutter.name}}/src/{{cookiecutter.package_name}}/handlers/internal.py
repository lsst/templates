"""Internal HTTP handlers that serve relative to the root path, ``/``.

These handlers aren't externally visible since the app is available at a path,
``/{{ cookiecutter.name | lower }}``. See `{{ cookiecutter.package_name }}.handlers.external` for
the external endpoint handlers.

These handlers should be used for monitoring, health checks, internal status,
or other information that should not be visible outside the Kubernetes cluster.
"""

from fastapi import APIRouter
from safir.metadata import Metadata, get_metadata

from ..config import config

__all__ = ["get_index", "internal_router"]

internal_router = APIRouter()
"""FastAPI router for all internal handlers."""


@internal_router.get(
    "/",
    description=(
        "Return metadata about the running application. Can also be used as"
        " a health check. This route is not exposed outside the cluster and"
        " therefore cannot be used by external clients."
    ),
    include_in_schema=False,
    response_model=Metadata,
    response_model_exclude_none=True,
    summary="Application metadata",
)
async def get_index() -> Metadata:
    """GET ``/`` (the app's internal root).

    By convention, this endpoint returns only the application's metadata.
    """
    return get_metadata(
        package_name="{{ cookiecutter.name }}",
        application_name=config.name,
    )
