from selenium.webdriver.common.by import By
from base.base_page import BasePage


class MenuPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        # Локаторы
        self.menu_button = (By.XPATH, "//*[@id='app']/div/nav/div/button")
        self.cart_link = (By.XPATH, "//*[@id='offcanvasNavbar']/div[2]/ul[3]/a")
        self.shop_link = (By.XPATH, "//*[@id='offcanvasNavbar']/div[2]/ul[2]/a")
        self.logout_button = (By.XPATH, "//*[@id='offcanvasNavbar']/div[2]/ul[4]/li/div")
        self.edit_goods_link = (By.XPATH, "//*[@id='offcanvasNavbar']/div[2]/ul[1]/a")

    def open_menu(self):
        self._click(self.menu_button)

    def get_cart_link_text(self):
        return self._get_text(self.cart_link)

    def open_cart(self):
        self._click(self.cart_link)

    def get_shop_link_text(self):
        return self._get_text(self.shop_link)

    def open_shop(self):
        self._click(self.shop_link)

    def get_logout_button_text(self):
        return self._get_text(self.logout_button)

    def logout(self):
        self._click(self.logout_button)

    def open_edit(self):
        self._click(self.edit_goods_link)