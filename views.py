from sanic import Sanic
from sanic import response
from mako.template import Template
import trafaret as t
from storage import Repo, Subscriber

tpl = mytemplate = Template(filename='tpl/hello.mako')


def views(app: Sanic) -> Sanic:
    @app.route("/", methods=['GET'])
    async def index(request):
        return response.html(tpl.render(cities=[], errors=[]))

    @app.route("/subscirbe", methods=['POST'])
    async def subscirbe(request):
        print(request.form)
        schema = t.Dict(email=t.Email, location=t.String)
        errors = []
        try:
            schema.check(request.form)
        except t.DataError as e:
            errors.append(str(e))
        return response.html(tpl.render(cities=[], errors=errors))

    @app.route("/v1/ping", methods=['GET'])
    async def ping(request):
        return response.json({"pong": True})

    @app.route("/v1/ping_db", methods=['GET'])
    async def ping_db(request):
        all_objects = await Repo.execute(Subscriber.select())
        print(all_objects)
        return response.json({"pong": True})

    return app
