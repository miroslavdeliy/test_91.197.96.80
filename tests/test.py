import pytest


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from conftest import driver, user_authorization, admin_authorization
from constants import (MENU_CART, MENU_SHOP,
                       MENU_LOGOUT, CART_HEADER_TEXT, AUTH_HEADER_TEXT,
                       EDIT_GOODS_HEADER_TEXT, PRODUCT_1_NAME,
                       PRODUCT_1_DESCRIPTION, PRODUCT_1_PRICE,
                       EMPTY_CART_MESSAGE, MAKE_ORDER_HEADER_TEXT,
                       PRODUCTS_HEADER_TEXT, TEST_USER_NAME,
                       TEST_USER_FIRST_NAME, TEST_USER_LAST_NAME,
                       TEST_USER_ADDRESS, TEST_USER_CARD,
                       FINISH_ORDER_HEADER_TEXT, GOOD_ORDER_SUCCESS_TEXT,
                       NEW_GOOD_NAME, NEW_GOOD_DESCRIPTION, NEW_GOOD_CATEGORY,
                       NEW_GOOD_PRICE, NEW_GOOD_IMAGE_URL, EDITED_GOOD_NAME,
                       EDITED_GOOD_DESCRIPTION, EDITED_GOOD_CATEGORY,
                       EDITED_GOOD_PRICE, EDITED_GOOD_IMAGE_URL,
                       MISSING_PERSONAL_DATA_ERROR, MAX_LOAD_TIME_MS,
                       MAX_TOTAL, MAX_QUANTITY)
from helpers.assertions import assert_login_successful, assert_text_equal
from pageobjects.authorization_page import AuthorizationPage
from pageobjects.cart_page import CartPage
from pageobjects.edit_goods_page import EditGoodsPage
from pageobjects.edit_product_page import EditProductPage
from pageobjects.good_order_page import GoodOrderPage
from pageobjects.finish_order_page import FinishOrderPage
from pageobjects.shop_page import ShopPage
from pageobjects.make_good_page import MakeGoodPage
from pageobjects.make_order_page import MakeOrderPage
from pageobjects.menu_page import MenuPage


