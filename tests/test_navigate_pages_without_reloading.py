# Импортирование библиотек
import allure
import pytest

# Импортирование пользовательских библиотек
from conftest import driver, user_authorization, admin_authorization
from constants import (MENU_CART, MENU_SHOP,
                       MENU_LOGOUT, CART_HEADER_TEXT,
                       SHOP_TITLE_TEXT, AUTH_HEADER_TEXT,
                       EDIT_GOODS_HEADER_TEXT)
from helpers.assertions import assert_text_equal
from pageobjects.authorization_page import AuthorizationPage
from pageobjects.cart_page import CartPage
from pageobjects.edit_goods_page import EditGoodsPage
from pageobjects.menu_page import MenuPage
from pageobjects.shop_page import ShopPage


class TestNavigatePagesWithoutReloading:
    @allure.title("Проверка наличия пунктов меню в {browser_name}")
    @allure.description("Проверка, что в меню присутствует 'Магазин',"
                        " 'Корзинка', 'Выход'")
    @pytest.mark.parametrize("browser_name",
                             ["Mozilla Firefox", "Google Chrome",
                              "Microsoft Edge", "Yandex Browser"])
    def test_menu_visibility(self, subtests, driver, user_authorization,
                             browser_name):
        allure.dynamic.parameter("Браузер", browser_name)

        with allure.step("Открытие страницы и иницилизация объектов"):
            menu = MenuPage(driver)

        with allure.step("Открытие меню"):
            menu.open_menu()

        with allure.step("Получение текста пунктов меню"):
            actual_shop = menu.get_shop_link_text().strip().lower()
            actual_cart = menu.get_cart_link_text().strip().lower()
            actual_logout = menu.get_logout_button_text().strip().lower()

            expected_shop = MENU_SHOP.lower()
            expected_cart = MENU_CART.lower()
            expected_logout = MENU_LOGOUT.lower()

        with allure.step("Проверка наличия пунктов меню"):
            data = [
                ("Корзинка", actual_cart, expected_cart),
                ("Магазин", actual_shop, expected_shop),
                ("Выход", actual_logout, expected_logout)
            ]
            for label, actual, expected in data:
                with subtests.test(label=label):
                    assert_text_equal(
                        actual,
                        expected,
                        f"Пункт меню '{label}' не присутствует"
                    )
                    with allure.step(f"Пункт меню '{label}' присутствует"):
                        pass

        with allure.step("Завершение теста"):
            pass

    @allure.title("Переход в 'Корзинку' без перезагрузки страницы в "
                  "({browser_name})")
    @allure.description(
        "Проверка, что переход в раздел 'Корзинка' не вызывает полной "
        "перезагрузки страницы и заголовок отображается корректно.")
    @pytest.mark.parametrize("browser_name",
                             ["Mozilla Firefox", "Google Chrome",
                              "Microsoft Edge", "Yandex Browser"])
    def test_menu_cart_navigation_no_reload(self, driver, user_authorization,
                                            browser_name):
        allure.dynamic.parameter("Браузер", browser_name)

        with allure.step(f"Открытие страницы и инициализация объектов"):
            menu = MenuPage(driver)
            cart = CartPage(driver)

        with allure.step("Фиксация времени загрузки до перехода"):
            initial_load_time = driver.execute_script(
                "return window.performance.timing.loadEventEnd;"
            )
            allure.attach(str(initial_load_time), name="Initial Load Time",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Открытие меню и переход в 'Корзинку'"):
            menu.open_menu()
            menu.open_cart()

        with allure.step("Проверка заголовка страницы 'Корзинка'"):
            actual_text = cart.get_cart_title_text().strip().lower()
            assert_text_equal(
                actual_text,
                CART_HEADER_TEXT,
                "Переход в корзинку не удался"
            )

        with allure.step("Фиксация времени загрузки после перехода"):
            after_load_time = driver.execute_script(
                "return window.performance.timing.loadEventEnd;"
            )
            allure.attach(str(after_load_time), name="After Load Time",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверка отсутствия полной перезагрузки"):
            assert after_load_time == initial_load_time, \
                "Произошла полная перезагрузка страницы"

        with allure.step("Завершение теста"):
            allure.attach("Пункт меню 'Корзинка' открывает корзину без полной "
                          "перезагрузки страницы",
                          name="End test",
                          attachment_type=allure.attachment_type.TEXT)

    @allure.title("Переход в 'Магазин' без перезагрузки страницы в "
                  "({browser_name})")
    @allure.description(
        "Проверка, что переход в раздел 'Магазин' не вызывает полной "
        "перезагрузки страницы и заголовок отображается корректно.")
    @pytest.mark.parametrize("browser_name",
                             ["Mozilla Firefox", "Google Chrome",
                              "Microsoft Edge", "Yandex Browser"])
    def test_menu_shop_navigation_no_reload(self, driver, user_authorization,
                                            browser_name):
        allure.dynamic.parameter("Браузер", browser_name)

        with allure.step(f"Открытие страницы и инициализация объектов"):
            menu = MenuPage(driver)
            shop = ShopPage(driver)

        with allure.step("Фиксация времени загрузки до перехода"):
            initial_load_time = driver.execute_script(
                "return window.performance.timing.loadEventEnd;"
            )
            allure.attach(str(initial_load_time), name="Initial Load Time",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Открытие меню и переход в 'Магазин'"):
            menu.open_menu()
            menu.open_shop()

        with allure.step("Проверка заголовка страницы 'Магазин'"):
            actual_text = shop.get_shop_title_text().strip().lower()
            assert_text_equal(
                actual_text,
                SHOP_TITLE_TEXT,
                "Переход в магазин не удался"
            )

        with allure.step("Фиксация времени загрузки после перехода"):
            after_load_time = driver.execute_script(
                "return window.performance.timing.loadEventEnd;"
            )
            allure.attach(str(after_load_time), name="After Load Time",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверка отсутствия полной перезагрузки"):
            assert after_load_time == initial_load_time, \
                "Произошла полная перезагрузка страницы"

        with allure.step("Завершение теста"):
            allure.attach("Пункт меню 'Магазин' открывает каталог без полной "
                          "перезагрузки страницы",
                          name="End test",
                          attachment_type=allure.attachment_type.TEXT)

    @allure.title("Переход на страницу авторизации без перезагрузки страницы"
                  " в ({browser_name})")
    @allure.description(
        "Проверка, что переход на страницу авторизации не вызывает полной "
        "перезагрузки страницы и заголовок отображается корректно.")
    @pytest.mark.parametrize("browser_name",
                             ["Mozilla Firefox", "Google Chrome",
                              "Microsoft Edge", "Yandex Browser"])
    def test_menu_exit_navigation_no_reload(self, driver, user_authorization,
                                            browser_name):
        allure.dynamic.parameter("Браузер", browser_name)

        with allure.step(f"Открытие страницы и инициализация объектов"):
            menu = MenuPage(driver)
            auth = AuthorizationPage(driver)

        with allure.step("Фиксация времени загрузки до перехода"):
            initial_load_time = driver.execute_script(
                "return window.performance.timing.loadEventEnd;"
            )
            allure.attach(str(initial_load_time), name="Initial Load Time",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Открытие меню и нажать на 'Выход'"):
            menu.open_menu()
            menu.logout()

        with allure.step("Проверка заголовка страницы авторизации"):
            actual_text = auth.get_auth_header_text().strip().lower()
            assert_text_equal(
                actual_text,
                AUTH_HEADER_TEXT.lower(),
                "Переход в магазин не удался"
            )

        with allure.step("Фиксация времени загрузки после перехода"):
            after_load_time = driver.execute_script(
                "return window.performance.timing.loadEventEnd;"
            )
            allure.attach(str(after_load_time), name="After Load Time",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверка отсутствия полной перезагрузки"):
            assert after_load_time == initial_load_time, \
                "Произошла полная перезагрузка страницы"

        with allure.step("Завершение теста"):
            allure.attach("Пункт меню 'Выход' переводит на страницу "
                          "авторизации без полной перезагрузки страницы",
                          name="End test",
                          attachment_type=allure.attachment_type.TEXT)

    @allure.title("Переход на страницу редактирования товаров без перезагрузки страницы"
                  " в ({browser_name})")
    @allure.description(
        "Проверка, что переход на страницу редактирования товаров не вызывает полной "
        "перезагрузки страницы и заголовок отображается корректно.")
    @pytest.mark.parametrize("browser_name",
                             ["Mozilla Firefox", "Google Chrome",
                              "Microsoft Edge", "Yandex Browser"])
    def test_menu_edit_navigation_no_reload(self, driver, admin_authorization,
                                            browser_name):
        allure.dynamic.parameter("Браузер", browser_name)

        with allure.step(f"Открытие страницы и инициализация объектов"):
            menu = MenuPage(driver)
            edit = EditGoodsPage(driver)

        with allure.step("Фиксация времени загрузки до перехода"):
            initial_load_time = driver.execute_script(
                "return window.performance.timing.loadEventEnd;"
            )
            allure.attach(str(initial_load_time), name="Initial Load Time",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Открытие меню и нажать на 'Редактирование товаров'"):
            menu.open_menu()
            menu.open_edit()

        with allure.step("Проверка заголовка страницы редактирования товаров"):
            actual_text = edit.get_edit_header_text().strip().lower()
            assert_text_equal(
                actual_text,
                EDIT_GOODS_HEADER_TEXT.lower(),
                "Переход в редактирование товаров не удался"
            )

        with allure.step("Фиксация времени загрузки после перехода"):
            after_load_time = driver.execute_script(
                "return window.performance.timing.loadEventEnd;"
            )
            allure.attach(str(after_load_time), name="After Load Time",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверка отсутствия полной перезагрузки"):
            assert after_load_time == initial_load_time, \
                "Произошла полная перезагрузка страницы"

        with allure.step("Завершение теста"):
            allure.attach("Пункт меню 'Редактирование товаров' переводит на страницу "
                          "редактирования без полной перезагрузки страницы",
                          name="End test",
                          attachment_type=allure.attachment_type.TEXT)