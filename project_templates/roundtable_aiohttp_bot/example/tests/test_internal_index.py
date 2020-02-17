"""Tests for the example.handlers.internal.index module and routes.
"""

from example.app import create_app


async def test_get_index(aiohttp_client):
    """Test GET /
    """
    app = create_app()
    client = await aiohttp_client(app)

    response = await client.get("/")
    assert response.status == 200
    data = await response.json()
    assert data['name'] == app['safir/config'].name
    assert isinstance(data['version'], str)
    assert isinstance(data['description'], str)
    assert isinstance(data['repository_url'], str)
    assert isinstance(data['documentation_url'], str)
