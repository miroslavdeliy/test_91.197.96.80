from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class MakeOrderPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

        # Локаторы
        self.make_order_header = (By.XPATH, "//*[@id='app']/div/div/div[1]/nav/div/div[1]")
        self.back_shop_button = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div/form/div[2]/a/button")
        self.name = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[2]/input")
        self.first_name = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[3]/input")
        self.last_name = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[4]/input")
        self.address = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[5]/input")
        self.card_number = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[6]/input")
        self.finish_order_button = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div/form/div[2]/button")
        self.error_message = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[1]")

    def _wait_until(self, condition, retries=1, timeout=5):
        attempt = 0
        while attempt <= retries:
            try:
                return WebDriverWait(self.driver, timeout).until(condition)
            except TimeoutException:
                attempt += 1
                if attempt > retries:
                    raise

    def get_make_order_header_text(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.make_order_header)
        ).text

    def back_shop(self):
        self._wait_until(
            EC.element_to_be_clickable(self.back_shop_button)
        ).click()

    def send_name(self, name):
        self._wait_until(
            EC.visibility_of_element_located(self.name)
        ).send_keys(name)

    def send_first_name(self, firstname):
        self._wait_until(
            EC.visibility_of_element_located(self.first_name)
        ).send_keys(firstname)

    def send_last_name(self, lastname):
        self._wait_until(
            EC.visibility_of_element_located(self.last_name)
        ).send_keys(lastname)

    def send_address(self, address):
        self._wait_until(
            EC.visibility_of_element_located(self.address)
        ).send_keys(address)

    def send_card_number(self, card_number):
        self._wait_until(
            EC.visibility_of_element_located(self.card_number)
        ).send_keys(card_number)

    # Нажать на
    def open_finish_order(self):
        self._wait_until(
            EC.element_to_be_clickable(self.finish_order_button)
        ).click()

    # Получить текст сообщения об ошибке
    def get_error_message(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.error_message)
        ).text