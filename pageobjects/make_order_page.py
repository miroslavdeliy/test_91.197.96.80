from selenium.webdriver.common.by import By
from base.base_page import BasePage


class MakeOrderPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        self.make_order_header = (By.XPATH, "//*[@id='app']/div/div/div[1]/nav/div/div[1]")
        self.back_shop_button = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div/form/div[2]/a/button")
        self.name = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[2]/input")
        self.first_name = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[3]/input")
        self.last_name = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[4]/input")
        self.address = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[5]/input")
        self.card_number = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[6]/input")
        self.finish_order_button = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div/form/div[2]/button")
        self.error_message = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[1]")

    def get_make_order_header_text(self):
        return self._get_text(self.make_order_header)

    def back_shop(self):
        self._click(self.back_shop_button)

    def send_name(self, name):
        self._send_keys(self.name, name)

    def send_first_name(self, firstname):
        self._send_keys(self.first_name, firstname)

    def send_last_name(self, lastname):
        self._send_keys(self.last_name, lastname)

    def send_address(self, address):
        self._send_keys(self.address, address)

    def send_card_number(self, card_number):
        self._send_keys(self.card_number, card_number)

    def open_finish_order(self):
        self._click(self.finish_order_button)

    def get_error_message(self):
        return self._get_text(self.error_message)