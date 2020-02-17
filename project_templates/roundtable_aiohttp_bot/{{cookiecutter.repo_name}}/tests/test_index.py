"""Tests for the {{ cookiecutter.package_name }}.handlers.external.index module and routes.
"""

from {{ cookiecutter.package_name }}.app import create_app


async def test_get_index(aiohttp_client):
    """Test GET /app-name/
    """
    app = create_app()
    name = app['safir/config'].name
    client = await aiohttp_client(app)

    response = await client.get(f"/{name}/")
    assert response.status == 200
    data = await response.json()
    metadata = data['_metadata']
    assert metadata['name'] == name
    assert isinstance(metadata['version'], str)
    assert isinstance(metadata['description'], str)
    assert isinstance(metadata['repository_url'], str)
    assert isinstance(metadata['documentation_url'], str)
