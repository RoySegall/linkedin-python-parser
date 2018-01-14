from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
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

    def scroll_to_element(self, xpath, attempts=200):
        i = 0
        while True:
            i = i + 1
            if i > attempts:
                # We still got a limit if the element was not found.
                return {}

            try:
                if self.getElement(xpath).is_displayed():
                    break
            except NoSuchElementException:
                self.driver.execute_script("window.scrollBy(0, 400);")
