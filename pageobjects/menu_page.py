# Импорт библиотек
from selenium.webdriver.common.by import By

# Импорт пользовательских библиотек
from base.base_page import BasePage


class MenuPage(BasePage):
    # Конструктор
    def __init__(self, driver):
        # Вызов родительского конструктора
        super().__init__(driver)

        # Локаторы
        self.menu_button = (By.XPATH, "//*[@id='app']/div/nav/div/button")
        self.cart_link = (
            By.XPATH, "//*[@id='offcanvasNavbar']/div[2]/ul[3]/a"
        )
        self.shop_link = (
            By.XPATH, "//*[@id='offcanvasNavbar']/div[2]/ul[2]/a"
        )
        self.logout_button = (
            By.XPATH, "//*[@id='offcanvasNavbar']/div[2]/ul[4]/li/div"
        )
        self.edit_goods_link = (
            By.XPATH, "//*[@id='offcanvasNavbar']/div[2]/ul[1]/a"
        )

    # Открыть меню
    def open_menu(self):
        self._click(self.menu_button)

    # Получить текст пункта меню Корзинка
    def get_cart_link_text(self):
        return self._get_text(self.cart_link)

    # Клик по Корзинке
    def open_cart(self):
        self._click(self.cart_link)

    # Получить текст пункта меню Магазин
    def get_shop_link_text(self):
        return self._get_text(self.shop_link)

    # Клик по Магазин
    def open_shop(self):
        self._click(self.shop_link)

    # Получить текст кнопки Выход
    def get_logout_button_text(self):
        return self._get_text(self.logout_button)

    # Клик по Выход
    def logout(self):
        self._click(self.logout_button)

    # Клик по пункту меню Редактирование товаров
    def open_edit(self):
        self._click(self.edit_goods_link)