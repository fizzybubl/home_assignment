import time
from pathlib import Path

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.select import Select

from config import ROOT_PATH
from drivers.custom_web_element import CustomWebElement
from drivers.types import LocatorType
from drivers.waiters.element_waiters import wait_for_element_to_be_clickable

_driver_executable = "chromedriver.exe"


CHROME_PATH = Path(ROOT_PATH, Path(__file__).parent, "executable", _driver_executable).resolve()


class CustomChromeDriver(WebDriver):

    def __init__(self, options: ChromeOptions = None, service: ChromeService = None, keep_alive: bool = True):
        super().__init__(options=options,
                         service=service,
                         keep_alive=keep_alive)

    def go_to_url(self, url: str):
        self.get(url)

    def get_element(self, locator: LocatorType) -> CustomWebElement:
        return CustomWebElement(self.find_element(*locator))

    def list_elements(self, locator: LocatorType) -> list[CustomWebElement]:
        return [CustomWebElement(web_element) for web_element in self.find_elements(*locator)]

    def click_element(self, locator: LocatorType):
        wait_for_element_to_be_clickable(self, *locator).click()

    def move_to_element(self, locator: LocatorType | CustomWebElement):
        if isinstance(locator, CustomWebElement):
            ActionChains(self).move_to_element(locator).perform()
        else:
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


def chrome_options():
    options = ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("incognito")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    return options


def chrome_service():
    return ChromeService(CHROME_PATH)


def chrome_driver(options: ChromeOptions = None, service: ChromeService = None, keep_alive: bool = True):
    driver = CustomChromeDriver(options, service, keep_alive)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver
