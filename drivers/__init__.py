import os
from contextlib import contextmanager
from typing import Literal

from drivers.chrome.driver import CustomChromeDriver, ChromeOptions, ChromeService, chrome_options, \
    chrome_service, chrome_driver
from drivers.firefox.driver import CustomFirefoxDriver, FirefoxOptions, FirefoxService, \
    firefox_options, firefox_service, firefox_driver

WebDriverType = CustomChromeDriver | CustomFirefoxDriver
_Options = ChromeOptions | FirefoxOptions
_Service = ChromeService | FirefoxService
_DriverType = Literal["chrome", "firefox"]


class DriverType:
    CHROME = "chrome"
    FIREFOX = "firefox"


def get_options():
    if os.getenv("BROWSER") == DriverType.FIREFOX:
        return firefox_options()
    elif os.getenv("BROWSER") == DriverType.CHROME:
        return chrome_options()


def get_service():
    if os.getenv("BROWSER") == DriverType.FIREFOX:
        return firefox_service()
    elif os.getenv("BROWSER") == DriverType.CHROME:
        return chrome_service()


@contextmanager
def webdriver_factory(*, driver_type: _DriverType = os.getenv("BROWSER"),
                      service: _Service = get_service(),
                      options: _Options = get_options()):
    driver = None
    try:
        if driver_type == DriverType.CHROME:
            driver = chrome_driver(options, service)

        if driver_type == DriverType.FIREFOX:
            driver = firefox_driver(options, service)
        yield driver
    finally:
        if driver:
            driver.quit()
