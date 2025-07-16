from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class MenuPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

        # Локаторы
        self.menu_button = (By.XPATH, "//*[@id='app']/div/nav/div/button")
        self.cart_link = (By.XPATH, "//*[@id='offcanvasNavbar']/div[2]/ul[3]/a")
        self.shop_link = (By.XPATH, "//*[@id='offcanvasNavbar']/div[2]/ul[2]/a")
        self.logout_button = (By.XPATH, "//*[@id='offcanvasNavbar']/div[2]/ul[4]/li/div")
        self.edit_goods_link = (By.XPATH, "//*[@id='offcanvasNavbar']/div[2]/ul[1]/a")

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

    # Функция открытия меню
    def open_menu(self):
        self._wait_until(
            EC.element_to_be_clickable(self.menu_button)
        ).click()

    # Функция получения текста пункта меню 'Корзинка'
    def get_cart_link_text(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.cart_link)
        ).text

    # Функция открытия пункта меню 'Корзинка'
    def open_cart(self):
        self._wait_until(
            EC.element_to_be_clickable(self.cart_link)
        ).click()

    # Функция получения текста пункта меню 'Магазин'
    def get_shop_link_text(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.shop_link)
        ).text

    # Функция открытия пункта меню 'Магазин'
    def open_shop(self):
        self._wait_until(
            EC.element_to_be_clickable(self.shop_link)
        ).click()

    # Функция получения текста пункта меню 'Выход'
    def get_logout_button_text(self):
        return self._wait_until(
            EC.visibility_of_element_located(self.logout_button)
        ).text

    # Функция выхода из системы
    def logout(self):
        self._wait_until(
            EC.element_to_be_clickable(self.logout_button)
        ).click()

    # Функция открытия пункта меню 'Редактирование товары'
    def open_edit(self):
        self._wait_until(
            EC.element_to_be_clickable(self.edit_goods_link)
        ).click()