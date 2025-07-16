from selenium.common import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class EditProductPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        self.back_goods_button = "//*[@id='app']/div/div/div[1]/div/div[2]/div/a/button"
        self.name = "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[2]/input"
        self.description = "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[3]/input"
        self.category = "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[4]/input"
        self.price = "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[6]/input"
        self.url = "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[7]/input"
        self.edit_button = "//*[@id='app']/div/div/div[1]/div/div[2]/div/button"


    def clear_and_enter_name(self, name):
        name_input = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.name))
        )
        name_input.clear()
        name_input.send_keys(name)


    def clear_and_enter_description(self, description):
        description_input = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.description))
        )
        description_input.clear()
        description_input.send_keys(description)


    def clear_and_enter_category(self, expected_category):
        expected_category_input = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.category))
        )
        expected_category_input.clear()
        expected_category_input.send_keys(expected_category)


    def clear_and_enter_price(self, price):
        price_input = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.price))
        )
        price_input.clear()
        price_input.send_keys(price)


    def cleat_and_enter_url(self, url):
        url_input = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.url))
        )
        url_input.clear()
        url_input.send_keys(url)


    def back_goods(self):
        # Находим элемент
        back_button = self.wait.until(
            EC.presence_of_element_located((By.XPATH, self.back_goods_button))
        )

        # Прокручиваем к элементу через JavaScript
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", back_button)

        # Явное ожидание кликабельности
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.back_goods_button))
        )

        try:
            back_button.click()
        # Альтернативный клик через JS (если обычный не сработал)
        except ElementNotInteractableException:
            self.driver.execute_script("arguments[0].click();", back_button)


    def edit_product(self):
        # Находим элемент
        edit_product_button = self.wait.until(
            EC.presence_of_element_located((By.XPATH, self.edit_button))
        )

        # Прокручиваем к элементу через JavaScript
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_product_button)

        # Явное ожидание кликабельности
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.edit_button))
        )

        try:
            edit_product_button.click()
        # Альтернативный клик через JS (если обычный не сработал)
        except ElementNotInteractableException:
            self.driver.execute_script("arguments[0].click();", edit_product_button)