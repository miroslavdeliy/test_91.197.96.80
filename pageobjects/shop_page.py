from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class ShopPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

        # Локаторы
        self.shop_header = (By.XPATH, "//*[@id='app']/div/nav/div/a[1]")
        self.shop_title = (By.XPATH, "//*[@id='app']/div/div/div[1]/nav/div/div[1]")
        self.product_1_name = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[3]/div")
        self.product_1_description = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[3]/p")
        self.product_1_price = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[6]")
        self.product_1_image = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[1]/img")
        self.product_1_input = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[4]/div/input")
        self.product_1_button_plus = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[4]/div/button[2]/span")
        self.product_1_button_minus = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div[4]/div/button[1]/span")
        self.quantity_goods_in_cart = (By.XPATH, "//*[@id='app']/div/nav/div/a[2]/button/span[2]")
        self.cart_icon = (By.XPATH, "//*[@id='app']/div/nav/div/a[2]/button/span[1]")

    def _wait_until(self, condition, retries=1, timeout=5):
        attempt = 0
        while attempt <= retries:
            try:
                return WebDriverWait(self.driver, timeout).until(condition)
            except TimeoutException:
                attempt += 1
                if attempt > retries:
                    raise

    # Получить заголовок магазина
    def get_shop_header_text(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.shop_header)
        ).text

    # Получить заголовок каталога
    def get_shop_title_text(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.shop_title)
        ).text

    # Получить название первого товара
    def get_product_1_name(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.product_1_name)
        ).text

    # Получить описание первого товара
    def get_product_1_description(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.product_1_description)
        ).text

    # Получить цену 1-го товара
    def get_product_1_price(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.product_1_price)
        ).text

    # Получить изображение 1-го товара
    def get_product_1_image(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.product_1_image)
        )

    # Получить количество 1-го товара
    def get_product_1_quantity(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.product_1_input)
        ).get_attribute("value")

    # Добавить 1 товар
    def add_product_1(self):
        input_field = self._wait_until(EC.visibility_of_element_located(self.product_1_input))
        value_before = int(input_field.get_attribute("value"))
        self._wait_until(
            EC.element_to_be_clickable(self.product_1_button_plus)
        ).click()

        # Ожидать пока количество товара увеличится на 1
        self._wait_until(
            lambda d: int(d.find_element(*self.product_1_input
                                         ).get_attribute("value")) == value_before + 1)
    # Удалить 1 товар
    def remove_product_1(self):
        input_field = self._wait_until(EC.visibility_of_element_located(self.product_1_input))
        value_before = int(input_field.get_attribute("value"))
        self._wait_until(
            EC.element_to_be_clickable(self.product_1_button_minus)
        ).click()

        # Ожидать пока количество товара уменьшится на 1
        self._wait_until(
            lambda d: int(d.find_element(*self.product_1_input
                                         ).get_attribute("value")) == value_before - 1)

    # Получить количество товара в корзине
    def get_quantity_goods_in_cart(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.quantity_goods_in_cart)
        ).text

    # Нажать на иконку корзины
    def open_cart(self):
        self._wait_until(
            EC.element_to_be_clickable(self.cart_icon)
        ).click()

    # Получить альтернативный текст изображения
    def get_alt_text_image(self):
        return self.get_product_1_image().get_attribute("alt")