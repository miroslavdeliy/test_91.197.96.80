from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AuthorizationPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        self.username_input = "//*[@id='app']/div/div/div[2]/form/div[1]/input"
        self.password_input = "//*[@id='app']/div/div/div[2]/form/div[2]/input"
        self.login_button = "//*[@id='app']/div/div/div[2]/form/div[3]/button"
        self.auth_header = "//*[@id='app']/div/div/div[1]/div"

    def enter_username(self, username):
        self.driver.find_element(By.XPATH, self.username_input).send_keys(username)


    def enter_password(self, password):
        self.driver.find_element(By.XPATH, self.password_input).send_keys(password)


    def submit(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.login_button))).click()


    def get_auth_header_text(self):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, self.auth_header))).text