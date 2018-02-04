import app as App
import pytest


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


async def test_db(test_cli):
    """
    GET request
    """
    resp = await test_cli.get('/v1/ping_db')
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


# async def test_fixture_test_client_put(test_cli):
#     """
#     PUT request
#     """
#     resp = await test_cli.put('/test_put')
#     assert resp.status == 200
#     resp_json = await resp.json()
#     assert resp_json == {"PUT": True}

# async def test_fixture_test_client_delete(test_cli):
#     """
#     DELETE request
#     """
#     resp = await test_cli.delete('/test_delete')
#     assert resp.status == 200
#     resp_json = await resp.json()
#     assert resp_json == {"DELETE": True}

# async def test_fixture_test_client_patch(test_cli):
#     """
#     PATCH request
#     """
#     resp = await test_cli.patch('/test_patch')
#     assert resp.status == 200
#     resp_json = await resp.json()
#     assert resp_json == {"PATCH": True}

# async def test_fixture_test_client_options(test_cli):
#     """
#     OPTIONS request
#     """
#     resp = await test_cli.options('/test_options')
#     assert resp.status == 200
#     resp_json = await resp.json()
#     assert resp_json == {"OPTIONS": True}

# async def test_fixture_test_client_head(test_cli):
#     """
#     HEAD request
#     """
#     resp = await test_cli.head('/test_head')
#     assert resp.status == 200
#     resp_json = await resp.json()
#     # HEAD should not have body
#     assert resp_json is None

# async def test_fixture_test_client_ws(test_cli):
#     """
#     Websockets
#     """
#     ws_conn = await test_cli.ws_connect('/test_ws')
#     data = 'hello world!'
#     await ws_conn.send_str(data)
#     msg = await ws_conn.receive()
#     assert msg.data == data
#     await ws_conn.close()
