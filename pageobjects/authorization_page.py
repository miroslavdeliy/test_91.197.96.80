from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class AuthorizationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

        # Локаторы
        self.username_input = (By.XPATH, "//*[@id='app']//form/div[1]/input")
        self.password_input = (By.XPATH, "//*[@id='app']//form/div[2]/input")
        self.login_button = (By.XPATH, "//*[@id='app']//form/div[3]/button")
        self.auth_header = (By.XPATH, "//*[@id='app']//div[@class='text-h5 font-weight-bold']")

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

    # Функция ввода логина
    def enter_username(self, username):
        self._wait_until(
            EC.visibility_of_element_located(self.username_input)
        ).send_keys(username)

    # Функция ввода пароля
    def enter_password(self, password):
        self._wait_until(
            EC.visibility_of_element_located(self.password_input)
        ).send_keys(password)

    # Функция нажатия на кнопку авторизации
    def click_login_button(self):
        self._wait_until(
            EC.element_to_be_clickable(self.login_button)
        ).click()

    # Получить тест заголовка страницы авторизации
    def get_auth_header_text(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.auth_header)
        ).text

    # Обобщающая функция авторизации
    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()