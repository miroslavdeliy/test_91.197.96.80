from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from base.base_page import BasePage


class EditProductPage(BasePage):
    # Конструктор
    def __init__(self, driver):
        # Вызов родительского конструктора
        super().__init__(driver)

        # Локаторы
        self.back_goods_button = (
            By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[2]/div/a/button"
        )
        self.name = (
            By.XPATH,
            "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[2]/"
            "input"
        )
        self.description = (
            By.XPATH,
            "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[3]/"
            "input"
        )
        self.category = (
            By.XPATH,
            "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[4]/"
            "input"
        )
        self.price = (
            By.XPATH,
            "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[6]/"
            "input"
        )
        self.url = (
            By.XPATH,
            "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[7]/"
            "input"
        )
        self.edit_button = (
            By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[2]/div/button"
        )

    # Очистка поля и ввод нового значения
    def _clear_and_send_keys(self, locator, value):
        input_element = self._get_element(locator, condition="visible")
        self._wait_for_value_not_clear(input_element)
        input_element.click()
        input_element.send_keys(Keys.CONTROL + 'a')
        input_element.send_keys(Keys.BACKSPACE)
        input_element.send_keys(value)

    # Ожидание пока поле не заполнится данными
    def _wait_for_value_not_clear(self, element, timeout=5):
        from selenium.webdriver.support.ui import WebDriverWait
        WebDriverWait(
            self.driver, timeout
        ).until(lambda _: element.get_attribute("value") != "")

    # Очистка и ввод нового названия товара
    def clear_and_enter_name(self, name):
        self._clear_and_send_keys(self.name, name)

    # Очистка и ввод нового описания
    def clear_and_enter_description(self, description):
        self._clear_and_send_keys(self.description, description)

    # Очистка и ввод новой категории
    def clear_and_enter_category(self, category):
        self._clear_and_send_keys(self.category, category)

    # Очистка и ввод новой цены
    def clear_and_enter_price(self, price):
        self._clear_and_send_keys(self.price, price)

    # Очистка и ввод нового url изображения
    def clear_and_enter_url(self, url):
        self._clear_and_send_keys(self.url, url)

    # Клик по кнопке Обратно к товарам
    def back_goods(self):
        self._scroll_and_click(self.back_goods_button)

    # Клик по кнопке Обновить товар
    def edit_product(self):
        self._scroll_and_click(self.edit_button)