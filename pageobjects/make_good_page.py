from selenium.common import ElementNotInteractableException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MakeGoodPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

        # Локаторы
        self.back_to_goods_button = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[2]/div/a/button")
        self.name = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[1]/input")
        self.description = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[2]/input")
        self.category = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[3]/input")
        self.price = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[5]/input")
        self.url = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[6]/input")
        self.make_good_button = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[2]/div/button")

    def _wait_until(self, condition, retries=1, timeout=5):
        attempt = 0
        while attempt <= retries:
            try:
                return WebDriverWait(self.driver, timeout).until(condition)
            except TimeoutException:
                attempt += 1
                if attempt > retries:
                    raise

    def _send_keys(self, locator, value):
        field = self._wait_until(EC.visibility_of_element_located(locator))
        field.send_keys(value)

    def _click_with_scroll(self, locator):
        element = self._wait_until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self._wait_until(EC.element_to_be_clickable(locator))
        try:
            element.click()
        except ElementNotInteractableException:
            self.driver.execute_script("arguments[0].click();", element)

    def back_goods(self):
        self._click_with_scroll(self.back_to_goods_button)

    def enter_name(self, name):
        self._send_keys(self.name, name)

    def enter_description(self, description):
        self._send_keys(self.description, description)

    def enter_category(self, expected_category):
        self._send_keys(self.category, expected_category)

    def enter_price(self, price):
        self._send_keys(self.price, price)

    def enter_url(self, url):
        self._send_keys(self.url, url)

    def make_good(self):
        self._click_with_scroll(self.make_good_button)
