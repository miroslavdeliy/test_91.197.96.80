from selenium.webdriver.common.by import By
from base.base_page import BasePage


class EditGoodsPage(BasePage):
    # Конструктор
    def __init__(self, driver):
        # Вызов родительского конструктора
        super().__init__(driver)

        # Локаторы
        self.edit_header = (
            By.XPATH, "//*[@id='app']/div/div/div[1]/nav/div/div[1]"
        )
        self.add_good_button = (
            By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[5]/a/button"
        )
        self.name = (
            By.XPATH,
            "//*[@id='app']/div/div/div[1]/div/div[5]/div[2]/div[1]/div"
        )
        self.description = (
            By.XPATH,
            "//*[@id='app']/div/div/div[1]/div/div[5]/div[2]/div[1]/p"
        )
        self.category = (
            By.XPATH,
            "//*[@id='app']/div/div/div[1]/div/div[5]/div[2]/div[2]/div/div"
        )
        self.price = (
            By.XPATH,
            "//*[@id='app']/div/div/div[1]/div/div[5]/div[2]/div[3]/div/div"
        )
        self.image = (
            By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[5]/div[1]/img"
        )
        self.edit_product_1_button = (
            By.XPATH,
            "//*[@id='app']/div/div/div[1]/div/div[1]/div[3]/a/button/span"
        )
        self.edit_product_5_button = (
            By.XPATH,
            "//*[@id='app']/div/div/div[1]/div/div[5]/div[3]/a/button/span"
        )
        self.delete_product_button = (
            By.XPATH,
            "//*[@id='app']/div/div/div[1]/div/div[5]/div[4]/button/span"
        )

    # Получить текст заголовка страницы редактирования товаров
    def get_edit_header_text(self):
        return self._get_text(self.edit_header)

    # Клик про кнопке Добавить товар
    def add_good(self):
        self._click(self.add_good_button)

    # Получить название товара из списка товаров
    def get_name(self):
        return self._get_text(self.name)

    # Получить описание товара из списка товаров
    def get_description(self):
        return self._get_text(self.description)

    # Получить категорию товаров из списка товаров
    def get_category(self):
        return self._get_text(self.category)

    # Получить цену товара из списка товаров
    def get_price(self):
        return self._get_text(self.price)

    # Получить ссылку на изображение из списка товаров
    def get_image_maked_good(self):
        return self._get_attribute(self.image, "src")

    # Клик по кнопке редактирования 1-го товара
    def open_edit_product_1(self):
        self._click(self.edit_product_1_button)

    # Клик по кнопке редактиварония 5-го товара
    def open_edit_product_5(self):
        self._click(self.edit_product_5_button)

    # Клик по кнопке удаления товара
    def delete_product(self):
        self._click(self.delete_product_button)