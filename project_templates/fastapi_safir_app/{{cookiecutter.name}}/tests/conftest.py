"""Test fixtures for {{ cookiecutter.name }} tests."""

from __future__ import annotations

from collections.abc import AsyncIterator{% if cookiecutter.uws_service == "True" %}, Iterator
from datetime import timedelta
{%- endif %}

{% if cookiecutter.uws_service == "True" -%}
import pytest
{% endif -%}
import pytest_asyncio
{%- if cookiecutter.uws_service == "True" %}
import structlog
{%- endif %}
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
{%- if cookiecutter.uws_service == "True" %}
from safir.arq import MockArqQueue
from safir.testing.gcs import MockStorageClient, patch_google_storage
from safir.testing.uws import MockUWSJobRunner
{%- endif %}

from {{ cookiecutter.module_name }} import main
{%- if cookiecutter.uws_service == "True" %}
from {{ cookiecutter.module_name }}.config import config, uws
{%- endif %}


@pytest_asyncio.fixture
{%- if cookiecutter.uws_service == "True" %}
async def app(arq_queue: MockArqQueue) -> AsyncIterator[FastAPI]:
{%- else %}
async def app() -> AsyncIterator[FastAPI]:
{%- endif %}
    """Return a configured test application.

    Wraps the application in a lifespan manager so that startup and shutdown
    events are sent during test execution.
    """
    {%- if cookiecutter.uws_service == "True" %}
    logger = structlog.get_logger("{{ cookiecutter.module_name }}")
    await uws.initialize_uws_database(logger, reset=True)
    uws.override_arq_queue(arq_queue)
    {%- endif %}
    async with LifespanManager(main.app):
        yield main.app
{%- if cookiecutter.uws_service == "True" %}


@pytest.fixture
def arq_queue() -> MockArqQueue:
    return MockArqQueue()
{%- endif %}


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    """Return an ``httpx.AsyncClient`` configured to talk to the test app."""
    async with AsyncClient(
        transport=ASGITransport(app=app),  # type: ignore[arg-type]
        base_url="https://example.com/",
    ) as client:
        yield client
{%- if cookiecutter.uws_service == "True" %}


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
{%- endif %}
