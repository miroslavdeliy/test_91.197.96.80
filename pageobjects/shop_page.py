# Импорт библиотек
from selenium.webdriver.common.by import By

# Импорт пользовательских библиотек
from base.base_page import BasePage


class ShopPage(BasePage):
    # Конструктор
    def __init__(self, driver):
        # Вызов родительского конструктора
        super().__init__(driver)

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

    # Получить текст заголовка магазина
    def get_shop_header_text(self):
        return self._get_text(self.shop_header)

    # Получить текст заголовка каталога
    def get_shop_title_text(self):
        return self._get_text(self.shop_title)

    # Получить текст названия 1-го продукта
    def get_product_1_name(self):
        return self._get_text(self.product_1_name)

    # Получить тест описания 1-го продукта
    def get_product_1_description(self):
        return self._get_text(self.product_1_description)

    # Получить цену 1-го продукта
    def get_product_1_price(self):
        return self._get_text(self.product_1_price)

    # Получить изображение 1-го продукта
    def get_product_1_image(self):
        return self._get_element(self.product_1_image)

    # Получить количество 1-го продукта
    def get_product_1_quantity(self):
        return self._get_attribute(self.product_1_input, "value")

    # Нажать на кнопку + под 1-м продуктом
    def add_product_1(self):
        value_before = int(self.get_product_1_quantity())
        self._click(self.product_1_button_plus)
        # Ожидание, пока не увеличится на 1
        self._wait_until(lambda d: int(d.find_element(*self.product_1_input).get_attribute("value")) == value_before + 1)

    # Нажать на кнопку - под 1-м продуктом
    def remove_product_1(self):
        value_before = int(self.get_product_1_quantity())
        self._click(self.product_1_button_minus)
        # Ожидание, пока не уменьшится на 1
        self._wait_until(lambda d: int(d.find_element(*self.product_1_input).get_attribute("value")) == value_before - 1)

    # Получить количество товара в корзине
    def get_quantity_goods_in_cart(self):
        return self._get_text(self.quantity_goods_in_cart)

    # Клик по иконке корзины
    def open_cart(self):
        self._click(self.cart_icon)

    # Получить альтернативный текст изображения
    def get_alt_text_image(self):
        return self._get_attribute(self.product_1_image, "alt")