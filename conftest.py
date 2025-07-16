import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from pageobjects.authorization_page import AuthorizationPage
from constants import (
    BASE_URL, USER_LOGIN, USER_PASSWORD,
    ADMIN_LOGIN, ADMIN_PASSWORD
)

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

    try:
        auth_page.enter_username(USER_LOGIN)
        auth_page.enter_password(USER_PASSWORD)
        auth_page.submit()

        yield

    except Exception as e:
        driver.save_screenshot("auth_failure.png")
        current_url = driver.current_url
        print(f"Ошибка авторизации. URL после submit: {current_url}")
        raise e


# Авторизация админа в Mozilla Firefox
@pytest.fixture(scope="function")
def admin_authorization_mozilla_firefox(driver_mozilla_firefox):

    driver = driver_mozilla_firefox
    auth_page = AuthorizationPage(driver)

    try:
        auth_page.enter_username(ADMIN_LOGIN)
        auth_page.enter_password(ADMIN_PASSWORD)
        auth_page.submit()

        yield

    except Exception as e:
        driver.save_screenshot("auth_failure.png")
        current_url = driver.current_url
        print(f"Ошибка авторизации. URL после submit: {current_url}")
        raise e