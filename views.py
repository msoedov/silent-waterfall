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
        schema = t.Dict({
            t.Key('email'): t.Email,
            t.Key('location', to_name='city'): t.String
        })
        errors = []
        try:
            data = schema.check(request.form)
        except t.DataError as e:
            errors.append(str(e))

        data['state'] = [
            c['state'] for c in cities if c['city'] == data['city']
        ][0]
        try:
            await Repo.create(Subscriber, **data)
        except peewee.IntegrityError:
            errors.append('Email is already used')
        return response.html(
            tpl.render(cities=cities, errors=errors, created=not errors),
            status=201 if not errors else 200)

    @app.route("/v1/ping", methods=['GET'])
    async def ping(request):
        return response.json({"pong": True})

    return app
