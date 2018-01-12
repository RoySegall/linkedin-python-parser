from apistar import Include, Route
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
from endpoints.ScrapeRoute import ScrapeRoute
from endpoints.SearchRoute import SearchRoute
from endpoints.SkillsAndAssociatedPeopleRoute import SkillsAndAssociatedPeopleRoute


routes = [
    Include('/scrape', ScrapeRoute().Routes()),
    Include('/search', SearchRoute().Routes()),
    Include('/search-skills', SkillsAndAssociatedPeopleRoute().Routes()),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]

app = App(routes=routes)


if __name__ == '__main__':
    app.main()
