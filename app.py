from apistar import Include, Route
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
from werkzeug.debug.repr import dump

from models.Profile import Profile


def upload():
    profile = Profile()
    print(profile.tableExists())
    return {}


routes = [
    Route('/search', 'GET', upload),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]

app = App(routes=routes)


if __name__ == '__main__':
    app.main()
