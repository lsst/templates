"""Tests for the {{ cookiecutter.package_name }}.handlers.external.index module and routes."""

from __future__ import annotations

from typing import TYPE_CHECKING

from {{ cookiecutter.package_name }}.app import create_app

if TYPE_CHECKING:
    from aiohttp.pytest_plugin.test_utils import TestClient


async def test_get_index(aiohttp_client: TestClient) -> None:
    """Test GET /app-name/"""
    app = create_app()
    name = app["safir/config"].name
    client = await aiohttp_client(app)

    response = await client.get(f"/{name}/")
    assert response.status == 200
    data = await response.json()
    metadata = data["_metadata"]
    assert metadata["name"] == name
    assert isinstance(metadata["version"], str)
    assert isinstance(metadata["description"], str)
    assert isinstance(metadata["repository_url"], str)
    assert isinstance(metadata["documentation_url"], str)
