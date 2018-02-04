from os.path import abspath, dirname, join

from sanic import Sanic
from sanic.config import LOGGING
from sanic.exceptions import NotFound, RequestTimeout, ServerError

from checkr import schedule_coro
from exception_handlers import handle_404s, handle_500s, handle_timeout
from views import views


def new_app() -> Sanic:
    app = Sanic()
    app = annotate_error_handling(app)
    app = views(app)
    return app


def annotate_error_handling(app: Sanic) -> Sanic:
    app.error_handler.add(ServerError, handle_500s)
    app.error_handler.add(NotFound, handle_404s)
    app.error_handler.add(RequestTimeout, handle_timeout)
    return app


def main():
    app = new_app()
    app.run()


if __name__ == '__main__':
    schedule_coro()
    main()
