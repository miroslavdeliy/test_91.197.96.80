from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FinishOrderPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

        # Локаторы
        self.finish_order_title = \
            (By.XPATH, "//*[@id='app']/div/div/div[1]/nav/div/div[1]")
        self.back_shop_button = \
            (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[11]/div/a[1]/button")
        self.name_product = \
            (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[2]/div[2]/div[1]/div")
        self.name = \
            (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[4]/div[1]")
        self.first_name = \
            (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[4]/div[2]")
        self.last_name = \
            (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[4]/div[3]")
        self.address = \
            (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[6]/div[1]")
        self.card_number = \
            (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[8]/div[2]")
        self.quantity_goods = \
            (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[10]/div[1]")
        self.total = \
            (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[10]/div[2]")
        self.finish_order_button = \
            (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[11]/div/a[2]/button")

    # Обработка исключения TimeoutException
    def _wait_until(self, condition, retries=1, timeout=5):
        attempt = 0
        while attempt <= retries:
            try:
                return WebDriverWait(self.driver, timeout).until(condition)
            except TimeoutException:
                attempt += 1
                if attempt > retries:
                    raise

    # Получить текст из элемента
    def _get_text(self, locator):
        return self._wait_until(
            EC.visibility_of_element_located(locator)
        ).text

    # Кликнуть по элементу
    def _click(self, locator):
        self._wait_until(EC.element_to_be_clickable(locator)).click()

    # Получить заголовок страницы подтвержденя заказа
    def get_finish_order_title(self):
        return self._get_text(self.finish_order_title)

    # Нажать на кнопку 'Обратно в магазин'
    def back_shop(self):
        self._click(self.back_shop_button)

    # Получить название товара
    def get_finish_order_name_product(self):
        return self._get_text(self.name_product)

    # Получить Имя
    def get_finish_order_name(self):
        return self._get_text(self.name)

    # Получить Фамилию
    def get_finish_order_first_name(self):
        return self._get_text(self.first_name)

    # Получить Отчество
    def get_finish_order_last_name(self):
        return self._get_text(self.last_name)

    # Получить адрес
    def get_finish_order_address(self):
        return self._get_text(self.address)

    # Получить номер карты
    def get_finish_order_card_number(self):
        return self._get_text(self.card_number)

    # Получить количество товара
    def get_finish_order_quantity_goods(self):
        return self._get_text(self.quantity_goods)

    # Получить общую стоимость
    def get_finish_order_total(self):
        return self._get_text(self.total)

    # Нажать 'Завершить заказ'
    def finish_order(self):
        self._click(self.finish_order_button)