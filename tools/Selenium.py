from selenium import webdriver
from selenium.webdriver.common.by import By
from tools.SettingsManager import SettingsManager


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
        self.driver = webdriver.Firefox(executable_path=SettingsManager().loadSettings()['gecko'])

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
