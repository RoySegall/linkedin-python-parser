from selenium import webdriver
from selenium.webdriver.common.by import By


class Selenium(object):
    """
    API for connecting to Selenium.
    """

    # The driver of the firefox.
    driver = {}

    def __init__(self):
        """
        Constructor.

        :return:
        """
        # todo: move to settings
        self.driver = webdriver.Firefox(executable_path=r'/Users/roysegall/geckodriver')

    def close(self):
        self.driver.close()

    def getPage(self, url):
        """
        Get the page for a URL.

        :param url:
            The URL of the page.

        :return:
        """
        self.driver.get(url)
        return self

    def getElement(self, xpath):
        return self.driver.find_element(By.XPATH, xpath)
