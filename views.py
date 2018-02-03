from sanic import Sanic
from sanic import response
from mako.template import Template
import peewee
import trafaret as t
from storage import Repo, Subscriber
from utils import cities

tpl = mytemplate = Template(filename='tpl/hello.mako')


def views(app: Sanic) -> Sanic:
    @app.route("/", methods=['GET'])
    async def index(request):
        return response.html(
            tpl.render(cities=cities, errors=[], created=Flase))

    @app.route("/subscirbe", methods=['POST'])
    async def subscirbe(request):
        schema = t.Dict(email=t.Email, location=t.String)
        errors = []
        try:
            data = schema.check(request.form)
        except t.DataError as e:
            errors.append(str(e))
        try:
            await Repo.create(Subscriber, **data)
        except peewee.OperationalError:
            errors.append('Email is already used')
        return response.html(
            tpl.render(cities=cities, errors=errorsб created=not errors),
            status=201 if not errors else 200)

    @app.route("/v1/ping", methods=['GET'])
    async def ping(request):
        return response.json({"pong": True})

    @app.route("/v1/ping_db", methods=['GET'])
    async def ping_db(request):
        all_objects = await Repo.execute(Subscriber.select())
        print(all_objects)
        return response.json({"pong": True})

    return app
