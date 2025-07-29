import allure
import os
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService


from constants import (BASE_URL, USER_LOGIN_1, USER_LOGIN_2, USER_LOGIN_3,
                       USER_LOGIN_4, USER_PASSWORD_1, USER_PASSWORD_2,
                       USER_PASSWORD_3, USER_PASSWORD_4, ADMIN_LOGIN,
                       ADMIN_PASSWORD)
from pageobjects.authorization_page import AuthorizationPage

# Ловить падения тестов
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    # Условие выполняемое при падении теста
    if result.when == "call" and result.failed:
        driver = item.funcargs.get("driver")
        if driver:
            # Скриншот
            try:
                allure.attach(driver.get_screenshot_as_png(), name="screenshot_on_failure", attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                print(f"Не удалось сделать скриншот: {e}")

            # HTML
            try:
                allure.attach(driver.page_source, name="page_source", attachment_type=allure.attachment_type.HTML)
            except Exception as e:
                print(f"Не удалось получить HTML: {e}")

# Фикстура создания драйвера
@pytest.fixture
def driver(browser_name):
    if browser_name == "Google Chrome":
        options = ChromeOptions()
        service = ChromeService()
        driver = webdriver.Chrome(service=service, options=options)

    elif browser_name == "Mozilla Firefox":
        options = FirefoxOptions()
        service = FirefoxService()
        driver = webdriver.Firefox(service=service, options=options)

    elif browser_name == "Microsoft Edge":
        options = EdgeOptions()
        service = EdgeService()
        driver = webdriver.Edge(service=service, options=options)

    elif browser_name == "Yandex Browser":
        driver_path = os.path.join(os.path.dirname(__file__), "yandexdriver.exe")

        # Путь к бинарнику Яндекс Браузера
        binary_path = "C:/Users/miros/AppData/Local/Yandex/YandexBrowser/Application/browser.exe"
        options = ChromeOptions()
        options.binary_location = binary_path

        service = ChromeService(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)

    else:
        raise ValueError(f"Неподдерживаемый браузер: {browser_name}")

    driver.maximize_window()
    driver.get(BASE_URL)
    yield driver
    driver.quit()

# Авторизация пользователя
@pytest.fixture(scope="function")
def user_authorization(driver, browser_name):
    auth_page = AuthorizationPage(driver)
    with allure.step(f"Авторизация пользователя в {browser_name}"):
        if browser_name == "Mozilla Firefox":
            auth_page.login(USER_LOGIN_1, USER_PASSWORD_1)
        elif browser_name == "Google Chrome":
            auth_page.login(USER_LOGIN_2, USER_PASSWORD_2)
        elif browser_name == "Microsoft Edge":
            auth_page.login(USER_LOGIN_3, USER_PASSWORD_3)
        elif browser_name == "Yandex Browser":
            auth_page.login(USER_LOGIN_4, USER_PASSWORD_4)

# Авторизация админа
@pytest.fixture(scope="function")
def admin_authorization(driver):
    auth_page = AuthorizationPage(driver)
    with allure.step("Авторизация администратора"):
        auth_page.login(ADMIN_LOGIN, ADMIN_PASSWORD)

# Мобильный режим
@pytest.fixture
def mobile_driver():
    chrome_options = ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", {"deviceName": "iPhone X"})
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(BASE_URL)
    yield driver
    driver.quit()

# Авторизация в мобильном режиме
@pytest.fixture(scope="function")
def user_authorization_mobile(mobile_driver):
    auth_page = AuthorizationPage(mobile_driver)
    with allure.step(f"Авторизация пользователя мобильном режиме"):
        auth_page.login(USER_LOGIN_1, USER_PASSWORD_1)