"""HTTP API route tables."""

__all__ = ["internal_routes", "routes", "init_internal_routes"]

from aiohttp import web

internal_routes = web.RouteTableDef()
"""Routes for the root application that serves from ``/``

Application-specific routes don't get attached here. In practice, only routes
for metrics and health checks get attached to this table. Attach public APIs
to `routes` instead since those are accessible from the public API gateway and
are prefixed with the application name.
"""

routes = web.RouteTableDef()
"""Routes for the public API that serves from ``/<api_name>/``."""


def init_external_routes() -> web.RouteTableDef:
    """Initialize the route table and handlers from the application APIs,
    served at ``/<api_name>/``.
    """
    # Import handlers so that they are registered with the routes table via
    # decorators. This isn't a global import to avoid circular dependencies.
    import {{ cookiecutter.package_name }}.handlers.external  # noqa: F401

    return routes


def init_internal_routes() -> web.RouteTableDef:
    """Initialize the route table and handlers for the root APIs (not the
    ones publicly available).
    """
    # Import handlers so that they are registered with the routes table via
    # decorators. This isn't a global import to avoid circular dependencies.
    import {{ cookiecutter.package_name }}.handlers.internal  # noqa: F401

    return internal_routes
