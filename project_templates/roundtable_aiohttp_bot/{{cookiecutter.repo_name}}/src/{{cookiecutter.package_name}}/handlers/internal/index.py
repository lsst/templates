"""Handlers for the app's root, ``/``.
"""

__all__ = ["get_index"]

from aiohttp import web

from {{ cookiecutter.package_name }}.handlers import internal_routes


@internal_routes.get("/")
async def get_index(request: web.Request) -> web.Response:
    """GET / (the app's internal root).

    By convention, this endpoint returns only the application's metadata.
    """
    metadata = request.config_dict["safir/metadata"]

    return web.json_response(metadata)
