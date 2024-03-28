import time
from typing import Self

from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from drivers.types import LocatorType
from drivers.waiters.element_waiters import wait_for_element_to_be_clickable


class CustomWebElement(WebElement):
    """Base HTML Element."""

    def __init__(self, web_element: WebElement):
        super().__init__(web_element.parent, web_element.id)

    def get_element(self, locator: LocatorType) -> Self:
        return self._new(self.find_element(*locator))

    def list_elements(self, locator: LocatorType) -> list[Self]:
        return [self._new(web_element) for web_element in self.find_elements(*locator)]

    def click_element(self, locator: LocatorType):
        wait_for_element_to_be_clickable(self, *locator).click()

    def write_text(self, locator: LocatorType, text: str, delay: float = 0.05):
        """Method used to write text in text fields."""
        element = self.get_element(*locator)
        if not delay:
            element.send_keys(text)
        else:
            for key in text:
                element.send_keys(key)
                time.sleep(delay)

    @classmethod
    def _new(cls, element: WebElement):
        return cls(element)
