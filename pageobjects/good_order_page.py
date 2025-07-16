from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class GoodOrderPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

        # Локаторы
        self.good_order_title = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div/div[2]")

    def _wait_until(self, condition, retries=1, timeout=5):
        attempt = 0
        while attempt <= retries:
            try:
                return WebDriverWait(self.driver, timeout).until(condition)
            except TimeoutException:
                attempt += 1
                if attempt > retries:
                    raise

    # Получить текст успешного заказа
    def get_good_order_page_title(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.good_order_title)
        ).text