"""Test fixtures for example-uws tests."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
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
async def app(arq_queue: MockArqQueue) -> AsyncIterator[FastAPI]:
    """Return a configured test application.

    Wraps the application in a lifespan manager so that startup and shutdown
    events are sent during test execution.
    """
    logger = structlog.get_logger("exampleuws")
    await uws.initialize_uws_database(logger, reset=True)
    uws.override_arq_queue(arq_queue)
    async with LifespanManager(main.app):
        yield main.app


@pytest.fixture
def arq_queue() -> MockArqQueue:
    return MockArqQueue()


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    """Return an ``httpx.AsyncClient`` configured to talk to the test app."""
    async with AsyncClient(
        transport=ASGITransport(app=app),  # type: ignore[arg-type]
        base_url="https://example.com/",
    ) as client:
        yield client


@pytest.fixture(autouse=True)
def mock_google_storage() -> Iterator[MockStorageClient]:
    yield from patch_google_storage(
        expected_expiration=timedelta(minutes=15), bucket_name="some-bucket"
    )


@pytest_asyncio.fixture
async def runner(
    arq_queue: MockArqQueue,
) -> AsyncIterator[MockUWSJobRunner]:
    async with MockUWSJobRunner(config.uws_config, arq_queue) as runner:
        yield runner
