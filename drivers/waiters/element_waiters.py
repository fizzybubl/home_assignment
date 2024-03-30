import time

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from drivers.types import ByType


# TODO: Improve waiters to that they wait for an element to be on screen (visible, present, transitioned)


def slow_down_before(_func=None, sleep=1):
    def outer(func):
        def inner(*args, **kwargs):
            time.sleep(sleep)
            return func(*args, **kwargs)
        return inner
    return outer(_func) if _func else outer


def slow_down_after(_func=None, sleep=1):
    def outer(func):
        def inner(*args, **kwargs):
            r = func(*args, **kwargs)
            time.sleep(sleep)
            return r
        return inner
    return outer(_func) if _func else outer


@slow_down_before
def wait_for_element_to_be_visible(driver, by: ByType, locator: str, *, timeout: int = 60,
                                   poll_frequency: float = 0.5):
    return WebDriverWait(driver, timeout=timeout, poll_frequency=poll_frequency) \
        .until(expected_conditions.visibility_of_element_located((by, locator)))


@slow_down_before
def wait_for_element_to_be_present(driver, by: ByType, locator: str, *, timeout: int = 60,
                                   poll_frequency: float = 0.5):
    return WebDriverWait(driver, timeout=timeout, poll_frequency=poll_frequency) \
        .until(expected_conditions.presence_of_element_located((by, locator)))


@slow_down_before
def wait_for_element_to_be_invisible(driver, by: ByType, locator: str, *, timeout: int = 60,
                                     poll_frequency: float = 0.5):
    return WebDriverWait(driver, timeout=timeout, poll_frequency=poll_frequency) \
        .until(expected_conditions.invisibility_of_element_located((by, locator)))


@slow_down_before
def wait_for_element_to_be_clickable(driver, by: ByType, locator: str, *, timeout: int = 60,
                                     poll_frequency: float = 0.5):
    return WebDriverWait(driver, timeout=timeout, poll_frequency=poll_frequency) \
        .until(expected_conditions.element_to_be_clickable((by, locator)))


@slow_down_before
def wait_for_page_to_load(driver, landmarks: list[tuple[ByType, str]], loaders: list[tuple[ByType, str]], /,
                          timeout: int = 60, poll_frequency: float = 0.5):
    for loader in loaders:
        wait_for_element_to_be_invisible(driver, *loader, timeout=timeout, poll_frequency=poll_frequency)
    for landmark in landmarks:
        wait_for_element_to_be_visible(driver, *landmark, timeout=timeout, poll_frequency=poll_frequency)
