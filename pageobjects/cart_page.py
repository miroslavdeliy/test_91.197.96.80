from selenium.webdriver.common.by import By
from base.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        self.cart_title = (By.XPATH, "//*[@id='app']/div/div/div[1]/nav/div/div[1]")
        self.empty_cart_message = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div")
        self.product_1_name = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[2]/div[3]/div[1]/div")
        self.product_1_input = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[2]/div[3]/div[2]/div[1]/input")
        self.product_1_price = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[2]/div[3]/div[2]/div[2]")
        self.product_1_button_plus = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[2]/div[3]/div[2]/div[1]/button[2]/span")
        self.product_1_button_minus = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[2]/div[3]/div[2]/div[1]/button[1]/span")
        self.total = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[2]/div[1]")
        self.make_order_button = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[2]/div[2]/a/button")

    def get_cart_title_text(self):
        return self._get_text(self.cart_title)

    def get_empty_cart_message(self):
        return self._get_text(self.empty_cart_message)

    def get_product_1_name(self):
        return self._get_text(self.product_1_name)

    def get_product_1_quantity(self):
        return self._get_attribute(self.product_1_input, "value")

    def get_product_1_price(self):
        return self._get_text(self.product_1_price)

    def get_total(self):
        return self._get_text(self.total)

    def add_product_1(self):
        value_before = int(self.get_product_1_quantity())
        self._click(self.product_1_button_plus)
        self._wait_until(lambda d: int(d.find_element(*self.product_1_input).get_attribute("value")) == value_before + 1)

    def remove_product_1(self):
        value_before = int(self.get_product_1_quantity())
        self._click(self.product_1_button_minus)
        if value_before > 1:
            self._wait_until(lambda d: int(d.find_element(*self.product_1_input).get_attribute("value")) == value_before - 1)

    def is_make_order_button_visible(self):
        return self._get_element(self.make_order_button, condition="present").is_displayed()

    def is_make_order_button_enabled(self):
        return self._get_element(self.make_order_button, condition="present").is_enabled()

    def make_order(self):
        self._click(self.make_order_button)
