import allure

from constants import MENU_SHOP, MENU_CART, MENU_LOGOUT
from helpers.assertions import assert_text_equal
from pageobjects.menu_page import MenuPage


class TestAdaptability:

    @allure.title("Проверка наличия пунктов меню в мобильном режиме")
    @allure.description("Проверка, что в меню присутствует 'Магазин',"
                        " 'Корзинка', 'Выход'")
    def test_mobile(self, subtests, mobile_driver, user_authorization_mobile):
        with allure.step("Открытие страницы и иницилизация объектов"):
            menu_page = MenuPage(mobile_driver)

        with allure.step("Открыть меню"):
            menu_page.open_menu()

        with allure.step("Получить текст пунктов меню"):
            actual_cart = menu_page.get_cart_link_text().lower()
            actual_shop = menu_page.get_shop_link_text().lower()
            actual_logout = menu_page.get_logout_button_text().lower()

            with allure.step("Проверка наличия пунктов меню в мобильном режиме"):
                expected_shop = MENU_SHOP.lower()
                expected_cart = MENU_CART.lower()
                expected_logout = MENU_LOGOUT.lower()
                data = [
                    ("Корзинка", actual_cart, expected_cart),
                    ("Магазин", actual_shop, expected_shop),
                    ("Выход", actual_logout, expected_logout)
                ]
                for label, actual, expected in data:
                    with allure.step(f"Проверка наличия '{label}' "
                                     f"в меню мобильного режима"):
                        with subtests.test(label=label):
                            assert_text_equal(
                                actual,
                                expected,
                                f"Пункт меню '{label}' не присутствует"
                            )