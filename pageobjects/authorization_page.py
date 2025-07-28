# Импорт библиотек
from selenium.webdriver.common.by import By

# Импорт пользовательских библиотек
from base.base_page import BasePage

class AuthorizationPage(BasePage):
    # Конструктор
    def __init__(self, driver):
        # Вызов родительского конструктора
        super().__init__(driver)

        # Локаторы
        self.username_input = (By.XPATH, "//*[@id='app']//form/div[1]/input")
        self.password_input = (By.XPATH, "//*[@id='app']//form/div[2]/input")
        self.login_button = (By.XPATH, "//*[@id='app']//form/div[3]/button")
        self.auth_header = (By.XPATH, "//*[@id='app']/div/div/div[1]/div")

    # Ввод логина
    def enter_username(self, username):
        self._send_keys(self.username_input, username)

    # Ввод пароля
    def enter_password(self, password):
        self._send_keys(self.password_input, password)

    # Клик по кнопке Войти
    def click_login_button(self):
        self._click(self.login_button)

    # Получить текст заголовка страницы авторизации
    def get_auth_header_text(self):
        return self._get_text(self.auth_header)

    # Обобщающая функция входа
    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()