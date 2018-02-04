import pytest

import app as App


@pytest.yield_fixture
def app():
    yield App.new_app()


@pytest.fixture
def test_cli(loop, app, test_client):
    return loop.run_until_complete(test_client(app))


async def test_404(test_cli):
    """
    GET request
    """
    resp = await test_cli.get('/404')
    assert resp.status == 404
    resp_json = await resp.json()
    assert resp_json.get('msg') == "Yep, I totally found the page"


async def test_ping(test_cli):
    """
    GET request
    """
    resp = await test_cli.get('/v1/ping')
    assert resp.status == 200
    resp_json = await resp.json()
    assert resp_json == {"pong": True}


async def test_main(test_cli):
    """
    GET request
    """
    resp = await test_cli.get('/')
    assert resp.status == 200


async def test_subscribe(test_cli):
    resp = await test_cli.post(
        '/subscirbe',
        data=dict(email="elon.musk@gmail.com", location="Boston"))
    assert resp.status == 201
