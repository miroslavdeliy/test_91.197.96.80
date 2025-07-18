import allure
import pytest



class TestNavigatePagesWithoutReloading:
    # Проверка наличия пунктов меню (с использованием subtests)
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_menu_visibility(self, subtests, driver, user_authorization,
                             browser_name):
        menu = MenuPage(driver)

        print(f"\nПроверка наличия пунктов меню в {browser_name}")

        # Кликаем на кнопку меню
        menu.open_menu()
        print("Меню открыто")

        # Получение фактических названий пунктов меню
        actual_shop = menu.get_shop_link_text().strip().lower()
        actual_cart = menu.get_cart_link_text().strip().lower()
        actual_logout = menu.get_logout_button_text().strip().lower()

        # Подготовка ожидаемых названий
        expected_shop = MENU_SHOP.lower()
        expected_cart = MENU_CART.lower()
        expected_logout = MENU_LOGOUT.lower()

        # Используем subtests — каждый пункт меню проверяется независимо
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
            print(f"Пункт меню {label} присутствует")