import pytest

pytestmark = [pytest.mark.ui]


class TestPositiveFlow:
    def test_buy_one_article(self, driver):
        ...

    def test_buy_multiple_articles(self, driver):
        ...


class TestNegativeFlow:
    def test_verify_required_checkout_fields(self, driver):
        ...

    def test_verify_payment_methods(self, driver):
        ...
