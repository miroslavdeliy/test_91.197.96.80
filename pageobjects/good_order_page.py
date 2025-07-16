from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GoodOrderPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        self.good_order_title = "//*[@id='app']/div/div/div[1]/div/div/div[2]"


    def get_good_order_page_title(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.good_order_title))
        ).text