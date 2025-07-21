from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class EditGoodsPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

        # Локаторы
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

    def _wait_until(self, condition, retries=1):
        attempt = 0
        while attempt <= retries:
            try:
                return self.wait.until(condition)
            except TimeoutException:
                attempt += 1
                if attempt > retries:
                    raise

    def get_edit_header_text(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.edit_header)
        ).text

    def add_good(self):
        self._wait_until(
            EC.element_to_be_clickable(self.add_good_button)
        ).click()

    def get_name(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.name)
        ).text

    def get_description(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.description)
        ).text

    def get_category(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.category)
        ).text

    def get_price(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.price)
        ).text

    def get_image_maked_good(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.image)
        ).get_attribute("src")

    def open_edit_product_1(self):
        self._wait_until(
            EC.element_to_be_clickable(self.edit_product_1_button)
        ).click()

    def open_edit_product_5(self):
        self._wait_until(
            EC.element_to_be_clickable(self.edit_product_5_button)
        ).click()

    def delete_product(self):
        self._wait_until(
            EC.element_to_be_clickable(self.delete_product_button)
        ).click()