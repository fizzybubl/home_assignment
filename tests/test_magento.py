import pytest
from selenium.webdriver import Keys

from magento.home_page import MagentoPage, MagentoPageData, CheckoutPage, CheckoutPageData, ShippingData, \
    are_errors_visible

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
        assert float(order_data["total_amount"].strip("$")) == float(order_data["sub_total"].strip("$")) + \
               float(order_data["shipping_fee"].strip("$"))
        checkout_pom.place_order()
        assert checkout_pom.is_success_message_visible()


class TestNegativeFlow:
    def test_verify_required_checkout_fields(self, driver):
        magento_pom = MagentoPage(driver, MagentoPageData)
        magento_pom.navigate_to_category(["topsCategory", "jacketsCategory"])
        magento_pom.add_random_product_to_cart()
        magento_pom.proceed_to_checkout()
        checkout_pom = CheckoutPage(driver, CheckoutPageData)
        checkout_pom.fill_in_shipping_details(ShippingData(email_address=Keys.ENTER,
                                                           firstname=Keys.SPACE,
                                                           lastname=Keys.SPACE,
                                                           street_address_line_1=Keys.SPACE,
                                                           city=Keys.SPACE,
                                                           postcode=Keys.SPACE,
                                                           phone_number=Keys.SPACE,
                                                           country="",
                                                           state=""))
        assert are_errors_visible(driver, "This is a required field.", 8)

    def test_invalid_fields(self, driver):
        magento_pom = MagentoPage(driver, MagentoPageData)
        magento_pom.navigate_to_category(["topsCategory", "jacketsCategory"])
        magento_pom.add_random_product_to_cart()
        magento_pom.proceed_to_checkout()
        checkout_pom = CheckoutPage(driver, CheckoutPageData)
        checkout_pom.fill_in_shipping_details(ShippingData(email_address="asfagsgasg",
                                                           postcode="agalkghakga"))
        assert are_errors_visible(driver, "Please enter a valid email address (Ex: johndoe@domain.com)", 1)
        assert are_errors_visible(driver, "Provided Zip/Postal Code seems to be invalid", 1)
