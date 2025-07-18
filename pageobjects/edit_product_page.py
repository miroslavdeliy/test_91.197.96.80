from selenium.common import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class EditProductPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

        # Локаторы
        self.back_goods_button = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[2]/div/a/button")
        self.name = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[2]/input")
        self.description = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[3]/input")
        self.category = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[4]/input")
        self.price = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[6]/input")
        self.url = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[7]/input")
        self.edit_button = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[2]/div/button")

    # Обработка исключения TimeoutException
    def _wait_until(self, condition, retries=1):
        attempt = 0
        while attempt <= retries:
            try:
                return self.wait.until(condition)
            except TimeoutException:
                attempt += 1
                if attempt > retries:
                    raise

    # Очистка поля и ввод нового значения
    def _clear_and_send_keys(self, locator, value):
        input_element = self._wait_until(
            EC.visibility_of_element_located(locator)
        )
        input_element.click()  # Фокусируемся на элементе
        input_element.send_keys(Keys.CONTROL + 'a')  # Выделить весь текст
        input_element.send_keys(Keys.BACKSPACE)  # Удалить выделенный текст
        self._wait_until(lambda _: input_element.get_attribute("value") == "")
        input_element.send_keys(value)  # Ввести новое значение

    # Ввод нового названия товара
    def clear_and_enter_name(self, name):
        self._clear_and_send_keys(self.name, name)

    # Ввод нового описания товара
    def clear_and_enter_description(self, description):
        self._clear_and_send_keys(self.description, description)

    # Ввод новой категории товара
    def clear_and_enter_category(self, expected_category):
        self._clear_and_send_keys(self.category, expected_category)

    # Ввод новой цены товара
    def clear_and_enter_price(self, price):
        self._clear_and_send_keys(self.price, price)

    # Ввод нового url изображения
    def clear_and_enter_url(self, url):
        self._clear_and_send_keys(self.url, url)

    # Проскроллить до кнопки и ожидание кликабельности
    def _click_with_scroll(self, locator):
        element = self._wait_until(EC.presence_of_element_located(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element)
        try:
            # Пробуем кликнуть через ActionChains (имитация реального клика)
            ActionChains(self.driver).move_to_element(element).click().perform()
        except Exception:
            # Если не вышло — JS в помощь
            self.driver.execute_script("arguments[0].click();", element)

    # Нажать кнопку 'Обратно к товарам'
    def back_goods(self):
        self._click_with_scroll(self.back_goods_button)

    # Нажать кнопку 'Обновить товар'
    def edit_product(self):
        self._click_with_scroll(self.edit_button)