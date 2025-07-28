from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from base.base_page import BasePage


class EditProductPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        self.back_goods_button = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[2]/div/a/button")
        self.name = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[2]/input")
        self.description = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[3]/input")
        self.category = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[4]/input")
        self.price = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[6]/input")
        self.url = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[7]/input")
        self.edit_button = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[2]/div/button")

    def _clear_and_send_keys(self, locator, value):
        input_element = self._get_element(locator, condition="visible")
        self._wait_for_value_not_clear(input_element)
        input_element.click()
        input_element.send_keys(Keys.CONTROL + 'a')
        input_element.send_keys(Keys.BACKSPACE)
        input_element.send_keys(value)

    def _wait_for_value_not_clear(self, element, timeout=5):
        from selenium.webdriver.support.ui import WebDriverWait
        WebDriverWait(self.driver, timeout).until(lambda _: element.get_attribute("value") != "")

    def clear_and_enter_name(self, name):
        self._clear_and_send_keys(self.name, name)

    def clear_and_enter_description(self, description):
        self._clear_and_send_keys(self.description, description)

    def clear_and_enter_category(self, category):
        self._clear_and_send_keys(self.category, category)

    def clear_and_enter_price(self, price):
        self._clear_and_send_keys(self.price, price)

    def clear_and_enter_url(self, url):
        self._clear_and_send_keys(self.url, url)

    def back_goods(self):
        self._scroll_and_click(self.back_goods_button)

    def edit_product(self):
        self._scroll_and_click(self.edit_button)