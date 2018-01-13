from selenium import webdriver
from selenium.webdriver.common.by import By
from tools.SettingsManager import SettingsManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


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

    def getElement(self, xpath):
        return self.driver.find_element(By.XPATH, xpath)

    def getElements(self, xpath):
        return self.driver.find_elements(By.XPATH, xpath)
