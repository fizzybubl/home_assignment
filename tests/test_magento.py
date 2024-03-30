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
        products_in_cart = checkout_pom.get_order_product_list()
        assert product_data in products_in_cart, f"Expected product: {product_data['name']} is not present in cart"
        checkout_pom.click_next()
        order_data = checkout_pom.get_order_data()
        assert order_data["sub_total"] == product_data["price"]
        assert order_data["total_amount"] == order_data["sub_total"] + order_data["shipping_fee"]
        checkout_pom.place_order()
        assert checkout_pom.is_success_message_visible()


class TestNegativeFlow:
    def test_verify_required_checkout_fields(self, driver):
        ...

    def test_verify_payment_methods(self, driver):
        ...
