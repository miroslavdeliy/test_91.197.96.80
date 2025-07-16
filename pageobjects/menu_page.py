from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MenuPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        self.menu_button = "//*[@id='app']/div/nav/div/button"
        self.cart_link = "//*[@id='offcanvasNavbar']/div[2]/ul[3]/a"
        self.shop_link = "//*[@id='offcanvasNavbar']/div[2]/ul[2]/a"
        self.logout_button = "//*[@id='offcanvasNavbar']/div[2]/ul[4]/li/div"
        self.edit_goods_link = "//*[@id='offcanvasNavbar']/div[2]/ul[1]/a"


    def open_menu(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.menu_button))).click()


    def get_cart_link_text(self):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, self.cart_link))).text


    def open_cart(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.cart_link))).click()


    def get_shop_link_text(self):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, self.shop_link))).text


    def open_shop(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.shop_link))).click()


    def get_logout_button_text(self):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, self.logout_button))).text


    def logout(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.logout_button))).click()


    def open_edit(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.edit_goods_link))).click()