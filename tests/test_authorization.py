# Импортирование библиотек
import allure
import pytest

# Импортирование пользовательских библиотек
from conftest import driver, user_authorization, admin_authorization
from helpers.assertions import assert_login_successful
from pageobjects.shop_page import ShopPage


class TestAuthorization:
    @allure.title("Проверка входа пользователя с корректными данными в"
                  " {browser_name}")
    @pytest.mark.parametrize("browser_name",
                             ["Mozilla Firefox", "Google Chrome",
                              "Microsoft Edge", "Yandex Browser"])
    def test_user_authorization(self, driver, user_authorization,
                                browser_name):
        allure.dynamic.parameter("Браузер", browser_name)

        with allure.step(f"Открытие страницы магазина в {browser_name}"):
            shop = ShopPage(driver)

        with allure.step("Проверка успешной авторизации пользователя"):
            try:
                assert_login_successful(shop, role="Пользователь")
            except AssertionError as e:
                allure.attach(
                    str(e),
                    name="Текст ошибки",
                    attachment_type=allure.attachment_type.TEXT
                )


    @allure.title("Проверка входа администратора с корректными данными в "
                  "{browser_name}")
    @pytest.mark.parametrize("browser_name",
                             ["Mozilla Firefox", "Google Chrome",
                              "Microsoft Edge", "Yandex Browser"])
    def test_admin_authorization(self, driver, admin_authorization,
                                browser_name):
        allure.dynamic.parameter("Браузер", browser_name)

        with allure.step(f"Открытие страницы магазина в {browser_name}"):
            shop = ShopPage(driver)

        with allure.step("Проверка успешной авторизации администратора"):
            try:
                assert_login_successful(shop, role="Администратор")
            except AssertionError as e:
                allure.attach(
                    str(e),
                    name=f"Текст ошибки",
                    attachment_type=allure.attachment_type.TEXT
                )