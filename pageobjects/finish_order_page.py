from tkinter.font import names

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FinishOrderPageLocations:
    FINISH_ORDER = (By.XPATH, '')


class FinishOrderPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        self.finish_order_title = "//*[@id='app']/div/div/div[1]/nav/div/div[1]"
        self.back_shop_button = "//*[@id='app']/div/div/div[1]/div/div[11]/div/a[1]/button"
        self.name_product = "//*[@id='app']/div/div/div[1]/div/div[2]/div[2]/div[1]/div"
        self.name = "//*[@id='app']/div/div/div[1]/div/div[4]/div[1]"
        self.first_name = "//*[@id='app']/div/div/div[1]/div/div[4]/div[2]"
        self.last_name = "//*[@id='app']/div/div/div[1]/div/div[4]/div[3]"
        self.address = "//*[@id='app']/div/div/div[1]/div/div[6]/div[1]"
        self.card_number = "//*[@id='app']/div/div/div[1]/div/div[8]/div[2]"
        self.quantity_goods = "//*[@id='app']/div/div/div[1]/div/div[10]/div[1]"
        self.total = "//*[@id='app']/div/div/div[1]/div/div[10]/div[2]"
        self.finish_order_button = "//*[@id='app']/div/div/div[1]/div/div[11]/div/a[2]/button"





    def get_finish_order_title(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.finish_order_title))
        ).text


    def back_shop(self):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.back_shop_button))
        ).click()


    def get_finish_order_name_product(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.name_product))
        ).text


    def get_finish_order_name(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH,  self.name))
        ).text


    def get_finish_order_first_name(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.first_name))
        ).text


    def get_finish_order_last_name(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.last_name))
        ).text


    def get_finish_order_address(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.address))
        ).text


    def get_finish_order_card_number(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.card_number))
        ).text


    def get_finish_order_quantity_goods(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.quantity_goods))
        ).text


    def get_finish_order_total(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.total))
        ).text


    def finish_order(self):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.finish_order_button))
        ).click()
