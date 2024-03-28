import pytest

from drivers import webdriver_factory


@pytest.fixture(scope="session")
def driver():
    yield webdriver_factory()
