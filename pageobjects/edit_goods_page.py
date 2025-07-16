from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class EditGoodsPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        self.edit_header = "//*[@id='app']/div/div/div[1]/nav/div/div[1]"
        self.add_good_button = "//*[@id='app']/div/div/div[1]/div/div[5]/a/button"
        self.name = "//*[@id='app']/div/div/div[1]/div/div[5]/div[2]/div[1]/div"
        self.description = "//*[@id='app']/div/div/div[1]/div/div[5]/div[2]/div[1]/p"
        self.category = "//*[@id='app']/div/div/div[1]/div/div[5]/div[2]/div[2]/div/div"
        self.price = "//*[@id='app']/div/div/div[1]/div/div[5]/div[2]/div[3]/div/div"
        self.image = "//*[@id='app']/div/div/div[1]/div/div[5]/div[1]/img"
        self.edit_product_button = "//*[@id='app']/div/div/div[1]/div/div[5]/div[3]/a/button/span"
        self.delete_product_button = "//*[@id='app']/div/div/div[1]/div/div[5]/div[4]/button/span"


    def get_edit_header_text(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.edit_header))
        ).text


    def add_good(self):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.add_good_button))
        ).click()


    def get_name(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.name))
        ).text


    def get_description(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.description))
        ).text


    def get_category(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.category))
        ).text


    def get_price(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.price))
        ).text


    def get_image_maked_good(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.image))
        ).get_attribute("src")


    def open_edit_product(self):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.edit_product_button))
        ).click()


    def delete_product(self):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.delete_product_button))
        ).click()