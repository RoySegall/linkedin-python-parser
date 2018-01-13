import time

from apistar import Route
from selenium.common.exceptions import NoSuchElementException

from endpoints.BaseRoute import BaseRoute
from models.Profile import Profile
from tools.Selenium import Selenium
from tools.SettingsManager import SettingsManager


class ScrapeRoute(BaseRoute):
    """
    This is the route for scraping the linked in profile.
    """

    # The selenium object.
    selenium = {}

    def Routes(self):
        return [
            Route('/{user_id}', 'get', self.scrape_post),
        ]

    def scrape_post(self, user_id):
        """
        Scrape a user profile.

        :return:
        """
        # Get the tools we need.
        self.selenium = Selenium()

        # Logging in.
        self.login()

        # Pull the details.
        details = self.pull_details(user_id)

        return details

        # Check if the user exists.
        profile = Profile()

        if 1 == 1:
            profile.insert({})
        else:
            profile.update({})

        # Print the user object.
        return {}
        # selenium.close()
        # return {'text': text}

    def login(self):
        """
        Connecting to the selenium page.

        :param selenium:
            The selenium object.

        :return:
        """
        settings = SettingsManager().loadSettings()

        # Login using selenium.
        self.selenium.getPage('https://www.linkedin.com/uas/login?formSignIn=true'
                              '&session_redirect=%2Fvoyager%2FloginRedirect.html'
                              '&one_time_redirect=https%3A%2F%2Fwww.linkedin.com%2Fm%2Flogin%2F')

        self.selenium.getElement('//a[@class="sign-in-link"]').click()
        self.selenium.getElement('//input[@id="session_key-login"]').send_keys(settings['linkedin']['username'])
        self.selenium.getElement('//input[@id="session_password-login"]').send_keys(settings['linkedin']['password'])
        self.selenium.getElement('//form[@id="login"]//input[@type="submit"]').click()

        # Waiting for a couple of seconds. Looks that Linkedin has some kind of scraping protection.
        time.sleep(5)
        self.selenium.getPage('https://www.linkedin.com/')

    def pull_details(self, user_id):
        """
        Extract the details of the user profile.

        :param selenium:
            The selenium object. We need that in order to scrape the user details.

        :return:
        """
        # Specify the list of xpaths.
        xpaths = {
            'name': '//div[contains(@class, "information")]//h1',
            'current_title': '//div[contains(@class, "information")]//h2',
            'current_position': '//div[contains(@class, "section__information")]//div[contains(@class, "experience")]'
                                '//h3[contains(@class, "company")]',
            'summary': '//p[contains(@class, "section__summary-text")]',
            'skills': '//div[@class="pv-skill-entity__header"]',
            # 'experience': '//section[contains(@class, "background-section")]'
            #               '//section[contains(@class, "pv-profile-section experience-section")]',
            # 'education': '//ul[@class="pv-profile-section__section-info section-info pv-profile-section__'
            #              'section-info--has-no-more ember-view"]',
        }

        #  Specify what is a special element so we could now how to handle it.
        special = ['skills', 'experience', 'education']

        # Ini the profile object with the user ID.
        profile = {
            'user_id': user_id,
        }

        # Go to the page we need to scrape - profile page.
        self.selenium.getPage('https://www.linkedin.com/in/' + user_id)
        time.sleep(5)

        for key, xpath in xpaths.items():

            if key in special:
                if key == 'skills':
                    profile[key] = self.get_list_of_skills(xpath)
            else:
                try:
                    element = self.selenium.getElement(xpath)
                except NoSuchElementException:
                    print("An error with the element " + xpath)
                    continue
                profile[key] = element.text

        return profile

    def get_list_of_skills(self, xpath):
        """
        We need to expand the list of skills.
        :param xpath:
        :return:
        """
        i = 0
        while True:
            i = i + 1
            if i > 200:
                # We still got a limit if the element was not found.
                return {}

            try:
                self.selenium.getElement(xpath)
                break
            except NoSuchElementException:
                self.selenium.driver.execute_script("window.scrollBy(0, 400);")

        # Todo: check if the button exists.
        self.selenium.getElement("//button[@class='pv-profile-section__card-action-bar pv-skills-section__"
                                 "additional-skills artdeco-container-card-action-bar']").click()

        # Get all the list.
        skills = []

        # Don't know why we don't have the index.
        i = 1
        for item in self.selenium.getElements(xpath):
            skill = item.find_element_by_xpath(
                "(//span[contains(@class, 'pv-skill-entity__skill-name')])[" + str(i) + "]"
            ).text
            try:
                rank = item.find_element_by_xpath(
                    "(//span[contains(@class, 'pv-skill-entity__endorsement-count')])[" + str(i) + "]"
                ).text
            except NoSuchElementException:
                rank = 0

            data = {'skill': skill, 'rank': rank}
            i = i + 1

            skills.append(data)

        return skills
