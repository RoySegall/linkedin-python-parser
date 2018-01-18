import time
from apistar import Route
from selenium.common.exceptions import NoSuchElementException
from endpoints.BaseRoute import BaseRoute
from models.Profile import Profile
from tools.Selenium import Selenium
from tools.SettingsManager import SettingsManager
from rethinkdb import r


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
            The person object as stored in the DB.
        """
        # Get the tools we need.
        self.selenium = Selenium()

        # Logging in.
        self.login()

        # Pull the details and process them.

        details = self.process_results(self.pull_details(user_id))

        # Close selenium.
        self.selenium.close()

        return details

    def process_results(self, details):
        """
        Processing the fields.

        :param details:
            The object we pulled from the DB.

        :return:
            The details object.
        """
        # Check if the user exists.
        profile = Profile()

        cursor = profile.getTable().filter(r.row['user_id'] == details['user_id']).run(profile.r)

        results = list(cursor)

        if len(results) == 0:
            details = profile.insert(details)
        else:
            details['id'] = results[0]['id']
            profile.update(details)

        return details

    def login(self):
        """
        Connecting to the selenium page.

        :param selenium:
            The selenium object.
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
            The object of the person from linkdein.
        """

        # Specify the list of xpaths.
        xpaths = {
            'name': '//div[contains(@class, "information")]//h1',
            'current_title': '//div[contains(@class, "information")]//h2',
            'current_position': '//div[contains(@class, "section__information")]//div[contains(@class, "experience")]'
                                '//h3[contains(@class, "company")]',
            'summary': '//p[contains(@class, "section__summary-text")]',
            'skills': '//div[@class="pv-skill-entity__header"]',
            'experience': '//section[contains(@class, "experience-section")]//ul'
                          '//li[not(contains(@class, "artdeco-carousel"))]',
            'education': '//section[contains(@class,"pv-profile-section education-section ember-view")]//ul//li',
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

        # First get the associated people. We fire this part since a profile which not look valid may bump into popups
        # that might prevent from selenium to go to the page.
        profile['associated_profiles'] = self.get_associated_profiles()

        # Go back to the of the profile.
        self.selenium.getPage('https://www.linkedin.com/in/' + user_id)
        for key, xpath in xpaths.items():

            if key in special:
                if key == 'skills':
                    profile[key] = self.get_list_of_skills(xpath)

                if key == 'experience':
                    profile[key] = self.get_experience_list(xpath)

                if key == 'education':
                    profile[key] = self.get_education_list(xpath)
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
            The xpath of the list of skills.

        :return:
            The skills list.
        """
        self.selenium.scroll_to_element(xpath)

        time.sleep(10)
        try:
            self.selenium.getElement("//button[@class='pv-profile-section__card-action-bar pv-skills-section__"
                                     "additional-skills artdeco-container-card-action-bar']").click()
        except NoSuchElementException:
            pass

        time.sleep(5)

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

    def get_experience_list(self, xpath):
        """
        Get the list of past jobs.

        :param xpath:
            The xpath for the jobs.

        :return:
            The list of experience.
        """
        number_of_jobs = len(self.selenium.getElements(xpath))

        jobs = []
        for i in range(1, number_of_jobs + 1):
            base_xpath = xpath + "[" + str(i) + "]"
            job = {}

            local_xpaths = {
                'title': '//div[@class="pv-entity__summary-info"]//h3',
                'company': '//div[@class="pv-entity__summary-info"]//span[@class="pv-entity__secondary-title"]',
                'duration': '//div[@class="pv-entity__summary-info"]'
                            '//h4[contains(@class, "pv-entity__date-range")]//span[not(@class="visually-hidden")]',
                'description': '//div[@class="pv-entity__extra-details"]//p',
            }

            for key, local_xpath in local_xpaths.items():
                try:
                    job[key] = self.selenium.getElement(base_xpath + local_xpath).text
                except NoSuchElementException:
                    job[key] = ''

            jobs.append(job)

        return jobs

    def get_education_list(self, xpath):
        """
        Get the list of education list.

        :param xpath:
            The base xpath.

        :return:
            List of institutions.
        """

        self.selenium.scroll_to_element(xpath)
        number_of_educations = len(self.selenium.getElements(xpath))

        institutions = []

        for i in range(1, number_of_educations + 1):
            base_xpath = xpath + "[" + str(i) + "]"

            local_xpaths = {
                'name': '//h3[contains(@class, "pv-entity__school-name")]',
                'degree_name': '//div[@class="pv-entity__degree-info"]'
                               '//p[contains(@class, "pv-entity__degree-name")]//span[not(@class="visually-hidden")]',
                'degree_secondary_title': '//div[@class="pv-entity__degree-info"]'
                                          '//p[contains(@class, "pv-entity__fos")]'
                                          '//span[not(@class="visually-hidden")]',
                'degree_grade': '//div[@class="pv-entity__degree-info"]'
                                '//p[contains(@class, "pv-entity__grade")]'
                                '//span[not(@class="visually-hidden")]',
                'duration': '//p[contains(@class, "pv-entity__dates")]//span[not(@class="visually-hidden")]',
            }

            institution = {}

            for key, local_xpath in local_xpaths.items():
                try:
                    institution[key] = self.selenium.getElement(base_xpath + local_xpath).text
                except NoSuchElementException:
                    institution[key] = ''

            institutions.append(institution)

        return institutions

    def get_associated_profiles(self):
        """
        Get the list of all the associated profile with the account.
        :return:
        """
        connections_link = self.selenium.getElement("//div[contains(@class, 'connections-section')]")

        if not connections_link.is_displayed():
            print('The connections section is blocked or unreachable for now.')
            return {}

        # Go to the page.
        connections_link.click()

        # Waiting for elements to appear.
        time.sleep(5)

        base_xpath = "//div[contains(@class, 'search-results__cluster-content')]//ul[1]//li"

        number_of_connections = len(self.selenium.getElements(base_xpath))
        names = []

        while True:
            for i in range(1, number_of_connections + 1):
                self.selenium.driver.execute_script("window.scrollBy(0, 400);")
                time.sleep(1)
                name_xpath = base_xpath + "[" + str(i) + "]//div[contains(@class, 'search-result__info')]" \
                                                         "//a[contains(@class, 'search-result__result-link')]" \
                                                         "//h3" \
                                                         "//span[@class='name actor-name']"
                try:
                    # Sometimes the element cannot be found but we we won't break the loop for that.
                    names.append(self.selenium.getElement(name_xpath).text)
                except NoSuchElementException:
                    pass

            try:
                self.selenium.getElement('//ol[contains(@class,"results-paginator")]//button[@class="next"]').click()
            except NoSuchElementException:
                # There's no more next button - we got to the end of the list. Breaking the loop.
                break

        return names
