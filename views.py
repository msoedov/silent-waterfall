from sanic import Sanic
from sanic import response
import trafaret as t
from storage import Repo, Subscriber


def views(app: Sanic) -> Sanic:
    @app.route("/v1/ping", methods=['GET'])
    async def ping(request):
        return response.json({"pong": True})

    @app.route("/v1/ping_db", methods=['GET'])
    async def ping_db(request):
        all_objects = await Repo.execute(Subscriber.select())
        print(all_objects)
        return response.json({"pong": True})

    return app
