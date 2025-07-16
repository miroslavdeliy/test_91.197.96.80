from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MakeOrderPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        self.make_order_header = "//*[@id='app']/div/div/div[1]/nav/div/div[1]"
        self.back_shop_button = "//*[@id='app']/div/div/div[1]/div/div/form/div[2]/a/button"
        self.name = "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[2]/input"
        self.first_name = "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[3]/input"
        self.last_name = "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[4]/input"
        self.address = "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[5]/input"
        self.card_number = "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[6]/input"
        self.finish_order_button = "//*[@id='app']/div/div/div[1]/div/div/form/div[2]/button"
        self.error_message = "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[1]"


    def get_make_order_header_text(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.make_order_header))
        ).text


    def back_shop(self):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.back_shop_button))
        ).click()


    def send_name(self, name):
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.name))
        ).send_keys(name)


    def send_first_name(self, firstname):
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.first_name))
        ).send_keys(firstname)


    def send_last_name(self, lastname):
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.last_name))
        ).send_keys(lastname)


    def send_address(self, address):
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.address))
        ).send_keys(address)


    def send_card_number(self, card_number):
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.card_number))
        ).send_keys(card_number)


    def open_finish_order(self):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.finish_order_button))
        ).click()


    def get_error_message(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.error_message))
        ).text


