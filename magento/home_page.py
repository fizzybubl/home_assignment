import random
from dataclasses import dataclass

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By

from drivers import WebDriverType
from drivers.custom_web_element import CustomWebElement
from drivers.types import LocatorType
from utils.static_class import StaticImmutableClass
from drivers.waiters.element_waiters import wait_for_page_to_load, wait_for_element_to_be_visible, \
    wait_for_element_to_be_invisible


class PageData(StaticImmutableClass):
    url: str
    loaders: list[LocatorType]
    landmarks: list[LocatorType]
    locators: dict[str, LocatorType]


class Page:
    __slots__ = ("driver", "__locators__", "__loaders__", "__landmarks__")

    def __init__(self, driver: WebDriverType, page_data: type[PageData]):
        self.driver = driver
        self.__locators__ = page_data.locators
        self.__loaders__ = page_data.loaders
        self.__landmarks__ = page_data.landmarks
        if page_data.url:
            self.driver.go_to_url(page_data.url)
        wait_for_page_to_load(self.driver, self.__landmarks__, self.__loaders__)


_COUNTY_TO_CODE = {
    "Giurgiu": "297"
}


@dataclass
class ShippingData:
    email_address: str = "mock_email@provider.com"
    firstname: str = "firstname_mock"
    lastname: str = "lastname_mock"
    street_address_line_1: str = "Mockup Address"
    street_address_line_2: str = ""
    street_address_line_3: str = ""
    city: str = "Giurgiu"
    country: str = "RO"
    postcode: str = "000222"
    phone_number: str = "0799234234"
    company: str = "Mock company"
    state: str = _COUNTY_TO_CODE["Giurgiu"]


class MagentoPageData(PageData):
    url: str = "https://magento.softwaretestingboard.com/"
    loaders: list[LocatorType] = []
    landmarks: list[LocatorType] = [(By.CSS_SELECTOR, "a.home-main"), (By.CSS_SELECTOR, "[data-action='navigation']")]
    locators: dict[str, LocatorType] = {
        "menTab": (By.XPATH, "//*[@data-action='navigation']//*[text()='Men']/../.."),
        "topsCategory": (By.XPATH, ".//*[text()='Tops']"),
        "jacketsCategory": (By.XPATH, ".//*[text()='Jackets']"),
        "productCard": (By.CSS_SELECTOR, ".product-item-info"),
        "colorBox": (By.CSS_SELECTOR, ".swatch-option.color"),
        "sizeBox": (By.CSS_SELECTOR, ".swatch-option.text"),
        "addToCart": (By.CSS_SELECTOR, "button.tocart.action"),
        "cartButton": (By.CSS_SELECTOR, ".action.showcart"),
        "proceedToCheckout": (By.CSS_SELECTOR, "[title='Proceed to Checkout']"),
        "itemsInCart": (By.CSS_SELECTOR, ".block items-in-cart")
    }


class CheckoutPageData(PageData):
    url: str = ""
    loaders = [(By.ID, "checkout-loader")]
    landmarks = [(By.CSS_SELECTOR, ".opc-progress-bar")]
    locators = {
        "emailAddress": (By.ID, "customer-email"),
        "firstName": (By.CSS_SELECTOR, "[name='firstname']"),
        "lastName": (By.CSS_SELECTOR, "[name='lastname']"),
        "company": (By.CSS_SELECTOR, "[name='company']"),
        "streetAddress0": (By.CSS_SELECTOR, "[name='street[0]']"),
        "streetAddress1": (By.CSS_SELECTOR, "[name='street[1]']"),
        "streetAddress2": (By.CSS_SELECTOR, "[name='street[2]']"),
        "city": (By.CSS_SELECTOR, "[name='city']"),
        "state": (By.CSS_SELECTOR, "[name='region_id']"),
        "postCode": (By.CSS_SELECTOR, "[name='postcode']"),
        "country": (By.CSS_SELECTOR, "[name='country_id']"),
        "phoneNumber": (By.CSS_SELECTOR, "[name='telephone']"),
        "product": (By.CSS_SELECTOR, ".product-item-details"),
        "nextButton": (By.CSS_SELECTOR, "button.action.continue"),
        "productInCart": (By.CSS_SELECTOR, ".minicart-items > .product-item"),
        "viewProductDetails": (By.CSS_SELECTOR, ".product.options span"),
        "productName": (By.CSS_SELECTOR, ".product-item-name"),
        "productPrice": (By.CSS_SELECTOR, ".price"),
        "productColor": (By.CSS_SELECTOR, ".item-options .values:nth-child(4)"),
        "productSize": (By.CSS_SELECTOR, ".item-options .values:nth-child(2)"),
        "showItemsInCart": (By.CSS_SELECTOR, ".block.items-in-cart"),
        "placeOrderButton": (By.CSS_SELECTOR, "button.checkout"),
        "orderTotal": (By.CSS_SELECTOR, "[data-th='Order Total'] span"),
        "orderSubtotal": (By.CSS_SELECTOR, "[data-th='Cart Subtotal']"),
        "shippingFee": (By.CSS_SELECTOR, "[data-th='Shipping']"),
        "sucessfulMessage": (By.XPATH, "//*[text()='Thank you for your purchase!']")
    }


