from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

        # Локаторы
        self.cart_title = (By.XPATH, "//*[@id='app']/div/div/div[1]/nav/div/div[1]")
        self.empty_cart_message = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div")
        self.product_1_name = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[2]/div[3]/div[1]/div")
        self.product_1_input = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[2]/div[3]/div[2]/div[1]/input")
        self.product_1_price = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[2]/div[3]/div[2]/div[2]")
        self.product_1_button_plus = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[2]/div[3]/div[2]/div[1]/button[2]/span")
        self.product_1_button_minus = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[2]/div[3]/div[2]/div[1]/button[1]/span")
        self.total = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[2]/div[1]")
        self.make_order_button = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[2]/div[2]/a/button")

    # Функция ожидания с повторной попыткой при TimeoutException
    def _wait_until(self, condition, retries=1, timeout=5):
        attempt = 0
        while attempt <= retries:
            try:
                return WebDriverWait(self.driver, timeout).until(condition)
            except TimeoutException:
                attempt += 1
                if attempt > retries:
                    raise

    # Получить текст заголовка корзины
    def get_cart_title_text(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.cart_title)
        ).text

    # Получить текст пустой корзины
    def get_empty_cart_message(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.empty_cart_message)
        ).text

    # Получить текст названия товаров
    def get_product_1_name(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.product_1_name)
        ).text

    # Получить количество товаров в корзине
    def get_product_1_quantity(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.product_1_input)
        ).get_attribute("value")

    # Получить цену товара в корзине
    def get_product_1_price(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.product_1_price)
        ).text

    # Получить общую стоимость
    def get_total(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.total)
        ).text

    # Добавить один товар в корзине
    def add_product_1(self):
        input_field = self._wait_until(
            EC.visibility_of_element_located(self.product_1_input)
        )
        value_before = int(input_field.get_attribute("value"))
        self._wait_until(
            EC.element_to_be_clickable(self.product_1_button_plus)
        ).click()

        # Ожидание пока количество товаров не увеличится на 1
        self._wait_until(
            lambda d: int(d.find_element(*self.product_1_input
                                         ).get_attribute("value")) == value_before + 1)

    # Удалить товар из корзины
    def remove_product_1(self):
        input_field = self._wait_until(
            EC.visibility_of_element_located(self.product_1_input))
        value_before = int(input_field.get_attribute("value"))
        if value_before > 1:
            self._wait_until(
                EC.element_to_be_clickable(self.product_1_button_minus)
            ).click()
            # Ожидание пока количество товаров не уменьшится на 1
            self._wait_until(
                lambda d: int(d.find_element(*self.product_1_input
                                            ).get_attribute("value")) == value_before - 1)
        else:
            self._wait_until(
                EC.element_to_be_clickable(self.product_1_button_minus)
            ).click()

    # Видимость кнопки совершения заказа
    def is_make_order_button_visible(self):
        return self._wait_until(
            EC.presence_of_element_located(self.make_order_button)
        ).is_displayed()

    # Активность кнопки совершения заказа
    def is_make_order_button_enabled(self):
        return self._wait_until(
            EC.presence_of_element_located(self.make_order_button)
        ).is_enabled()

    # Нажать на кнопку совершения заказа
    def make_order(self):
        self._wait_until(
            EC.element_to_be_clickable(self.make_order_button)
        ).click()
