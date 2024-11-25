"""The main application factory for the {{ cookiecutter.name }} service.

Notes
-----
Be aware that, following the normal pattern for FastAPI services, the app is
constructed when this module is loaded and is not deferred until a function is
called.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from importlib.metadata import metadata, version

import structlog
from fastapi import FastAPI
from safir.dependencies.http_client import http_client_dependency
from safir.logging import configure_logging, configure_uvicorn_logging
from safir.middleware.x_forwarded import XForwardedMiddleware
from safir.slack.webhook import SlackRouteErrorHandler

from .config import config{% if cookiecutter.flavor == "UWS" %}, uws{% endif %}
from .handlers.external import external_router
from .handlers.internal import internal_router

__all__ = ["app"]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Set up and tear down the application."""
    # Any code here will be run when the application starts up.
    {%- if cookiecutter.flavor == "UWS" %}
    await uws.initialize_fastapi()
    {%- endif %}

    yield

    # Any code here will be run when the application shuts down.
    {%- if cookiecutter.flavor == "UWS" %}
    await uws.shutdown_fastapi()
    {%- endif %}
    await http_client_dependency.aclose()


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
    openapi_url=f"{config.path_prefix}/openapi.json",
    docs_url=f"{config.path_prefix}/docs",
    redoc_url=f"{config.path_prefix}/redoc",
    lifespan=lifespan,
)
"""The main FastAPI application for {{ cookiecutter.name }}."""

# Attach the routers.
app.include_router(internal_router)
{%- if cookiecutter.flavor == "UWS" %}
uws.install_handlers(external_router)
{%- endif %}
app.include_router(external_router, prefix=f"{config.path_prefix}")

# Add middleware.
app.add_middleware(XForwardedMiddleware)
{%- if cookiecutter.flavor == "UWS" %}
uws.install_middleware(app)

# Install error handlers.
uws.install_error_handlers(app)
{%- endif %}

# Configure Slack alerts.
if config.slack_webhook:
    logger = structlog.get_logger("{{ cookiecutter.module_name }}")
    SlackRouteErrorHandler.initialize(
        config.slack_webhook, "{{ cookiecutter.name }}", logger
    )
    logger.debug("Initialized Slack webhook")
