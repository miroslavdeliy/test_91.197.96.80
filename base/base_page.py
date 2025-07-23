from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from helpers.wait_for_element import wait_for_element


class BasePage:
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.timeout = timeout

    def _get_text(self, locator, condition="visible", timeout=None):
        try:
            by, value = locator
            element = wait_for_element(
                self.driver, by, value,
                timeout=timeout or self.timeout,
                condition=condition
            )
            return element.text.strip()
        except TimeoutException:
            raise AssertionError(f"Не удалось получить текст: "
                                 f"элемент не найден по локатору "
                                 f"{locator} ({condition})")

    def _click(self, locator, timeout=None):
        element = wait_for_element(
            self.driver, *locator,
            timeout=timeout or self.timeout,
            condition="clickable"
        )
        element.click()

    def _get_attribute(self, locator, attr_name, condition="visible",
                       timeout=None):
        element = wait_for_element(
            self.driver, *locator,
            timeout=timeout or self.timeout,
            condition=condition
        )
        return element.get_attribute(attr_name)

    def _wait_until(self, condition, retries=1, timeout=None):
        attempt = 0
        timeout = timeout or self.timeout
        while attempt <= retries:
            try:
                return WebDriverWait(self.driver, timeout).until(condition)
            except TimeoutException:
                attempt += 1
                if attempt > retries:
                    raise

    def _send_keys(self, locator, value, timeout=None):
        element = self._get_element(locator, condition="visible", timeout=timeout)
        element.clear()
        element.send_keys(value)

    def _get_element(self, locator, timeout=None, condition="visible"):
        by, value = locator
        return wait_for_element(
            self.driver, by, value,
            timeout=timeout or self.timeout,
            condition=condition
        )