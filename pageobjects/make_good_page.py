# Импорт библиотек
from selenium.webdriver.common.by import By

# Импорт пользовательских библиотек
from base.base_page import BasePage


class MakeGoodPage(BasePage):
    # Конструктор
    def __init__(self, driver):
        # Вызов родительского конструктора
        super().__init__(driver)

        # Локаторы
        self.back_to_goods_button = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[2]/div/a/button")
        self.name = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[1]/input")
        self.description = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[2]/input")
        self.category = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[3]/input")
        self.price = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[5]/input")
        self.url = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[6]/input")
        self.make_good_button = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[2]/div/button")

    # Ввести название нового товара
    def enter_name(self, name):
        self._send_keys(self.name, name)

    # Ввести описание нового товара
    def enter_description(self, description):
        self._send_keys(self.description, description)

    # Ввести категорию нового товара
    def enter_category(self, category):
        self._send_keys(self.category, category)

    # Ввести цену нового товара
    def enter_price(self, price):
        self._send_keys(self.price, price)

    # Ввести url нового товара
    def enter_url(self, url):
        self._send_keys(self.url, url)

    # Клик по кнопке Обратно к товарам
    def back_goods(self):
        self._scroll_and_click(self.back_to_goods_button)

    # Клик по кнопке Создать товар
    def make_good(self):
        self._scroll_and_click(self.make_good_button)