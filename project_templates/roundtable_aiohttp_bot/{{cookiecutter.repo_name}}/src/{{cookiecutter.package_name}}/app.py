"""The main application definition for {{ cookiecutter.package_name }} service.
"""

__all__ = ["create_app"]

import sys
from typing import Any, Dict

from aiohttp import web
from safir.http import init_http_session
from safir.logging import configure_logging
from safir.middleware import bind_logger

from {{ cookiecutter.package_name }}.config import Configuration
from {{ cookiecutter.package_name }}.handlers import init_external_routes, init_internal_routes

if sys.version_info < (3, 8):
    from importlib_metadata import metadata, PackageNotFoundError
else:
    from importlib.metadata import metadata, PackageNotFoundError


def create_app() -> web.Application:
    """Create and configure the aiohttp.web application.
    """
    config = Configuration()
    configure_logging(
        profile=config.profile,
        log_level=config.log_level,
        name=config.logger_name
    )

    root_app = web.Application()
    root_app["safir/config"] = config
    setup_metadata(app=root_app, config=config)
    setup_middleware(root_app)
    root_app.add_routes(init_internal_routes())
    root_app.cleanup_ctx.append(init_http_session)

    sub_app = web.Application()
    setup_middleware(sub_app)
    sub_app.add_routes(init_external_routes())
    root_app.add_subapp(f'/{root_app["safir/config"].name}', sub_app)

    return root_app


def setup_middleware(app: web.Application) -> None:
    """Add middleware to the application.
    """
    app.middlewares.append(bind_logger)


def setup_metadata(*, app: web.Application, config: Configuration) -> None:
    """Add a metadata object to the application under the ``safir/metadata``
    key.
    """
    try:
        pkg_metadata = metadata("{{ cookiecutter.package_name }}")
    except PackageNotFoundError:
        pkg_metadata = {}

    meta: Dict[str, Any] = {
        # Use configured name in case it is dynamically changed.
        "name": config.name,
        # Get metadata from the package configuration
        "version": pkg_metadata.get("Version", "0.0.0"),
        "description": pkg_metadata.get("Summary", None),
        "repository_url": "https://github.com/{{ cookiecutter.github_org }}/{{ cookiecutter.repo_name }}",
        "documentation_url": pkg_metadata.get("Home-page", None),
    }
    app["safir/metadata"] = meta
