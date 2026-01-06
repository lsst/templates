"""Test fixtures for example-uws tests."""

from collections.abc import AsyncGenerator, Iterator
from datetime import timedelta

import pytest
import pytest_asyncio
import structlog
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from safir.arq import MockArqQueue
from safir.testing.gcs import MockStorageClient, patch_google_storage
from safir.testing.uws import MockUWSJobRunner

from exampleuws import main
from exampleuws.config import config, uws


@pytest_asyncio.fixture
async def app(arq_queue: MockArqQueue) -> AsyncGenerator[FastAPI]:
    """Return a configured test application.

    Wraps the application in a lifespan manager so that startup and shutdown
    events are sent during test execution.
    """
    uws.override_arq_queue(arq_queue)
    async with LifespanManager(main.app):
        yield main.app


@pytest.fixture
def arq_queue() -> MockArqQueue:
    return MockArqQueue()


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient]:
    """Return an ``httpx.AsyncClient`` configured to talk to the test app."""
    async with AsyncClient(
        base_url="https://example.com/", transport=ASGITransport(app=app)
    ) as client:
        yield client


@pytest.fixture(autouse=True)
def mock_google_storage() -> Iterator[MockStorageClient]:
    yield from patch_google_storage(
        expected_expiration=timedelta(minutes=15), bucket_name="some-bucket"
    )


@pytest_asyncio.fixture
async def runner(arq_queue: MockArqQueue) -> MockUWSJobRunner:
    return MockUWSJobRunner(config.uws_config, arq_queue)
