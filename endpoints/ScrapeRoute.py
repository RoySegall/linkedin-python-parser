import time
from apistar import Route, Response
from endpoints.BaseRoute import BaseRoute
from models.Profile import Profile
from tools.Selenium import Selenium
from tools.SettingsManager import SettingsManager


class ScrapeRoute(BaseRoute):
    """
    This is the route for scraping the linked in profile.
    """

    def Routes(self):
        return [
            Route('/', 'post', self.scrape_post),
        ]

    def scrape_post(self):
        """
        Scrape a user profile.

        :return:
        """
        # Get the tools we need.
        selenium = Selenium()
        settings = SettingsManager().loadSettings()

        # Login using selenium.
        selenium.getPage('https://www.linkedin.com/uas/login?formSignIn=true'
                         '&session_redirect=%2Fvoyager%2FloginRedirect.html'
                         '&one_time_redirect=https%3A%2F%2Fwww.linkedin.com%2Fm%2Flogin%2F')

        selenium.getElement('//a[@class="sign-in-link"]').click()
        selenium.getElement('//input[@id="session_key-login"]').send_keys(settings['linkedin']['username'])
        selenium.getElement('//input[@id="session_password-login"]').send_keys(settings['linkedin']['password'])
        selenium.getElement('//form[@id="login"]//input[@type="submit"]').click()

        # Waiting for a couple of seconds. Looks that Linkedin has some kind of scraping protection.
        time.sleep(10)
        selenium.getPage('https://www.linkedin.com/')

        # Go to the page we need to scrape.
        selenium.getPage()
        return

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
        # page = selenium.getPage('http://www.mako.co.il/news-israel/education-q1_2018/Article-fbb189d572ae061004.htm'
        #                         '?sCh=3d385dd2dd5d4110&pId=1898243326')
        # text = page.getElement("//h1").text
        # selenium.close()
        # return {'text': text}

    def pull_details(self):
        return {}
