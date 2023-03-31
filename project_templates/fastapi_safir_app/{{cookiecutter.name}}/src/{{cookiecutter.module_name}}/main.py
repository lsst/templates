"""The main application factory for the {{ cookiecutter.name }} service.

Notes
-----
Be aware that, following the normal pattern for FastAPI services, the app is
constructed when this module is loaded and is not deferred until a function is
called.
"""

from importlib.metadata import metadata, version

from fastapi import FastAPI
from safir.dependencies.http_client import http_client_dependency
from safir.logging import configure_logging, configure_uvicorn_logging
from safir.middleware.x_forwarded import XForwardedMiddleware

from .config import config
from .handlers.external import external_router
from .handlers.internal import internal_router

__all__ = ["app", "config"]


configure_logging(
    profile=config.profile,
    log_level=config.log_level,
    name="{{ cookiecutter.module_name }}",
)
configure_uvicorn_logging(config.log_level)

app = FastAPI(
    title="{{ cookiecutter.name }}",
    description=metadata("{{ cookiecutter.name }}")["Summary"],
    version=version("{{ cookiecutter.name }}"),
    openapi_url=f"/{config.path_prefix}/openapi.json",
    docs_url=f"/{config.path_prefix}/docs",
    redoc_url=f"/{config.path_prefix}/redoc",
)
"""The main FastAPI application for {{ cookiecutter.name }}."""

# Attach the routers.
app.include_router(internal_router)
app.include_router(external_router, prefix=f"/{config.path_prefix}")

# Add middleware.
app.add_middleware(XForwardedMiddleware)


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await http_client_dependency.aclose()