class TestWebApplication:

    # --- Переход по страницам сайта без перезагрузки ---
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

    # Проверка перехода в раздел Корзинка без перезагрузки
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_menu_cart_navigation_no_reload(self, driver, user_authorization,
                                            browser_name):
        menu = MenuPage(driver)
        cart = CartPage(driver)

        print(f"\nПроверка перехода в раздел"
                    f"'Корзинка' без перезагрузки в {browser_name}")

        # Засекаем время загрузки страницы ДО перехода
        initial_load_time = driver.execute_script(
            "return window.performance.timing.loadEventEnd;"
        )
        print(f"Время до перехода {initial_load_time}")

        # Открываем меню и кликаем по пункту "Корзинка"
        menu.open_menu()
        print("Меню открыто")

        # Кликаем по пункту меню 'Корзинка'
        menu.open_cart()
        print("Клик по пункту меню 'Корзинка'")

        # Проверяем текст заголовка "Корзинки"
        actual_text = cart.get_cart_title_text().strip().lower()
        assert_text_equal(
            actual_text,
            CART_HEADER_TEXT,
            "Переход в корзинку не удался"
        )

        # Засекаем время загрузки страницы ПОСЛЕ перехода
        after_load_time = driver.execute_script(
            "return window.performance.timing.loadEventEnd;"
        )
        print(f"Время после перехода {after_load_time}")

        # Проверка, что не произошла полная перезагрузка страницы
        assert after_load_time == initial_load_time,\
            "Произошла полная перезагрузка страницы"
        print(f"Переход в 'Корзинку' прошел без перезагрузки"
                    f"страницы с корректным заголовком в {browser_name}")

    # Проверка перехода в раздел Магазин без перезагрузки
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_menu_shop_navigation_no_reload(self, driver, user_authorization,
                                            browser_name):
        menu = MenuPage(driver)
        shop = ShopPage(driver)

        print(f"\nПроверка перехода в раздел 'Магазин'"
                    f"без перезагрузки в {browser_name}")

        # Засекаем время загрузки страницы ДО перехода
        initial_load_time = driver.execute_script(
            "return window.performance.timing.loadEventEnd;"
        )
        print(f"Время до перехода {initial_load_time}")

        # Открываем меню
        menu.open_menu()
        print("Меню открыто")

        # Кликаем по пункту меню 'Магазин'
        menu.open_shop()
        print("Клик по пункту меню 'Магазин'")

        # Проверяем текст заголовка "Магазин"
        actual_text = shop.get_shop_title_text().strip().lower()
        assert_text_equal(
            actual_text,
            PRODUCTS_HEADER_TEXT.lower(),
            "Переход в 'Магазин' не удался"
        )

        # Засекаем время загрузки страницы ПОСЛЕ перехода
        after_load_time = driver.execute_script(
            "return window.performance.timing.loadEventEnd;"
        )
        print(f"Время после перехода {after_load_time}")

        # Проверка, что не произошла полная перезагрузка страницы
        assert after_load_time == initial_load_time,\
            "Произошла полная перезагрузка страницы"
        print(f"Переход в 'Магазин' прошел без перезагрузки страницы"
                    f"с корректным заголовком")

    # Проверка кнопки Выход без перезагрузки
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_menu_exit(self, driver, user_authorization,
                       browser_name):
        menu = MenuPage(driver)
        auth = AuthorizationPage(driver)

        print(f"\nПроверка кнопки 'Выход' без перезагрузки в {browser_name}")

        # Засекаем время загрузки страницы ДО выхода
        initial_load_time = driver.execute_script(
            "return window.performance.timing.loadEventEnd;"
        )
        print(f"Время до перехода {initial_load_time}")

        # Открываем меню
        menu.open_menu()
        print("Меню открыто")

        # Кликаем по кнопке 'Выход'
        menu.logout()
        print("Клик по кнопке 'Выход' выполнен")

        # Проверяем текст заголовка
        actual_text = auth.get_auth_header_text().strip().lower()
        assert_text_equal(
            actual_text,
            AUTH_HEADER_TEXT.lower(),
            "Переход на страницу авторизации не выполнен"
        )

        # Засекаем время загрузки страницы ПОСЛЕ перехода
        after_load_time = driver.execute_script(
            "return window.performance.timing.loadEventEnd;"
        )
        print(f"Время после перехода {after_load_time}")

        # Проверка, что не произошла полная перезагрузка страницы
        assert after_load_time == initial_load_time,\
            "Произошла полная перезагрузка страницы"
        print(f"Переход на страницу авторизации прошел без перезагрузки"
                    f"страницы с корректным заголовком")

    # Проверка перехода на страницу редактирования товара
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_edit_goods_button(self, driver, admin_authorization,
                               browser_name):
        menu = MenuPage(driver)
        edit = EditGoodsPage(driver)

        print(f"\nПроверка перехода администратора в"
                    f"'Редактирование: Товары' в {browser_name}")

        # Засекаем время загрузки страницы
        initial_load_time = driver.execute_script(
            "return window.performance.timing.loadEventEnd;"
        )
        print(f"Время до перехода {initial_load_time}")

        # Открываем меню
        menu.open_menu()
        print("Меню открыто")

        # Кликаем по 'Редактировать товары'
        menu.open_edit()
        print("Клик по 'Редактировать товары' выполнен")

        # Проверяем текст заголовка
        actual_text = edit.get_edit_header_text().strip().lower()
        assert_text_equal(
            actual_text,
            EDIT_GOODS_HEADER_TEXT.lower(),
            "Переход на страницу авторизации не выполнен"
        )

        # Засекаем время загрузки страницы ПОСЛЕ перехода
        after_load_time = driver.execute_script(
            "return window.performance.timing.loadEventEnd;"
        )
        print(f"Время после перехода {after_load_time}")

        # Проверка, что не произошла полная перезагрузка страницы
        assert after_load_time == initial_load_time,\
            "Произошла полная перезагрузка страницы"
        print(f"Переход на страницу авторизации прошел без перезагрузки"
                    f"страницы с корректным заголовком")

    # --- Корректность карточки товара ---
    # Проверка отображения данных товара
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_product_card_display(self, subtests, driver, user_authorization,
                                  browser_name):
        shop = ShopPage(driver)

        print(f"\nПроверка отображения карточки товара в {browser_name}")

        # Сохраняем фактические значения карточки товара
        actual_name = shop.get_product_1_name().strip().lower()
        actual_description = shop.get_product_1_description().strip().lower()
        actual_price = shop.get_product_1_price().strip().lower()

        # Подготовка ожидаемых значений
        expected_name = PRODUCT_1_NAME.lower()
        expected_description = PRODUCT_1_DESCRIPTION.lower()
        expected_price = PRODUCT_1_PRICE.lower()

        # Используем subtests — каждый текстовый элемент карточки товара
        # проверяется независимо
        data = [
            ("Название", actual_name, expected_name),
            ("Описание", actual_description, expected_description),
            ("Цена", actual_price, expected_price)
        ]
        for label, actual, expected in data:
            with subtests.test(label=label):
                assert_text_equal(
                    actual,
                    expected,
                    f"{label} товара некорректно"
                )
            print(f"{label} товара отображается корректно")

        # Проверяем картинку
        image = shop.get_product_1_image()
        assert image.get_attribute("src") != "",\
            "Изображение товара не загружено (src-пустой)"
        print("Изображение товара загружено")

    # Проверка работоспособности кнопок
    # изменения количества товара
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_button_changing_quantity_goods(self, subtests, driver,
                                            user_authorization, browser_name):
        shop = ShopPage(driver)

        print(f"\nПроверка работоспособности кнопок"
                    f" изменения количества товара в {browser_name}")

        # Получаем текущее количество (до добавления)
        quantity_before = int(shop.get_product_1_quantity())
        print(f"Изначальное количество {quantity_before}")

        # --- Подтест 1: Увеличение количества товара ---
        shop.add_product_1()
        print("Добавлен один товар")

        # Получаем количество товаров после добавления
        quantity_after_add = int(shop.get_product_1_quantity())
        print(f"Количество товара после добавления:"
                    f"{quantity_after_add}")

        # Проверка увеличения количества товара на 1 штуку
        with subtests.test(label="Добавление товара"):
            assert quantity_after_add == quantity_before + 1, \
                (f"Количество товара не увеличилось. Было: {quantity_before},"
                 f" стало: {quantity_after_add}")
        print(f"Товар успешно добавлен: было {quantity_before},"
                    f" стало {quantity_after_add}")

        # --- Подтест 2: Уменьшение количества товара ---
        shop.remove_product_1()
        print("Удален один товар")

        # Получаем количество товаров после удаления
        quantity_after_remove = int(shop.get_product_1_quantity())
        print(f"Количество товара после удаления:"
                    f" {quantity_after_remove}")

        # Проверка уменьшения количества товара на 1 штуку
        with subtests.test(label="Удаление товара"):
            assert quantity_after_remove == quantity_after_add - 1, \
                (f"Количество товара не уменьшилось. Было:"
                 f" {quantity_after_add}, стало: {quantity_after_remove}")
        print(f"Товар успешно удален: было {quantity_after_add},"
                    f"стало: {quantity_after_remove}")

    # Проверка видимости изменения количества товара в корзине
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_visibility_changing_quantity_goods_in_cart(self, subtests, driver,
                                            user_authorization, browser_name):
        shop = ShopPage(driver)

        print(f"Проверка отображения товаров в корзине в {browser_name}")

        # Сохраняем текущее количество товара в корзине
        quantity_before = int(shop.get_quantity_goods_in_cart())
        print(f"Текущее количество товаров в корзине:{quantity_before}")

        # --- Подтест 1: Увеличение количества товара в корзине ---
        shop.add_product_1()
        print("Товар добавлен в корзину")

        quantity_after_add = int(shop.get_product_1_quantity())
        print(f"Количество товара после добавления: {quantity_after_add}")

        with subtests.test(label="Добавление товара в корзину"):
            assert quantity_after_add == quantity_before + 1, \
                (f"Количество не увеличилось. Было: {quantity_before},"
                 f"стало: {quantity_after_add}")
        print(f"Товар успешно добавлен: было {quantity_before},"
                    f"стало {quantity_after_add}")

        # --- Подтест 2: Уменьшение количества товара в корзине ---
        shop.remove_product_1()
        print("Товар удалён из корзины")

        # Получаем количество товаров после удаления
        quantity_after_remove = int(shop.get_product_1_quantity())
        print(f"Количество товара после удаления: {quantity_after_remove}")

        with subtests.test(label="Удаление товара из корзины"):
            assert quantity_after_remove == quantity_after_add - 1, \
                (f"Количество не уменьшилось. Было: {quantity_after_add}, "
                 f"стало: {quantity_after_remove}")
        print(f"Товар успешно удалён: было {quantity_after_add}, "
                    f"стало {quantity_after_remove}")

    # --- Корректность корзины ---
    # Проверка корректного отображения товаров в корзине
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_cart_items_display(self, subtests, driver, user_authorization,
                                browser_name):
        shop = ShopPage(driver)
        cart = CartPage(driver)

        print(f"Проверка корректного отображения товаров "
                    f"в корзине в {browser_name}")

        # Добавляем товар в корзину
        shop.add_product_1()
        print("Товар добавлен")

        # Переход в корзину
        shop.open_cart()
        print("Клик иконке 'Корзинка'")

        # Получение фактических значений
        actual_name = cart.get_product_1_name().strip().lower()
        actual_quantity = int(cart.get_product_1_quantity())
        actual_price = cart.get_product_1_price().strip().lower()

        # Подготовка ожидаемых значений
        expected_name = PRODUCT_1_NAME.lower()
        expected_quantity = 1
        expected_price = PRODUCT_1_PRICE.lower()

        # Список под-тестов:
        data = [
            ("Название товара", actual_name, expected_name, assert_text_equal),
            ("Количество товара", actual_quantity, expected_quantity, None),
            ("Цена товара", actual_price, expected_price, assert_text_equal),
        ]
        for label, actual, expected, custom_assert in data:
            with ((subtests.test(label=label))):
                if custom_assert:
                    custom_assert(
                        actual,
                        expected,
                        f"{label} некорректно отображается в корзине"
                    )
                else:
                    assert actual == expected,\
                    f"{label}некорректно: {actual} ≠ {expected}"
                print(f"{label} в корзине отображается корректно")

    # Проверка корректного пересчета итоговой цены в корзине
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_cart_price_recalculation(self, driver, user_authorization,
                                      browser_name):
        shop = ShopPage(driver)
        cart = CartPage(driver)

        print(f"Проверка корректного пересчета итоговой "
                    f"цены в корзине в {browser_name}")

        # Переход в корзину
        shop.open_cart()
        print("Клик по пункту меню 'Корзинка'")

        # Сохранить количество товара в корзине ДО добавления
        quantity_before_add = int(cart.get_product_1_quantity())
        print(f"Количество товара: {quantity_before_add} в корзине")

        # Сохранить цену товара
        price = float(cart.get_product_1_price().split()[0])
        print(f"Цена товара {price}")

        # Сохранить итоговую цену ДО добавления товара
        total_1 = float(cart.get_total().split()[-2])
        print(f'Итоговая цена: {total_1} в корзине')

        # Добавить один товар в корзину
        cart.add_product_1()
        print("Товар добавлен в корзину")

        # Сохранить количество товара ПОСЛЕ добавления
        quantity_after_add = int(cart.get_product_1_quantity())
        print(f"Количества товара после добавления: {quantity_after_add}"
                    f" в корзине")

        # Проверка корректного пересчета итоговой цены
        total_2 = float(cart.get_total().split()[-2])
        print(f"Итоговая цена после добавления товара: {total_2} в "
                    f"корзине")

        assert total_2 == price * quantity_after_add,\
            "Итоговая цена пересчитывается некорректно"
        print("Итоговая цена пересчиталась корректно")

    # Проверка очистки корзины
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_clear_cart(self, driver, user_authorization, browser_name):
        shop = ShopPage(driver)
        cart = CartPage(driver)

        print(f"Проверка очистки корзины в {browser_name}")

        # Переход в корзину
        shop.open_cart()
        print("Клик по иконке 'Корзинка'")

        # Сохранить количество товара в корзине ДО очистки
        quantity_before_clear = int(cart.get_product_1_quantity())
        print(f"Количество товара: {quantity_before_clear} в корзине")

        # Уменьшать количество товара в корзине до очистки
        for _ in range(quantity_before_clear):
            cart.remove_product_1()
        print("Корзина очистилась")

        # Проверка корректности сообщения о пустой корзине
        empty_cart_message = cart.get_empty_cart_message().strip().lower()
        assert_text_equal(
            empty_cart_message,
            EMPTY_CART_MESSAGE.lower(),
            "Корзина не очистилась!"
        )
        print("Сообщение о пустой корзине корректно")

    # Проверка неактивности кнопки 'Оформить заказ' при пустой корзине
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_make_order_button_disabled_when_cart_empty(self, driver,
                                                        user_authorization,
                                                        browser_name):
        shop = ShopPage(driver)
        cart = CartPage(driver)

        print(f"Проверка неактивности кнопки 'Оформить заказ' при пустой "
              f"корзине в {browser_name}")

        # Переход в корзину
        shop.open_cart()
        print("Клик по иконке 'Корзинка'")

        # Проверяем недоступность кнопки "Оформить заказ"
        is_visible = cart.is_make_order_button_visible()
        if not is_visible:
            print("Кнопка 'Оформить заказ' не видима при пустой "
                        "корзине")
        else:
            is_enabled = cart.is_make_order_button_enabled()
            assert not is_enabled, ("Кнопка 'Оформить заказ' активна при "
                                    "пустой корзине")

    # Проверка активности кнопки Оформить заказ при непустой корзине
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_make_order_button_enabled(self, driver, user_authorization,
                                       browser_name):
        shop = ShopPage(driver)
        cart = CartPage(driver)

        print(f"Проверка активности кнопки 'Оформить заказ' при непустой "
              f"корзине в {browser_name}")

        # Добавляем товар
        shop.add_product_1()
        print("Товар добавлен в корзину")

        # Переход в корзину
        shop.open_cart()
        print("Клик по иконке 'Корзинка'")

        # Проверяем доступность кнопки "Оформить заказ"
        is_visible = cart.is_make_order_button_visible()
        if is_visible:
            print("Кнопка 'Оформить заказ' видна при непустой корзине")
            is_enabled = cart.is_make_order_button_enabled()
            assert is_enabled, ("Кнопка 'Оформить заказ' неактивна "
                                "при непустой корзине")
            print("Кнопка 'Оформить заказ' активна при непустой корзине")
        else:
            print("Кнопка 'Оформить заказ' не видима при пустой корзине")

    # --- Оформление и совершение заказа ---
    # Проверка перенаправления на страницу заполнения личных
    # данных при нажатии на кнопку Оформить заказ
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_making_order_button_work(self, driver, user_authorization,
                                      browser_name):
        shop = ShopPage(driver)
        cart = CartPage(driver)
        make_order = MakeOrderPage(driver)

        print(f"Тест-кейс 16: Проверка перенаправления на страницу "
              f"заполнения личных данных при нажатии на кнопку "
              f"Оформить заказ в {browser_name}")

        # Переход в корзину
        shop.open_cart()
        print("Клик по иконке 'Корзинка'")

        # Нажать на кнопку Офомить заказ
        cart.make_order()
        print("Клик по кнопке 'Оформить заказ'")

        # Проверка нахождения на странице ввода личных данных
        making_order_text = make_order.get_make_order_header_text().lower()
        assert_text_equal(
            making_order_text,
            MAKE_ORDER_HEADER_TEXT.lower(),
            "Кнопка Оформить заказ не переводит на страницу заполнения данных"
        )
        print("Кнопка Оформить заказ переводит на страницу "
                    "заполнения личных данных")

    # Проверка перенаправления на страницу каталога
    # со страницы заполнения личных данных при нажатии на кнопку
    # Обратно в магазин
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_button_back_to_shop_from_personal_page(self, driver,
                                                    user_authorization,
                                                    browser_name):
        shop = ShopPage(driver)
        cart = CartPage(driver)

        print(
            f"Проверка перенаправления на страницу каталога"
            f"со страницы заполнения личных данных при нажатии на кнопку"
            f" 'Обратно в магазин' в {browser_name}"
        )

        # Переход в корзину
        shop.open_cart()
        print("Клик по иконке 'Корзинка'")

        # Нажать на кнопку Офомить заказ
        cart.make_order()
        print("Нажата кнопка 'Оформить заказ'")
        make_order = MakeOrderPage(driver)

        # Нажать на кнопку Обратно к товарам
        make_order.back_shop()
        print("Нажата кнопка 'Обратно в магазин'")

        # Проверка нахождения на каталоге
        catalog_text = shop.get_shop_title_text().strip().lower()
        assert_text_equal(
            catalog_text,
            PRODUCTS_HEADER_TEXT.lower(),
            "Кнопка Обратно в магазин не переводит на страницу каталога"
        )

        print("Кнопка 'Обратно в магазин' переводит на страницу каталога")

    # Проверка перенаправления на страницу подтверждения заказа
    # после заполнения личных данных
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_making_order(self, driver, user_authorization, browser_name):
        shop = ShopPage(driver)
        cart = CartPage(driver)
        make_order = MakeOrderPage(driver)
        finish_order = FinishOrderPage(driver)

        print(f"Проверка перенаправления на страницу "
              f"подтверждения заказа после заполнения личных данных "
              f"{browser_name}")

        # Переход в корзину
        shop.open_cart()
        print("Совершен переход в корзину")

        # Нажать на кнопку Оформить заказ
        cart.make_order()
        print("Нажата кнопка 'Оформить заказ'")

        # Заполнение личной информации
        make_order.send_name(TEST_USER_NAME)
        make_order.send_first_name(TEST_USER_FIRST_NAME)
        make_order.send_last_name(TEST_USER_LAST_NAME)
        make_order.send_address(TEST_USER_ADDRESS)
        make_order.send_card_number(TEST_USER_CARD)
        print("Заполнена личная информация")

        # Нажать на кнопку Завершить заказ
        make_order.open_finish_order()
        print("Нажата кнопка 'Оформить заказ'")

        # Проверка нахождения на странице подтверждения заказа
        make_order_check = finish_order.get_finish_order_title().strip().lower()
        assert_text_equal(
            make_order_check,
            FINISH_ORDER_HEADER_TEXT.lower(),
            "Пользователь не попадает на страницу подтверждения заказа"
        )
        print("Пользователь попадает на страницу подтверждения "
                    "оформления заказа")

    # Проверка перенаправления на страницу каталога со страницы
    # подтверждения заказа при нажатии на кнопку Обратно в магазин
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_back_to_shop_from_order(self, driver, user_authorization,
                                     browser_name):
        shop = ShopPage(driver)
        cart = CartPage(driver)
        make_order = MakeOrderPage(driver)
        finish_order = FinishOrderPage(driver)

        print(f"Проверка перенаправления на страницу "
                    f"каталога со страницы подтверждения заказа при нажатии"
                    f" на кнопку Обратно в магазин в {browser_name}")

        # Переход в корзину
        shop.open_cart()
        print("Совершен переход в корзину")

        # Нажать на кнопку Оформить заказ
        cart.make_order()
        print("Нажата кнопка 'Оформить заказ'")

        # Заполнение личной информации
        make_order.send_name(TEST_USER_NAME)
        make_order.send_first_name(TEST_USER_FIRST_NAME)
        make_order.send_last_name(TEST_USER_LAST_NAME)
        make_order.send_address(TEST_USER_ADDRESS)
        make_order.send_card_number(TEST_USER_CARD)
        print("Заполнена личная информация")

        # Нажать на кнопку Завершить заказ
        make_order.open_finish_order()
        print("Нажата кнопка 'Оформить заказ'")

        # Нажать на кнопку Обратно в магазин
        finish_order.back_shop()
        print("Нажата кнопка 'Обратно в магазин'")

        # Проверка нахождения на странице каталога
        shop_text = shop.get_shop_title_text().strip().lower()
        assert_text_equal(
            shop_text,
            PRODUCTS_HEADER_TEXT,
            "Кнопка Обратно в магазин не переводит в каталог"
        )
        print("Кнопка 'Обратно в магазин' переводит в каталог")

    # Проверка корректности данных на странице подтверждения заказа
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_correct_data_order_page(self, subtests,
                                     driver, user_authorization, browser_name):
        shop = ShopPage(driver)
        cart = CartPage(driver)
        make_order = MakeOrderPage(driver)
        finish_order = FinishOrderPage(driver)

        print(f"Проверка корректности данных на странице "
                    f"подтверждения заказа в {browser_name}")

        # Переход в корзину
        shop.open_cart()
        print("Совершен переход в корзину")

        # Сохраняем количество и сумму до оформления
        quantity_goods_in_cart = cart.get_product_1_quantity()
        total_in_cart = cart.get_total()

        # Оформляем заказ
        cart.make_order()
        print("Нажата кнопка 'Оформить заказ'")

        # Заполняем личную информацию
        make_order.send_name(TEST_USER_NAME)
        make_order.send_first_name(TEST_USER_FIRST_NAME)
        make_order.send_last_name(TEST_USER_LAST_NAME)
        make_order.send_address(TEST_USER_ADDRESS)
        make_order.send_card_number(TEST_USER_CARD)
        print("Заполнена личная информация")

        # Нажать кнопку 'Оформить заказ'
        make_order.open_finish_order()
        print("Нажата кнопка 'Оформить заказ'")

        # Получаем фактические значения с формы подтверждения
        actual_name_product= (finish_order.get_finish_order_name_product()
                              .strip().lower())
        actual_name = (finish_order.get_finish_order_name()
                       .strip().lower())
        actual_first_name = (finish_order.get_finish_order_first_name()
                             .strip().lower())
        actual_finish_name = (finish_order.get_finish_order_last_name()
                              .strip().lower())
        actual_address = (finish_order.get_finish_order_address()
                          .strip().lower())
        actual_card = (finish_order.get_finish_order_card_number()
                       .strip().lower())
        actual_quantity_goods = (finish_order.get_finish_order_quantity_goods()
                                 .strip().lower())

        # Подготавливаем ожидаемые значения
        expected_name_product = PRODUCT_1_NAME.lower()
        expected_name = f"имя: {TEST_USER_NAME}".lower()
        expected_first_name = f"фамилия: {TEST_USER_FIRST_NAME}".lower()
        expected_finish_name = f"отчество: {TEST_USER_LAST_NAME}".lower()
        expected_address = f"адрес доставки: {TEST_USER_ADDRESS}".lower()
        expected_card = f"номер карты: {TEST_USER_CARD}".lower()
        expected_quantity_goods = (f"количество товаров: "
                                   f"{quantity_goods_in_cart}")

        data = [
            ("Название товара", actual_name_product, expected_name_product,
             assert_text_equal),
            ("Имя", actual_name, expected_name, assert_text_equal),
            ("Фамилия", actual_first_name, expected_first_name,
             assert_text_equal),
            ("Отчество", actual_finish_name, expected_finish_name,
             assert_text_equal),
            ("Адрес доставки", actual_address, expected_address,
             assert_text_equal),
            ("Номер карты", actual_card, expected_card, assert_text_equal),
            ("Количество товаров", actual_quantity_goods,
             expected_quantity_goods, assert_text_equal),
        ]

        # Проверка текстовых данных с использованием subtests
        for label, actual, expected, custom_assert in data:
            with subtests.test(label=label):
                custom_assert(actual, expected, f"{label} "
                                                f"некорректно отображается")
                print(f"{label} отображается корректно")

        # Проверка итоговой суммы — сравниваем числовые значения
        total_order = float(finish_order.get_finish_order_total().split()[-2])
        expected_total = float(total_in_cart.split()[-2])
        with subtests.test(label="Итоговая сумма"):
            assert total_order == expected_total, \
                f"Итоговая сумма некорректна: {total_order} ≠ {expected_total}"
            print("Итоговая сумма корректна")

    # Проверка успешного оформления заказа
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_good_make_order(self, driver, user_authorization, browser_name):
        shop = ShopPage(driver)
        cart = CartPage(driver)
        make_order = MakeOrderPage(driver)
        finish_order = FinishOrderPage(driver)
        good_order = GoodOrderPage(driver)

        print(f"Проверка успешного оформления заказа в {browser_name}")

        # Переход в корзину
        shop.open_cart()
        print("Совершен переход в корзину")

        # Нажать на кнопку Оформить заказ
        cart.make_order()
        print("Нажата кнопка 'Оформить заказ'")

        # Заполнение личной информации
        make_order.send_name(TEST_USER_NAME)
        make_order.send_first_name(TEST_USER_FIRST_NAME)
        make_order.send_last_name(TEST_USER_LAST_NAME)
        make_order.send_address(TEST_USER_ADDRESS)
        make_order.send_card_number(TEST_USER_CARD)
        print("Заполнена личная информация")

        # Нажать на кнопку Завершить заказ
        make_order.open_finish_order()
        print("Нажата кнопка 'Оформить заказ'")

        # Нажать на кнопку "Завершить заказ"
        finish_order.finish_order()
        print("Нажата кнопка 'Завершить заказ'")

        # Проверка сообщения об успешном оформлении заказа
        good_order_text = good_order.get_good_order_page_title().strip().lower()
        assert_text_equal(
            good_order_text,
            GOOD_ORDER_SUCCESS_TEXT.lower(),
            "Заказ не оформляется"
        )

        print("Заказ успешно оформляется")

    # --- Профиль администратора ---
    # Проверка кнопки Обратно к товарам на странице создания и редактирования товаров
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_button_back(self, driver, admin_authorization,
                                        browser_name):
        menu = MenuPage(driver)
        edit = EditGoodsPage(driver)
        make_good = MakeGoodPage(driver)
        edit_product = EditProductPage(driver)

        print(f"Проверка кнопки Обратно к товарам на "
                    f"странице создания и редактирования"
              f" товаров в {browser_name}")

        # Нажать иконку меню
        menu.open_menu()
        print("Открылось меню")

        # Нажать Редактирование товаров
        menu.open_edit()
        print("Перешли на страницу редактирования товаров")

        # Нажать кнопку добавления товара
        edit.add_good()
        print("Перешли на страницу создания нового товара")

        # Нажать кнопку Обратно к товарам
        make_good.back_goods()
        print("Нажата кнопка 'Обратно к товарам'")

        # Проверка нахождения на странице редактирования товаров
        edit_header_text_1 = edit.get_edit_header_text().strip().lower()
        assert_text_equal(
            edit_header_text_1,
            EDIT_GOODS_HEADER_TEXT.lower(),
            "Кнопка Обратно к товарам не переводит на страницу списка товаров"
        )
        print("Кнопка Обратно к товарам переводит на страницу"
              " списка товаров со страницы создания товара")

        edit.open_edit_product_1()
        print("Перешли на страницу редактирования конкретного товара")

        # Нажать кнопку Обратно к товарам
        edit_product.back_goods()
        print("Нажали кнопку 'Обратно к товарам'")


        edit_header_text_2 = edit.get_edit_header_text().strip().lower()
        assert_text_equal(
            edit_header_text_2,
            EDIT_GOODS_HEADER_TEXT.lower(),
            "Кнопка Обратно к товарам не переводит на страницу списка товаров"
        )

        print("Кнопка 'Обратно к товарам' переводит на страницу списка "
                    "товаров со страницы редактирования товара")

    # Проверка корректного создания редактирования и удаления товаров
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_make_edit_delete_good(self, subtests, driver,
                        admin_authorization, browser_name):
        menu = MenuPage(driver)
        edit = EditGoodsPage(driver)
        make_good = MakeGoodPage(driver)
        edit_product = EditProductPage(driver)

        print(f"Проверка корректного создания товара в {browser_name}")

        # Открытие меню и переход к созданию товара
        menu.open_menu()
        print("Открылось меню")

        # Клик на 'Редактирование товаров'
        menu.open_edit()
        print("Перешли на страницу редактирования товаров")

        # Клик на 'Добавить товар'
        edit.add_good()
        print("Перешли на страницу создания нового товара")

        # Заполнение формы нового товара
        make_good.enter_name(NEW_GOOD_NAME)
        make_good.enter_description(NEW_GOOD_DESCRIPTION)
        make_good.enter_category(NEW_GOOD_CATEGORY)
        make_good.enter_price(NEW_GOOD_PRICE)
        make_good.enter_url(NEW_GOOD_IMAGE_URL)

        # Клик на 'Создать товар'
        make_good.make_good()
        print("Товар создан")

        # Получение фактических значений
        actual_name_maked_good = edit.get_name().strip().lower()
        actual_description_maked_good = edit.get_description().strip().lower()
        actual_category_maked_good = edit.get_category().strip().lower()
        actual_price_maked_good = edit.get_price().strip().lower()
        actual_image_url_maked_good = edit.get_image_maked_good()

        # Подготовка ожидаемых значений
        expected_name_maked_good = NEW_GOOD_NAME.lower()
        expected_description_maked_good = NEW_GOOD_DESCRIPTION.lower()
        expected_category_maked_good = (f"категория: {NEW_GOOD_CATEGORY}").lower()
        expected_price_maked_good = (f"цена: {NEW_GOOD_PRICE}.00 ₽").lower()
        expected_image_url_maked_good = NEW_GOOD_IMAGE_URL

        # Подготовка проверок
        data_maked_goods = [
            ("Название", actual_name_maked_good, expected_name_maked_good),
            ("Описание", actual_description_maked_good, expected_description_maked_good),
            ("Категория", actual_category_maked_good, expected_category_maked_good),
            ("Цена", actual_price_maked_good, expected_price_maked_good),
            ("URL изображения", actual_image_url_maked_good, expected_image_url_maked_good),
        ]

        # Подтесты с assert_text_equal
        for label, actual, expected in data_maked_goods:
            with subtests.test(label=label):
                assert_text_equal(actual, expected,
                                  f"{label} товара создается некорректно")
                print(f"{label} товара создается корректно")

        print(f"Проверка редактирования созданного товара в {browser_name}")

        # Нажать иконку редактирование конкретного товара
        edit.open_edit_product_5()
        print("Клик по иконке редактирования созданного товара")

        # Внести новые значения в форму
        edit_product.clear_and_enter_name(EDITED_GOOD_NAME)
        edit_product.clear_and_enter_description(EDITED_GOOD_DESCRIPTION)
        edit_product.clear_and_enter_category(EDITED_GOOD_CATEGORY)
        edit_product.clear_and_enter_price(EDITED_GOOD_PRICE)
        edit_product.clear_and_enter_url(EDITED_GOOD_IMAGE_URL)

        # Сохранить изменения
        edit_product.edit_product()
        print("Товар отредактирован")

        # Получить отредактированные значения с интерфейса
        actual_name_edidded_good = edit.get_name().strip().lower()
        actual_description_edidded_good = edit.get_description().strip().lower()
        actual_category_edidded_good = edit.get_category().strip().lower()
        actual_price_edidded_good = edit.get_price().strip().lower()
        actual_image_url_edidded_good = edit.get_image_maked_good()

        # Подготовить ожидаемые значения
        expected_name_edidded_good = EDITED_GOOD_NAME.lower()
        expected_description_edidded_good = EDITED_GOOD_DESCRIPTION.lower()
        expected_category_edidded_good = f"категория: {EDITED_GOOD_CATEGORY}".lower()
        expected_price_edidded_good = f"цена: {EDITED_GOOD_PRICE}.00 ₽".lower()
        expected_image_url_edidded_good = EDITED_GOOD_IMAGE_URL

        # Подготовка проверок
        data_edidded_good = [
            ("Название", actual_name_edidded_good, expected_name_edidded_good),
            ("Описание", actual_description_edidded_good, expected_description_edidded_good),
            ("Категория", actual_category_edidded_good, expected_category_edidded_good),
            ("Цена", actual_price_edidded_good, expected_price_edidded_good),
            ("URL изображения", actual_image_url_edidded_good, expected_image_url_edidded_good),
        ]

        # Подтесты с assert_text_equal
        for label, actual, expected in data_edidded_good:
            with subtests.test(label=label):
                assert_text_equal(actual, expected,
                                  f"{label} товара редактируется некорректно")
                print(f"{label} товара редактируется корректно")

        print(f"Проверка удаления созданного товара в {browser_name}")

        # Сохранить название товара
        good_name = edit.get_name()
        edit.delete_product()
        print(f"Нажата кнопка удаления товара {good_name}")

        # Ожидаем исчезновения конкретного товара
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located(
                (By.XPATH, f'//div[contains(text(), "{good_name}")]'))
        )
        print("Товар исчез из списка")


    # 9 Негативные сценарии
    # Проверка добавления количества товара больше максимального
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_more_max_goods(self, driver, user_authorization,
                            browser_name):
        shop = ShopPage(driver)

        print(f"Тест-кейс 27: Проверка добавления количества товара "
                    f"больше максимального в {browser_name}")

        # Кликнуть на кнопку добавления товаров на 1 раз больше максимального
        for _ in range(MAX_QUANTITY + 1):
            shop.add_product_1()

        # Проверка, что в корзине не больше 100 штук
        count_goods = shop.get_quantity_goods_in_cart()
        assert int(count_goods) <= MAX_QUANTITY, \
            f"В корзину добавляется больше {MAX_QUANTITY} единиц товара"
        print(f"В корзину добавляется не более {MAX_QUANTITY} единиц товара")

    # Проверка добавления товаров на стоимость больше максимальной
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_more_max_total(self, driver, user_authorization,
                            browser_name):
        shop = ShopPage(driver)
        cart = CartPage(driver)

        print("Проверка добавления товаров на стоимость "
                    "больше максимальной")

        # Переход в корзину
        shop.open_cart()
        print("Совершен переход в корзину")

        current_total = 0
        while current_total <= MAX_TOTAL:
            cart.add_product_1()
            current_total = int(cart.get_total().split()[-2])

        assert current_total <= MAX_TOTAL, \
            "Итоговая сумма корзины больше максимальной"
        print("Итоговая сумма не превышает максимальной")

    # Проверка оформления заказа без заполнения личных данных
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_without_personal_data(self, driver, user_authorization,
                                   browser_name):
        shop = ShopPage(driver)
        cart = CartPage(driver)
        make_order = MakeOrderPage(driver)

        print(f"Проверка оформления заказа без заполнения личных данных в "
              f"{browser_name}")

        # Переход в корзину
        shop.open_cart()
        print("Совершен переход в корзину")

        # Нажать на кнопку Офомить заказ
        cart.make_order()
        print("Совершен переход на страницу заполнения личных данных")

        # Нажать на кнопку Оформить заказ
        make_order.open_finish_order()
        print("Нажата кнопка 'Оформить заказ'")

        # Сохранить текст сообщения об ошибке
        error_message = make_order.get_error_message().strip().lower()
        assert_text_equal(
            error_message,
            MISSING_PERSONAL_DATA_ERROR.lower(),
            "Тест провален! Текст сообщения об ошибке некорректный"
        )
        print("Текст сообщения об ошибке корректный")

    # 10 Производительность
    # Проверка времени загрузки главной страницы
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_time_load(self, driver, browser_name):

        print(f"Проверка времени загрузки главной страницы в {browser_name}")

        # Выполняем JavaScript для получения времени загрузки
        load_event_end = driver.execute_script(
                "return window.performance.timing.loadEventEnd")
        navigation_start = driver.execute_script(
                "return window.performance.timing.navigationStart")

        load_time_ms = load_event_end - navigation_start
        print(f"Время загрузки: {load_time_ms} мс")
        assert load_time_ms <= MAX_LOAD_TIME_MS, \
                f"Главная страница загружалась слишком долго: {load_time_ms} мс"
        print("Главная страница загрузилась вовремя")

    # 11 Доступность
    # Проверка альтернативного текста для изображений
    @pytest.mark.parametrize("browser_name",
                             ["firefox", "chrome", "edge", "yandex"])
    def test_alt_image(self, driver, user_authorization, browser_name):
        shop = ShopPage(driver)

        print(f"Проверка альтернативного текста для изображений в {browser_name}")

        # Получить альтернативный текст для изображений
        alt_text_image = shop.get_alt_text_image()
        assert alt_text_image, "У изображения отсутствует alt-text"
        print(f"У изображения присутствует alt-text: {alt_text_image}")