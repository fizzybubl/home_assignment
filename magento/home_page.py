import random
from dataclasses import dataclass

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


@dataclass
class ShippingData:
    ...


class MagentoPageData(PageData):
    url: str = "https://magento.softwaretestingboard.com/"
    loaders: list[LocatorType] = []
    landmarks: list[LocatorType] = [(By.CSS_SELECTOR, "a.home-main"), (By.CSS_SELECTOR, "[data-action='navigation']")]
    locators: dict[str, LocatorType] = {
        "menTab": (By.XPATH, "//*[@data-action='navigation']//*[text()='Men']"),
        "topsCategory": (By.XPATH, "//*[@data-action='navigation']//*[text()='Tops']"),
        "jacketsCategory": (By.XPATH, "//*[@data-action='navigation']//*[text()='Jackets']"),
        "productCard": (By.CSS_SELECTOR, ".product-item-info"),
        "colorBox": (By.CSS_SELECTOR, ".swatch-option.color"),
        "sizeBox": (By.CSS_SELECTOR, ".swatch-option.text"),
        "addToCart": (By.CSS_SELECTOR, "button.tocart.action"),
        "cartButton": (By.CSS_SELECTOR, ".action.showcart"),
        "proceedToCheckout": (By.CSS_SELECTOR, "[title='Proceed to Checkout']")
    }


class CheckoutPageData(PageData):
    url: str = ""
    loaders = [(By.ID, "checkout-loader")]
    landmarks = [(By.CSS_SELECTOR, ".opc-progress-bar")]
    locators = {
        "emailAddress": (),
        "firstName": (),
        "lastName": (),
        "company": (),
        "streetAddress0": (),
        "streetAddress1": (),
        "streetAddress2": (),
        "city": (),
        "state": (),
        "postCode": (),
        "country": (),
        "phoneNumber": (),
    }



class CheckoutPage(Page):

    def __init__(self, driver: WebDriverType, page_data: type[PageData]):
        super().__init__(driver, page_data)


class MagentoPage(Page):

    def __init__(self, driver: WebDriverType, page_data: type[PageData]):
        super().__init__(driver, page_data)

    def navigate_to_category(self, path_to_category: list[str]):
        self.driver.move_to_element(self.__locators__["menTab"])
        for category in path_to_category:
            self.driver.move_to_element(self.__locators__[category])
        self.driver.click_element(self.__locators__[path_to_category[-1]])

    def add_random_product_to_cart(self):
        products = self.driver.list_elements(self.__locators__["productCard"])
        product: CustomWebElement = random.choice(products)
        self.driver.move_to_element(product)

        random_color = random.choice(product.list_elements(self.__locators__["colorBox"]))
        random_color.click()

        random_size = random.choice(product.list_elements(self.__locators__["sizeBox"]))
        random_size.click()
        product.get_element(self.__locators__["addToCard"]).click()
        wait_for_element_to_be_visible(self.driver, By.CSS_SELECTOR, "[data-ui-id='message-success']")

    def proceed_to_checkout(self):
        self.driver.click_element(self.__locators__["cartButton"])
        self.driver.click_element(self.__locators__["proceedToCheckout"])
        wait_for_element_to_be_invisible(self.driver, By.ID, "checkout-loader")

    def fill_in_shipping_data(self, shipping_data: ShippingData):
        ...