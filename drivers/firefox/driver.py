import time
from pathlib import Path

from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.select import Select

from config import ROOT_PATH
from drivers.custom_web_element import CustomWebElement
from drivers.types import LocatorType
from drivers.waiters.element_waiters import wait_for_element_to_be_visible, \
    wait_for_element_to_be_clickable

_driver_executable = "geckodriver.exe"


GECKO_PATH = Path(ROOT_PATH, Path(__file__).parent, "executable", _driver_executable).resolve()


class CustomFirefoxDriver(WebDriver):

    def __init__(self, options: FirefoxOptions = None, service: FirefoxService = None, keep_alive: bool = True):
        super().__init__(options=options,
                         service=service,
                         keep_alive=keep_alive)

    def go_to_url(self, url: str):
        self.get(url)

    def get_element(self, locator: LocatorType) -> CustomWebElement:
        wait_for_element_to_be_visible(self, *locator)
        return CustomWebElement(self.find_element(*locator))

    def list_elements(self, locator: LocatorType) -> list[CustomWebElement]:
        wait_for_element_to_be_visible(self, *locator)
        return [CustomWebElement(web_element) for web_element in self.find_elements(*locator)]

    def click_element(self, locator: LocatorType):
        wait_for_element_to_be_clickable(self, *locator).click()

    def move_to_element(self, locator: LocatorType):
        ActionChains(self).move_to_element(self.get_element(locator)).perform()

    def write_text(self, locator: LocatorType, text: str, delay: float = 0.05):
        """Method used to write text in text fields."""
        element = self.get_element(*locator)
        if not delay:
            element.send_keys(text)
        else:
            for key in text:
                element.send_keys(key)
                time.sleep(delay)

    def select_option_from_dropdown(self, locator: LocatorType, option: str):
        Select(self.get_element(locator)).select_by_value(option)


def firefox_profile():
    profile = FirefoxProfile()
    profile.set_preference("dom.webdriver.enabled", False)
    profile.set_preference('useAutomationExtension', False)
    profile.update_preferences()
    return profile


def firefox_options(profile: FirefoxProfile = firefox_profile()):
    options = FirefoxOptions()
    options.add_argument("--ignore-certificate-errors")
    options.profile = profile
    return options


def firefox_service():
    return FirefoxService(GECKO_PATH)


def firefox_driver(options: FirefoxOptions = None, service: FirefoxService = None, keep_alive: bool = True):
    driver = CustomFirefoxDriver(options, service, keep_alive)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.maximize_window()
    return driver
