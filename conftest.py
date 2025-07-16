import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
import os

from pageobjects.authorization_page import AuthorizationPage
from constants import (USER_LOGIN_1, USER_LOGIN_2, USER_LOGIN_3, USER_LOGIN_4,
                       USER_PASSWORD_1, USER_PASSWORD_2, USER_PASSWORD_3,
                       USER_PASSWORD_4, ADMIN_LOGIN, ADMIN_PASSWORD)

BASE_URL = "http://91.197.96.80/"

@pytest.fixture(scope="function")
def driver(browser_name):
    if browser_name == "firefox":
        options = FirefoxOptions()
        options.headless = False
        driver = webdriver.Firefox(options=options, service=FirefoxService())
    elif browser_name == "chrome":
        options = ChromeOptions()
        options.headless = False
        driver = webdriver.Chrome(options=options, service=ChromeService())
    elif browser_name == "edge":
        options = EdgeOptions()
        options.headless = False
        driver = webdriver.Edge(options=options, service=EdgeService())
    elif browser_name == "yandex":
        # Указать путь к Яндекс.Драйверу, если он не в PATH
        options = ChromeOptions()
        options.headless = False
        driver = webdriver.Chrome(executable_path="/path/to/yandexdriver", options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    driver.maximize_window()
    driver.implicitly_wait(3)

    try:
        driver.get(BASE_URL)
        yield driver
    except Exception as e:
        screenshot_path = f"screenshots/{browser_name}_failed_to_load_main_page.png"
        os.makedirs("screenshots", exist_ok=True)
        driver.save_screenshot(screenshot_path)
        allure.attach.file(screenshot_path, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
        raise e
    finally:
        driver.quit()

# Авторизация пользователя
@pytest.fixture(scope="function")
def user_authorization(driver, browser_name):
    auth_page = AuthorizationPage(driver)
    if browser_name == "firefox":
        auth_page.login(USER_LOGIN_1, USER_PASSWORD_1)
    elif browser_name == "chrome":
        auth_page.login(USER_LOGIN_2, USER_PASSWORD_2)
    elif browser_name == "edge":
        auth_page.login(USER_LOGIN_3, USER_PASSWORD_3)

# Авторизация админа
@pytest.fixture(scope="function")
def admin_authorization(driver):
    auth_page = AuthorizationPage(driver)
    auth_page.login(ADMIN_LOGIN, ADMIN_PASSWORD)