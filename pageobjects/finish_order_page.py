from selenium.webdriver.common.by import By
from base.base_page import BasePage


class FinishOrderPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        self.finish_order_title = (By.XPATH, "//*[@id='app']/div/div/div[1]/nav/div/div[1]")
        self.back_shop_button = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[11]/div/a[1]/button")
        self.name_product = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[2]/div[2]/div[1]/div")
        self.name = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[4]/div[1]")
        self.first_name = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[4]/div[2]")
        self.last_name = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[4]/div[3]")
        self.address = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[6]/div[1]")
        self.card_number = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[8]/div[2]")
        self.quantity_goods = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[10]/div[1]")
        self.total = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[10]/div[2]")
        self.finish_order_button = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[11]/div/a[2]/button")

    def get_finish_order_title(self):
        return self._get_text(self.finish_order_title)

    def back_shop(self):
        self._click(self.back_shop_button)

    def get_finish_order_name_product(self):
        return self._get_text(self.name_product)

    def get_finish_order_name(self):
        return self._get_text(self.name)

    def get_finish_order_first_name(self):
        return self._get_text(self.first_name)

    def get_finish_order_last_name(self):
        return self._get_text(self.last_name)

    def get_finish_order_address(self):
        return self._get_text(self.address)

    def get_finish_order_card_number(self):
        return self._get_text(self.card_number)

    def get_finish_order_quantity_goods(self):
        return self._get_text(self.quantity_goods)

    def get_finish_order_total(self):
        return self._get_text(self.total)

    def finish_order(self):
        self._click(self.finish_order_button)