from apistar import Route

from endpoints.BaseRoute import BaseRoute
from models.Profile import Profile
from tools.Selenium import Selenium


class ScrapeRoute(BaseRoute):
    """
    This is the route for scraping the linked in profile.
    """

    def Routes(self):
        return [
            Route('/', 'POST', self.scrape_post),
        ]

    def scrape_post(self):
        """
        Scrape a user profile.

        :return:
        """
        # Login to selenium.

        # Go to a profile page.

        # Pull the details.
        details = self.pull_details()

        # Check if the user exists.
        profile = Profile()

        if 1 == 1:
            profile.insert({})
        else:
            profile.update({})

        # Print the user object.
        return {}
        # selenium = Selenium()
        # page = selenium.getPage('http://www.mako.co.il/news-israel/education-q1_2018/Article-fbb189d572ae061004.htm'
        #                         '?sCh=3d385dd2dd5d4110&pId=1898243326')
        # text = page.getElement("//h1").text
        # selenium.close()
        # return {'text': text}

    def pull_details(self):
        return {}
