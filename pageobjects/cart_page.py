from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        self.cart_title = "//*[@id='app']/div/div/div[1]/nav/div/div[1]"
        self.empty_cart_message = "//*[@id='app']/div/div/div[1]/div/div[1]/div"
        self.product_1_name = "//*[@id='app']/div/div/div[1]/div/div[1]/div[2]/div[3]/div[1]/div"
        self.product_1_input = "//*[@id='app']/div/div/div[1]/div/div[1]/div[2]/div[3]/div[2]/div[1]/input"
        self.product_1_price = "//*[@id='app']/div/div/div[1]/div/div[1]/div[2]/div[3]/div[2]/div[2]"
        self.product_1_button_plus = "//*[@id='app']/div/div/div[1]/div/div[1]/div[2]/div[3]/div[2]/div[1]/button[2]/span"
        self.product_1_button_minus = "//*[@id='app']/div/div/div[1]/div/div[1]/div[2]/div[3]/div[2]/div[1]/button[1]/span"
        self.total = "//*[@id='app']/div/div/div[1]/div/div[2]/div[1]"
        self.make_order_button = "//*[@id='app']/div/div/div[1]/div/div[2]/div[2]/a/button"


    def get_cart_title_text(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.cart_title))
        ).text


    def get_empty_cart_message(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.empty_cart_message))
        ).text


    def get_product_1_name(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.product_1_name))
        ).text


    def get_product_1_quantity(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.product_1_input))
        ).get_attribute("value")


    def get_product_1_price(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.product_1_price))
        ).text


    def get_total(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.total))
        ).text


    def add_product_1(self):
        input_field = self.driver.find_element(By.XPATH, self.product_1_input)
        value_before = int(input_field.get_attribute("value"))
        self.driver.find_element(By.XPATH, self.product_1_button_plus).click()

        WebDriverWait(self.driver, 5).until(
            lambda d: int(d.find_element(By.XPATH, self.product_1_input).get_attribute("value")) == value_before + 1
        )


    def remove_product_1(self):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.product_1_button_minus))
        ).click()

    def is_make_order_button_visible(self):
        return self.wait.until(
            EC.presence_of_element_located((By.XPATH, self.make_order_button))
        ).is_displayed()


    def is_make_order_button_enabled(self):
        return self.wait.until(
            EC.presence_of_element_located((By.XPATH, self.make_order_button))
        ).is_enabled()


    def make_order(self):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.make_order_button))
        ).click()