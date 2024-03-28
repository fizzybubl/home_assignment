import pytest

from drivers import webdriver_factory


@pytest.fixture(scope="session")
def driver():
    with webdriver_factory() as driver:
        yield driver
