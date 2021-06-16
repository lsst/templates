"""Tests for the {{ cookiecutter.package_name }}.handlers.external module and routes."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from {{ cookiecutter.package_name }}.config import config

if TYPE_CHECKING:
    from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_index(client: AsyncClient) -> None:
    """Test ``GET /{{ cookiecutter.package_name }}/``"""
    response = await client.get("/{{ cookiecutter.package_name }}/")
    assert response.status_code == 200
    data = response.json()
    metadata = data["metadata"]
    assert metadata["name"] == config.name
    assert isinstance(metadata["version"], str)
    assert isinstance(metadata["description"], str)
    assert isinstance(metadata["repository_url"], str)
    assert isinstance(metadata["documentation_url"], str)
