from apistar import Include, Route
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
from models import Profile
from werkzeug.debug.repr import dump
import remodel.connection


# todo: move to json file.
remodel.connection.pool.configure(db="linkedin")


def upload():
    my_order = Profile.Profile.create(customer='Andrei', shop='GitHub')
    dump(my_order)


routes = [
    Route('/search', 'GET', upload),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]

app = App(routes=routes)


if __name__ == '__main__':
    app.main()
