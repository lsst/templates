"""Tests for the {{ cookiecutter.module_name }}.handlers.internal module and routes."""

from __future__ import annotations

import pytest
from httpx import AsyncClient

from {{ cookiecutter.module_name }}.config import config


@pytest.mark.asyncio
async def test_get_index(client: AsyncClient) -> None:
    """Test ``GET /``"""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == config.name
    assert isinstance(data["version"], str)
    assert isinstance(data["description"], str)
    assert isinstance(data["repository_url"], str)
    assert isinstance(data["documentation_url"], str)
