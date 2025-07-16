from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ShopPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        self.shop_header = "//*[@id='app']/div/nav/div/a[1]"
        self.shop_title = "//*[@id='app']/div/div/div[1]/nav/div/div[1]"
        self.product_1_name = "//*[@id='app']/div/div/div[1]/div/div[1]/div[3]/div"
        self.product_1_description = "//*[@id='app']/div/div/div[1]/div/div[1]/div[3]/p"
        self.product_1_price = "//*[@id='app']/div/div/div[1]/div/div[1]/div[6]"
        self.product_1_image = "//*[@id='app']/div/div/div[1]/div/div[1]/div[1]/img"
        self.product_1_input = "//*[@id='app']/div/div/div[1]/div/div[1]/div[4]/div/input"
        self.product_1_button_plus = "//*[@id='app']/div/div/div[1]/div/div[1]/div[4]/div/button[2]/span"
        self.product_1_button_minus = "//*[@id='app']/div/div/div[1]/div/div[1]/div[4]/div/button[1]/span"
        self.quantity_goods_in_cart = "//*[@id='app']/div/nav/div/a[2]/button/span[2]"
        self.cart_icon = "//*[@id='app']/div/nav/div/a[2]/button/span[1]"


    def get_shop_header_text(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.shop_header))
        ).text


    def get_shop_title_text(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.shop_title))
        ).text


    def get_product_1_name(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.product_1_name))
        ).text


    def get_product_1_description(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.product_1_description))
        ).text


    def get_product_1_price(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.product_1_price))
        ).text


    def get_product_1_image(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.product_1_image))
        )


    def get_product_1_quantity(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.product_1_input))
        ).get_attribute("value")


    def add_product_1(self):
        input_field = self.driver.find_element(By.XPATH, self.product_1_input)
        value_before = int(input_field.get_attribute("value"))
        self.driver.find_element(By.XPATH, self.product_1_button_plus).click()

        WebDriverWait(self.driver, 5).until(
            lambda d: int(d.find_element(By.XPATH, self.product_1_input).get_attribute("value")) == value_before + 1
        )


    def remove_product_1(self):
        input_field = self.driver.find_element(By.XPATH, self.product_1_input)
        value_before = int(input_field.get_attribute("value"))
        self.driver.find_element(By.XPATH, self.product_1_button_minus).click()

        WebDriverWait(self.driver, 5).until(
            lambda d: int(d.find_element(By.XPATH, self.product_1_input).get_attribute("value")) == value_before - 1
        )


    def get_quantity_goods_in_cart(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.quantity_goods_in_cart))
        ).text


    def open_cart(self):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.cart_icon))
        ).click()


    def get_alt_text_image(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.product_1_image))
        ).get_attribute("alt")