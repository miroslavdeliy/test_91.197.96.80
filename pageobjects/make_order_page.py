# Импорт библиотек
from selenium.webdriver.common.by import By

# Импорт пользовательских библиотек
from base.base_page import BasePage


class MakeOrderPage(BasePage):
    # Конструктор
    def __init__(self, driver):
        # Вызов родительского конструктора
        super().__init__(driver)

        # Локаторы
        self.make_order_header = (
            By.XPATH, "//*[@id='app']/div/div/div[1]/nav/div/div[1]"
        )
        self.back_shop_button = (
            By.XPATH,
            "//*[@id='app']/div/div/div[1]/div/div/form/div[2]/a/button"
        )
        self.name = (
            By.XPATH,
            "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[2]/input"
        )
        self.first_name = (
            By.XPATH,
            "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[3]/input"
        )
        self.last_name = (
            By.XPATH,
            "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[4]/input"
        )
        self.address = (
            By.XPATH,
            "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[5]/input"
        )
        self.card_number = (
            By.XPATH,
            "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[6]/input"
        )
        self.finish_order_button = (
            By.XPATH,
            "//*[@id='app']/div/div/div[1]/div/div/form/div[2]/button"
        )
        self.error_message = (
            By.XPATH,
            "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[1]"
        )

    # Получить текст заголовка заполнения личных данных
    def get_make_order_header_text(self):
        return self._get_text(self.make_order_header)

    # Клик по кнопке Обратно в магазин
    def back_shop(self):
        self._click(self.back_shop_button)

    # Заполнить имя
    def send_name(self, name):
        self._send_keys(self.name, name)

    # Заполнить фамилию
    def send_first_name(self, firstname):
        self._send_keys(self.first_name, firstname)

    # Заполнить отчество
    def send_last_name(self, lastname):
        self._send_keys(self.last_name, lastname)

    # Заполнить адрес
    def send_address(self, address):
        self._send_keys(self.address, address)

    # Заполнить номер карты
    def send_card_number(self, card_number):
        self._send_keys(self.card_number, card_number)

    # Перейти на страницу подтверждения заказа
    def open_finish_order(self):
        self._click(self.finish_order_button)

    # Получить текст ошибки
    def get_error_message(self):
        return self._get_text(self.error_message)