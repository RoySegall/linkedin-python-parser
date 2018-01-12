from apistar import Route

from endpoints.BaseRoute import BaseRoute
from tools.Selenium import Selenium


class ScrapeRoute(BaseRoute):
    """
    This is the route for scraping the linked in profile.
    """

    def Routes(self):
        return [
            Route('/', 'GET', self.scrapeGet),
            Route('/', 'POST', self.scrapePost),
            Route('/', 'PATCH', self.scrapePatch),
            Route('/', 'DELETE', self.scrapeDelete),
        ]

    def scrapeGet(self):
        selenium = Selenium()
        page = selenium.getPage('http://www.mako.co.il/news-israel/education-q1_2018/Article-fbb189d572ae061004.htm'
                                '?sCh=3d385dd2dd5d4110&pId=1898243326')
        text = page.getElement("//h1").text
        selenium.close()
        return {'text': text}

    def scrapePost(self):
        return {}

    def scrapePatch(self):
        return {}

    def scrapeDelete(self):
        return {}
