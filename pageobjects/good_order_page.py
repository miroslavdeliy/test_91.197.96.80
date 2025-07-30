# Импорт библиотек
from selenium.webdriver.common.by import By

# Импорт пользовательских библиотек
from base.base_page import BasePage


class GoodOrderPage(BasePage):
    # Конструктор
    def __init__(self, driver):
        # Вызов родительского конструктора
        super().__init__(driver)
        self.good_order_title = (
            By.XPATH, "//*[@id='app']/div/div/div[1]/div/div/div[2]"
        )

    # Получение текста успешного завершения заказа
    def get_good_order_page_title(self):
        return self._get_text(self.good_order_title)