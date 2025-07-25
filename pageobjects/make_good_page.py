from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from base.base_page import BasePage


class MakeGoodPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        # Локаторы
        self.back_to_goods_button = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[2]/div/a/button")
        self.name = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[1]/input")
        self.description = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[2]/input")
        self.category = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[3]/input")
        self.price = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[5]/input")
        self.url = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[6]/input")
        self.make_good_button = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[2]/div/button")

    def _scroll_and_click(self, locator):
        element = self._get_element(locator, condition="present")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        try:
            ActionChains(self.driver).move_to_element(element).click().perform()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    def back_goods(self):
        self._scroll_and_click(self.back_to_goods_button)

    def enter_name(self, name):
        self._send_keys(self.name, name)

    def enter_description(self, description):
        self._send_keys(self.description, description)

    def enter_category(self, category):
        self._send_keys(self.category, category)

    def enter_price(self, price):
        self._send_keys(self.price, price)

    def enter_url(self, url):
        self._send_keys(self.url, url)

    def make_good(self):
        self._scroll_and_click(self.make_good_button)