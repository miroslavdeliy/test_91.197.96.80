import pytest

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from constants import (
    BASE_URL, USER_LOGIN, USER_PASSWORD,
    ADMIN_LOGIN, ADMIN_PASSWORD
)
from pageobjects.authorization_page import AuthorizationPage

@pytest.fixture(scope="function")
def driver_mozilla_firefox():
    options = FirefoxOptions()
    options.headless = False

    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    driver.implicitly_wait(3)

    try:
        driver.get(BASE_URL)
        yield driver
    except Exception as e:
        driver.save_screenshot("failed_to_load_main_page.png")  # можно логировать
        raise e
    finally:
        driver.quit()

# Авторизация пользователя в Mozilla Firefox
@pytest.fixture(scope="function")
def user_authorization_mozilla_firefox(driver_mozilla_firefox):
    driver = driver_mozilla_firefox
    auth_page = AuthorizationPage(driver)

    # Авторизация
    auth_page.login(USER_LOGIN, USER_PASSWORD)


# Авторизация админа в Mozilla Firefox
@pytest.fixture(scope="function")
def admin_authorization_mozilla_firefox(driver_mozilla_firefox):

    driver = driver_mozilla_firefox
    auth_page = AuthorizationPage(driver)

    auth_page.login(ADMIN_LOGIN, ADMIN_PASSWORD)