class CheckoutPage(Page):

    def __init__(self, driver: WebDriverType, page_data: type[PageData]):
        super().__init__(driver, page_data)

    def fill_in_shipping_details(self, shipping_data: ShippingData):
        self.driver.write_text(self.__locators__["emailAddress"], shipping_data.email_address)
        self.driver.write_text(self.__locators__["streetAddress0"], shipping_data.street_address_line_1)
        self.driver.write_text(self.__locators__["streetAddress1"], shipping_data.street_address_line_2)
        self.driver.write_text(self.__locators__["streetAddress2"], shipping_data.street_address_line_3)
        self.driver.write_text(self.__locators__["firstName"], shipping_data.firstname)
        self.driver.write_text(self.__locators__["lastName"], shipping_data.lastname)
        self.driver.write_text(self.__locators__["company"], shipping_data.company)
        self.driver.write_text(self.__locators__["phoneNumber"], shipping_data.phone_number)
        self.driver.write_text(self.__locators__["postCode"], shipping_data.postcode)
        self.driver.write_text(self.__locators__["city"], shipping_data.city)
        self.driver.select_option_from_dropdown(self.__locators__["country"], shipping_data.country)
        self.driver.select_option_from_dropdown(self.__locators__["state"], shipping_data.state)

    def get_order_product_list(self):
        self.driver.click_element(self.__locators__["showItemsInCart"])
        products_in_cart = self.driver.list_elements(self.__locators__["productInCart"])
        product_data = []
        for prod in products_in_cart:
            prod.click_element(self.__locators__["viewProductDetails"])
            product_data.append({
                "price": prod.get_element(self.__locators__["productPrice"]).text,
                "name": prod.get_element(self.__locators__["productName"]).text,
                "color": prod.get_element(self.__locators__["productColor"]).text,
                "size": prod.get_element(self.__locators__["productSize"]).text
            })
        return product_data

    def click_next(self):
        self.driver.click_element(self.__locators__["nextButton"])
        wait_for_page_to_load(self.driver, [], [(By.CSS_SELECTOR, ".loader")])

    def place_order(self):
        self.driver.click_element(self.__locators__["placeOrderButton"])

    def get_order_total(self):
        return self.driver.get_element(self.__locators__["orderTotal"]).text

    def get_order_data(self):
        return {
            "total_amount": self.driver.get_element(self.__locators__["orderTotal"]).text,
            "sub_total": self.driver.get_element(self.__locators__["orderSubtotal"]).text,
            "shipping_fee": self.driver.get_element(self.__locators__["shippingFee"]).text
        }

    def is_success_message_visible(self):
        wait_for_page_to_load(self.driver, [], [(By.CSS_SELECTOR, ".loader")])
        return self.driver.is_visible(self.__locators__["sucessfulMessage"])


class MagentoPage(Page):

    def __init__(self, driver: WebDriverType, page_data: type[PageData]):
        super().__init__(driver, page_data)

    def navigate_to_category(self, path_to_category: list[str]):
        self.driver.move_to_element(self.__locators__["menTab"])
        men_tab = self.driver.get_element(self.__locators__["menTab"])
        for category in path_to_category:
            self.driver.move_to_element(men_tab.get_element(self.__locators__[category]))
        men_tab.get_element(self.__locators__[path_to_category[-1]]).click()

    def add_random_product_to_cart(self):
        """Adds a random product to cart and returns the data about it.

        Data such as:
            name
            size
            color
        """
        wait_for_page_to_load(self.driver, [], [])
        products = self.driver.list_elements(self.__locators__["productCard"])
        product: CustomWebElement = random.choice(products)
        self.driver.move_to_element(product)

        random_color = random.choice(product.list_elements(self.__locators__["colorBox"]))
        random_color.click()

        random_size = random.choice(product.list_elements(self.__locators__["sizeBox"]))
        random_size.click()
        wait_for_page_to_load(self.driver, [], [])
        product.get_element(self.__locators__["addToCart"]).click()
        wait_for_element_to_be_visible(self.driver, By.CSS_SELECTOR, "[data-ui-id='message-success']")
        return {
            "name": product.get_element((By.CSS_SELECTOR, ".product-item-name a")).text,
            "size": random_size.text,
            "color": random_color.get_attribute("option-label"),
            "price": product.get_element((By.CSS_SELECTOR, "[data-price-type='finalPrice'] span")).text
        }

    def proceed_to_checkout(self):
        self.driver.click_element(self.__locators__["cartButton"])
        self.driver.click_element(self.__locators__["proceedToCheckout"])
        wait_for_element_to_be_invisible(self.driver, By.ID, "checkout-loader")


def is_error_visible(driver, error_message):
    return driver.is_visible((By.XPATH, f"//*[contains(text(), '{error_message}')]"))


def are_errors_visible(driver, error_message, count):
    return len(driver.list_elements((By.XPATH, f"//*[contains(text(), '{error_message}')]"))) == count
