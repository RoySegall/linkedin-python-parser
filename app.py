from apistar import Include, Route
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
from tools.Selenium import Selenium


def upload():
    selenium = Selenium()
    page = selenium.getPage('http://www.mako.co.il/news-israel/education-q1_2018/Article-fbb189d572ae061004.htm'
                            '?sCh=3d385dd2dd5d4110&pId=1898243326')
    text = page.getElement("//h1").text
    selenium.close()
    return {'text': text}


routes = [
    Route('/search', 'GET', upload),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]

app = App(routes=routes)


if __name__ == '__main__':
    app.main()
