"""Test fixtures for {{ cookiecutter.name }} tests."""

from collections.abc import AsyncGenerator{% if cookiecutter.flavor == "UWS" %}, Iterator
from datetime import timedelta
{%- endif %}

{% if cookiecutter.flavor == "UWS" -%}
import pytest
{% endif -%}
import pytest_asyncio
{%- if cookiecutter.flavor == "UWS" %}
import structlog
{%- endif %}
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
{%- if cookiecutter.flavor == "UWS" %}
from safir.arq import MockArqQueue
from safir.testing.gcs import MockStorageClient, patch_google_storage
from safir.testing.uws import MockUWSJobRunner
{%- endif %}

from {{ cookiecutter.module_name }} import main
{%- if cookiecutter.flavor == "UWS" %}
from {{ cookiecutter.module_name }}.config import config, uws
{%- endif %}


@pytest_asyncio.fixture
{%- if cookiecutter.flavor == "UWS" %}
async def app(arq_queue: MockArqQueue) -> AsyncGenerator[FastAPI]:
{%- else %}
async def app() -> AsyncGenerator[FastAPI]:
{%- endif %}
    """Return a configured test application.

    Wraps the application in a lifespan manager so that startup and shutdown
    events are sent during test execution.
    """
    {%- if cookiecutter.flavor == "UWS" %}
    uws.override_arq_queue(arq_queue)
    {%- endif %}
    async with LifespanManager(main.app):
        yield main.app
{%- if cookiecutter.flavor == "UWS" %}


@pytest.fixture
def arq_queue() -> MockArqQueue:
    return MockArqQueue()
{%- endif %}


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient]:
    """Return an ``httpx.AsyncClient`` configured to talk to the test app."""
    async with AsyncClient(
        base_url="https://example.com/", transport=ASGITransport(app=app)
    ) as client:
        yield client
{%- if cookiecutter.flavor == "UWS" %}


@pytest.fixture(autouse=True)
def mock_google_storage() -> Iterator[MockStorageClient]:
    yield from patch_google_storage(
        expected_expiration=timedelta(minutes=15), bucket_name="some-bucket"
    )


@pytest_asyncio.fixture
async def runner(arq_queue: MockArqQueue) -> MockUWSJobRunner:
    return MockUWSJobRunner(config.uws_config, arq_queue)
{%- endif %}
