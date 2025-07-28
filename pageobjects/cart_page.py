# Импорт библиотек
from selenium.webdriver.common.by import By

# Импорт пользовательских библиотек
from base.base_page import BasePage


class CartPage(BasePage):
    # Конструктор
    def __init__(self, driver):
        # Вызов родительского конструктора
        super().__init__(driver)

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

    # Получить текст заголовка корзины
    def get_cart_title_text(self):
        return self._get_text(self.cart_title)

    # Получить текст пустой корзины
    def get_empty_cart_message(self):
        return self._get_text(self.empty_cart_message)

    # Получить текст названия 1-го продукта
    def get_product_1_name(self):
        return self._get_text(self.product_1_name)

    # Получить количество 1-го продукта
    def get_product_1_quantity(self):
        return self._get_attribute(self.product_1_input, "value")

    # Получить цену 1-го продукта
    def get_product_1_price(self):
        return self._get_text(self.product_1_price)

    # Получить общую стоимость
    def get_total(self):
        return self._get_text(self.total)

    # Добавить 1 продукт в корзине
    def add_product_1(self):
        value_before = int(self.get_product_1_quantity())
        self._click(self.product_1_button_plus)
        # Ожидание увеличения количества товара на 1
        self._wait_until(lambda d: int(d.find_element(*self.product_1_input).get_attribute("value")) == value_before + 1)

    # Удалить 1 продукт из корзины
    def remove_product_1(self):
        value_before = int(self.get_product_1_quantity())
        self._click(self.product_1_button_minus)
        # Если до нажатия было больше 1 товара, то ждем уменьшения количества товара на 1
        if value_before > 1:
            self._wait_until(lambda d: int(d.find_element(*self.product_1_input).get_attribute("value")) == value_before - 1)

    # Проверка видимости кнопки совершения заказа
    def is_make_order_button_visible(self):
        return self._get_element(self.make_order_button, condition="present").is_displayed()

    # Проверка активности кнопки совершения заказа
    def is_make_order_button_enabled(self):
        return self._get_element(self.make_order_button, condition="present").is_enabled()

    # Клик по кнопке совершения заказа
    def make_order(self):
        self._click(self.make_order_button)
