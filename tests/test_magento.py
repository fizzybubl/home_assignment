import pytest

from magento.home_page import MagentoPage, MagentoPageData, CheckoutPage, CheckoutPageData, ShippingData

pytestmark = [pytest.mark.ui]


class TestPositiveFlow:

    def test_buy_multiple_articles(self, driver):
        magento_pom = MagentoPage(driver, MagentoPageData)
        magento_pom.navigate_to_category(["topsCategory", "jacketsCategory"])
        product_data = magento_pom.add_random_product_to_cart()
        magento_pom.proceed_to_checkout()
        checkout_pom = CheckoutPage(driver, CheckoutPageData)
        checkout_pom.fill_in_shipping_details(ShippingData())
        checkout_pom.click_next()


class TestNegativeFlow:
    def test_verify_required_checkout_fields(self, driver):
        ...

    def test_verify_payment_methods(self, driver):
        ...
