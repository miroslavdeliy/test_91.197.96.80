# Импортирование библиотек
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

# Импортирование пользовательских библиотек
from helpers.wait_for_element import wait_for_element


class BasePage:
    # Конструктор
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.timeout = timeout

    # Метод получение текста из элемента
    def _get_text(self, locator, condition="visible", timeout=None):
        by, value = locator
        element = wait_for_element(
                self.driver, by, value,
                timeout=timeout or self.timeout,
                condition=condition
        )
        return element.text.strip()

    # Метод клика по элементу
    def _click(self, locator, timeout=None):
        element = wait_for_element(
            self.driver, *locator,
            timeout=timeout or self.timeout,
            condition="clickable"
        )
        element.click()

    # Метод получения аттрибута элемента
    def _get_attribute(self, locator, attr_name, condition="visible", timeout=None):
        element = wait_for_element(self.driver, *locator, timeout=timeout or self.timeout, condition=condition)
        return element.get_attribute(attr_name)

    # Метод кастомного ожидания
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

    # Метод ввода данных в поле
    def _send_keys(self, locator, value, timeout=None):
        element = self._get_element(locator, condition="visible", timeout=timeout)
        element.click()
        element.send_keys(value)

    # Метод получения элемента страницы
    def _get_element(self, locator, timeout=None, condition="visible"):
        by, value = locator
        return wait_for_element(self.driver, by, value, timeout=timeout or self.timeout, condition=condition)

    # Метод скролла и нажатия на кнопку
    def _scroll_and_click(self, locator):
        # Ожидать появление элемента в DOM
        element = self._get_element(locator, condition="present")
        # Проскроллить до элемента с помощью JS
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        try:
            # Навестить и кликнуть с помощью ActionChains
            ActionChains(self.driver).move_to_element(element).click().perform()
        except Exception:
            # В случае неудачи клик через JS
            self.driver.execute_script("arguments[0].click();", element)