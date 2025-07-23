from selenium.webdriver.common.by import By
from base.base_page import BasePage


class GoodOrderPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.good_order_title = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div/div[2]")

    def get_good_order_page_title(self):
        return self._get_text(self.good_order_title)