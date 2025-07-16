from selenium.common import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MakeGoodPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        self.back_to_goods_button = "//*[@id='app']/div/div/div[1]/div/div[2]/div/a/button"
        self.name = "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[1]/input"
        self.description = "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[2]/input"
        self.category = "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[3]/input"
        self.price = "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[5]/input"
        self.url = "//*[@id='app']/div/div/div[1]/div/div[1]/div/form/div[1]/div[6]/input"
        self.make_good_button = "//*[@id='app']/div/div/div[1]/div/div[2]/div/button"


    # Функция нажатия на кнопку "Обратно к товарам"
    def back_goods(self):

        # Находим элемент
        back_button = self.wait.until(
            EC.presence_of_element_located((By.XPATH, self.back_to_goods_button))
        )

        # Прокручиваем к элементу через JavaScript
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", back_button)

        # Явное ожидание кликабельности
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.back_to_goods_button))
        )

        try:
            back_button.click()
        # Альтернативный клик через JS (если обычный не сработал)
        except ElementNotInteractableException:
            self.driver.execute_script("arguments[0].click();", back_button)


    def enter_name(self, name):
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.name))
        ).send_keys(name)


    def enter_description(self, description):
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.description))
        ).send_keys(description)


    def enter_category(self, expected_category):
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.category))
        ).send_keys(expected_category)


    def enter_price(self, price):
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.price))
        ).send_keys(price)


    def enter_url(self, url):
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.url))
        ).send_keys(url)


    def make_good(self):
        # Находим элемент
        make_good_button = self.wait.until(
            EC.presence_of_element_located((By.XPATH, self.make_good_button))
        )

        # Прокручиваем к элементу через JavaScript
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", make_good_button)

        # Явное ожидание кликабельности
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.make_good_button))
        )

        try:
            make_good_button.click()
        # Альтернативный клик через JS (если обычный не сработал)
        except ElementNotInteractableException:
            self.driver.execute_script("arguments[0].click();", make_good_button)