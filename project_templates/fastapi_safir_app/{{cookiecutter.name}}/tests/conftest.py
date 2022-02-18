"""Test fixtures for {{ cookiecutter.name }} tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from {{ cookiecutter.package_name }} import main

if TYPE_CHECKING:
    from typing import AsyncIterator

    from fastapi import FastAPI


@pytest_asyncio.fixture
async def app() -> AsyncIterator[FastAPI]:
    """Return a configured test application.

    Wraps the application in a lifespan manager so that startup and shutdown
    events are sent during test execution.
    """
    async with LifespanManager(main.app):
        yield main.app


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    """Return an ``httpx.AsyncClient`` configured to talk to the test app."""
    async with AsyncClient(app=app, base_url="https://example.com/") as client:
        yield client
