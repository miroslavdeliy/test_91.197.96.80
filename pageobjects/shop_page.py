from selenium.webdriver.common.by import By

from base.base_page import BasePage
from helpers.wait_for_element import wait_for_element


class ShopPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        self.shop_header = (By.XPATH, "//*[@id='app']/div/nav/div/a[1]")
        self.shop_title = (By.XPATH, "//*[@id='app']/div/div/div[1]/nav/div/div[1]")
        self.product_1_name = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[3]/div")
        self.product_1_description = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[3]/p")
        self.product_1_price = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[6]")
        self.product_1_image = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[1]/img")
        self.product_1_input = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[4]/div/input")
        self.product_1_button_plus = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[4]/div/button[2]/span")
        self.product_1_button_minus = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[4]/div/button[1]/span")
        self.quantity_goods_in_cart = (By.XPATH, "//*[@id='app']/div/nav/div/a[2]/button/span[2]")
        self.cart_icon = (By.XPATH, "//*[@id='app']/div/nav/div/a[2]/button/span[1]")

    def get_shop_header_text(self):
        return self._get_text(self.shop_header)

    def get_shop_title_text(self):
        return self._get_text(self.shop_title)

    def get_product_1_name(self):
        return self._get_text(self.product_1_name)

    def get_product_1_description(self):
        return self._get_text(self.product_1_description)

    def get_product_1_price(self):
        return self._get_text(self.product_1_price)

    def get_product_1_image(self):
        return wait_for_element(self.driver, *self.product_1_image, condition="visible")

    def get_product_1_quantity(self):
        return self._get_attribute(self.product_1_input, "value")

    def add_product_1(self):
        value_before = int(self.get_product_1_quantity())
        self._click(self.product_1_button_plus)
        self._wait_until(lambda d: int(d.find_element(*self.product_1_input).get_attribute("value")) == value_before + 1)

    def remove_product_1(self):
        value_before = int(self.get_product_1_quantity())
        self._click(self.product_1_button_minus)
        self._wait_until(lambda d: int(d.find_element(*self.product_1_input).get_attribute("value")) == value_before - 1)

    def get_quantity_goods_in_cart(self):
        return self._get_text(self.quantity_goods_in_cart)

    def open_cart(self):
        self._click(self.cart_icon)

    def get_alt_text_image(self):
        return self._get_attribute(self.product_1_image, "alt")