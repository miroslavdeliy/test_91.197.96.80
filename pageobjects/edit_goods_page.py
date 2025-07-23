from selenium.webdriver.common.by import By
from base.base_page import BasePage


class EditGoodsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        self.edit_header = (By.XPATH, "//*[@id='app']/div/div/div[1]/nav/div/div[1]")
        self.add_good_button = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[5]/a/button")
        self.name = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[5]/div[2]/div[1]/div")
        self.description = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[5]/div[2]/div[1]/p")
        self.category = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[5]/div[2]/div[2]/div/div")
        self.price = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[5]/div[2]/div[3]/div/div")
        self.image = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[5]/div[1]/img")
        self.edit_product_1_button = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[3]/a/button/span")
        self.edit_product_5_button = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[5]/div[3]/a/button/span")
        self.delete_product_button = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[5]/div[4]/button/span")

    def get_edit_header_text(self):
        return self._get_text(self.edit_header)

    def add_good(self):
        self._click(self.add_good_button)

    def get_name(self):
        return self._get_text(self.name)

    def get_description(self):
        return self._get_text(self.description)

    def get_category(self):
        return self._get_text(self.category)

    def get_price(self):
        return self._get_text(self.price)

    def get_image_maked_good(self):
        return self._get_attribute(self.image, "src")

    def open_edit_product_1(self):
        self._click(self.edit_product_1_button)

    def open_edit_product_5(self):
        self._click(self.edit_product_5_button)

    def delete_product(self):
        self._click(self.delete_product_button)