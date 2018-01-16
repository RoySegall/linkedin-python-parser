from apistar import Include, Route
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
from endpoints.ScrapeRoute import ScrapeRoute
from endpoints.SearchBySkillsRoute import SearchBySkillsRoute
from endpoints.SearchByNameRoute import SearchByNameRoute


routes = [
    Include('/scrape', ScrapeRoute().Routes()),
    Include('/search-by-name', SearchByNameRoute().Routes()),
    Include('/search-by-skills', SearchBySkillsRoute().Routes()),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]

app = App(routes=routes)


if __name__ == '__main__':
    app.main()
