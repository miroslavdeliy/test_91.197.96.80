import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import (driver_mozilla_firefox,
                      user_authorization_mozilla_firefox)
from constants import (BASE_URL, MENU_CART, MENU_SHOP, MENU_LOGOUT,
                       CART_HEADER_TEXT, AUTH_HEADER_TEXT,
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

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class TestMozillaFirefox:
    # --- Авторизация ---
    # Тест-кейс 1: Проверка авторизации пользователя с корректными данными
    def test_successful_user_login(self, driver_mozilla_firefox,
                                   user_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        shop = ShopPage(driver)

        logger.info("\nТест-кейс 1: Проверка входа пользователя"
                    "с корректными данными")

        # Проверка корректной авторизации пользователя
        assert_login_successful(shop, role="Пользователь")
        logger.info("Авторизация пользователя успешна")

    # Тест-кейс 2: Проверка авторизации профиля администратора
    def test_admin_authorization(self, driver_mozilla_firefox,
                                 admin_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        shop = ShopPage(driver)

        logger.info("\nТест-кейс 2: Проверка входа администратора"
                    "с корректными данными")

        # Проверка корректной авторизации Администратора
        assert_login_successful(shop, role="Администратор")
        logger.info("Авторизация администратора успешна")

    # --- Переход по страницам сайта без перезагрузки ---
    # Тест-кейс 3: Проверка наличия пунктов меню (с использованием subtests)
    def test_menu_visibility(self, subtests, driver_mozilla_firefox,
                             user_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        menu = MenuPage(driver)

        logger.info("\nТест-кейс 3: Проверка наличия пунктов меню")

        # Кликаем на кнопку меню
        menu.open_menu()
        logger.info("Меню открыто")

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
            logger.info(f"Пункт меню {label} присутствует")

    # Тест-кейс 4: Проверка перехода в раздел Корзинка без перезагрузки
    def test_menu_cart_navigation_no_reload(self, driver_mozilla_firefox,
                                            user_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        menu = MenuPage(driver)
        cart = CartPage(driver)

        logger.info("\nТест-кейс 4: Проверка перехода в раздел"
                    "'Корзинка' без перезагрузки")

        # Засекаем время загрузки страницы ДО перехода
        initial_load_time = driver.execute_script(
            "return window.performance.timing.loadEventEnd;"
        )
        logger.info(f"Время до перехода {initial_load_time}")

        # Открываем меню и кликаем по пункту "Корзинка"
        menu.open_menu()
        logger.info("Меню открыто")

        # Кликаем по пункту меню 'Корзинка'
        menu.open_cart()
        logger.info("Клик по пункту меню 'Корзинка'")

        # Проверяем текст заголовка "Корзинки"
        actual_text = cart.get_cart_title_text().strip().lower()
        assert_text_equal(
            actual_text,
            CART_HEADER_TEXT,
            "Переход в корзинку не удался"
        )

        # Засекаем время загрузки страницы ПОСЛЕ перехода
        after_load_time = driver_mozilla_firefox.execute_script(
            "return window.performance.timing.loadEventEnd;"
        )
        logger.info(f"Время после перехода {after_load_time}")

        # Проверка, что не произошла полная перезагрузка страницы
        assert after_load_time == initial_load_time,\
            "Произошла полная перезагрузка страницы"
        logger.info("Переход в 'Корзинку' прошел без перезагрузки"
                    "страницы с корректным заголовком")

    # Тест-кейс 5: Проверка перехода в раздел Магазин без перезагрузки
    def test_menu_shop_navigation_no_reload(self, driver_mozilla_firefox,
                                            user_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        menu = MenuPage(driver)
        shop = ShopPage(driver)

        logger.info("\nТест-кейс 5: Проверка перехода в раздел 'Магазин'"
                    "без перезагрузки")

        # Засекаем время загрузки страницы ДО перехода
        initial_load_time = driver.execute_script(
            "return window.performance.timing.loadEventEnd;"
        )
        logger.info(f"Время до перехода {initial_load_time}")

        # Открываем меню
        menu.open_menu()
        logger.info("Меню открыто")

        # Кликаем по пункту меню 'Магазин'
        menu.open_shop()
        logger.info("Клик по пункту меню 'Магазин'")

        # Проверяем текст заголовка "Магазин"
        actual_text = shop.get_shop_title_text().strip().lower()
        assert_text_equal(
            actual_text,
            PRODUCTS_HEADER_TEXT.lower(),
            "Переход в 'Магазин' не удался"
        )

        # Засекаем время загрузки страницы ПОСЛЕ перехода
        after_load_time = driver_mozilla_firefox.execute_script(
            "return window.performance.timing.loadEventEnd;"
        )
        logger.info(f"Время после перехода {after_load_time}")

        # Проверка, что не произошла полная перезагрузка страницы
        assert after_load_time == initial_load_time,\
            "Произошла полная перезагрузка страницы"
        logger.info("Переход в 'Магазин' прошел без перезагрузки страницы"
                    "с корректным заголовком")

    # Тест-кейс 6: Проверка кнопки Выход без перезагрузки
    def test_menu_exit(self, driver_mozilla_firefox,
                       user_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        menu = MenuPage(driver)
        auth = AuthorizationPage(driver)

        logger.info("\nТест-кейс 6: Проверка кнопки 'Выход' без перезагрузки")

        # Засекаем время загрузки страницы ДО выхода
        initial_load_time = driver.execute_script(
            "return window.performance.timing.loadEventEnd;"
        )
        logger.info(f"Время до перехода {initial_load_time}")

        # Открываем меню
        menu.open_menu()
        logger.info("Меню открыто")

        # Кликаем по кнопке 'Выход'
        menu.logout()
        logger.info("Клик по кнопке 'Выход' выполнен")

        # Проверяем текст заголовка
        actual_text = auth.get_auth_header_text().strip().lower()
        assert_text_equal(
            actual_text,
            AUTH_HEADER_TEXT.lower(),
            "Переход на страницу авторизации не выполнен"
        )

        # Засекаем время загрузки страницы ПОСЛЕ перехода
        after_load_time = driver_mozilla_firefox.execute_script(
            "return window.performance.timing.loadEventEnd;"
        )
        logger.info(f"Время после перехода {after_load_time}")

        # Проверка, что не произошла полная перезагрузка страницы
        assert after_load_time == initial_load_time,\
            "Произошла полная перезагрузка страницы"
        logger.info("Переход на страницу авторизации прошел без перезагрузки"
                    "страницы с корректным заголовком")

    # Тест-кейс 7: Проверка перехода на страницу редактирования товара
    def test_edit_goods_button(self, driver_mozilla_firefox,
                               admin_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        menu = MenuPage(driver)
        edit = EditGoodsPage(driver)

        logger.info("\nТест-кейс 7: Проверка перехода администратора в"
                    "'Редактирование: Товары'")

        # Засекаем время загрузки страницы
        initial_load_time = driver.execute_script(
            "return window.performance.timing.loadEventEnd;"
        )
        logger.info(f"Время до перехода {initial_load_time}")

        # Открываем меню
        menu.open_menu()
        logger.info("Меню открыто")

        # Кликаем по 'Редактировать товары'
        menu.open_edit()
        logger.info("Клик по 'Редактировать товары' выполнен")

        # Проверяем текст заголовка
        actual_text = edit.get_edit_header_text().strip().lower()
        assert_text_equal(
            actual_text,
            EDIT_GOODS_HEADER_TEXT.lower(),
            "Переход на страницу авторизации не выполнен"
        )

        # Засекаем время загрузки страницы ПОСЛЕ перехода
        after_load_time = driver_mozilla_firefox.execute_script(
            "return window.performance.timing.loadEventEnd;"
        )
        logger.info(f"Время после перехода {after_load_time}")

        # Проверка, что не произошла полная перезагрузка страницы
        assert after_load_time == initial_load_time,\
            "Произошла полная перезагрузка страницы"
        logger.info("Переход на страницу авторизации прошел без перезагрузки"
                    "страницы с корректным заголовком")

    # --- Корректность карточки товара ---
    # Тест-кейс 8: Проверка отображения данных товара
    def test_product_card_display(self, subtests, driver_mozilla_firefox,
                                  user_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        shop = ShopPage(driver)

        logger.info("\nТест-кейс 8: Проверка отображения карточки товара")

        # Сохраняем фактические значения карточки товара
        actual_name = shop.get_product_1_name().strip().lower()
        actual_description = shop.get_product_1_description().strip().lower()
        actual_price = shop.get_product_1_price().strip().lower()

        # Подготовка ожидаемых значений
        expected_name = PRODUCT_1_NAME.lower()
        expected_description = PRODUCT_1_DESCRIPTION.lower()
        expected_price = PRODUCT_1_DESCRIPTION.lower()

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
            logger.info(f"{label} товара отображается корректно")

        # Проверяем картинку
        image = shop.get_product_1_image()
        assert image.get_attribute("src") != "",\
            "Изображение товара не загружено (src-пустой)"
        logger.info("Изображение товара загружено")

    # Тест-кейс 9: Проверка работоспособности кнопок
    # изменения количества товара
    def test_button_changing_quantity_goods(
            self,
            subtests,
            driver_mozilla_firefox,
            user_authorization_mozilla_firefox
    ):
        driver = driver_mozilla_firefox
        shop = ShopPage(driver)

        logger.info("\nТест-кейс 9: Проверка работоспособности кнопок"
                    "изменения количества товара")

        # Получаем текущее количество (до добавления)
        quantity_before = int(shop.get_product_1_quantity())
        logger.info(f"Изначальное количество {quantity_before}")

        # --- Подтест 1: Увеличение количества товара ---
        shop.add_product_1()
        logger.info("Добавлен один товар")

        # Получаем количество товаров после добавления
        quantity_after_add = int(shop.get_product_1_quantity())
        logger.info(f"Количество товара после добавления:"
                    f"{quantity_after_add}")

        # Проверка увеличения количества товара на 1 штуку
        with subtests.test(label="Добавление товара"):
            assert quantity_after_add == quantity_before + 1, \
                (f"Количество товара не увеличилось. Было: {quantity_before},"
                 f" стало: {quantity_after_add}")
        logger.info(f"Товар успешно добавлен: было {quantity_before},"
                    f" стало {quantity_after_add}")

        # --- Подтест 2: Уменьшение количества товара ---
        shop.remove_product_1()
        logger.info("Удален один товар")

        # Получаем количество товаров после удаления
        quantity_after_remove = int(shop.get_product_1_quantity())
        logger.info(f"Количество товара после удаления:"
                    f" {quantity_after_remove}")

        # Проверка уменьшения количества товара на 1 штуку
        with subtests.test(label="Удаление товара"):
            assert quantity_after_remove == quantity_after_add - 1, \
                (f"Количество товара не уменьшилось. Было:"
                 f" {quantity_after_add}, стало: {quantity_after_remove}")
        logger.info(f"Товар успешно удален: было {quantity_after_add},"
                    f"стало: {quantity_after_remove}")

    # Тест-кейс 10: Проверка видимости изменения количества товара в корзине
    def test_visibility_changing_quantity_goods_in_cart(
            self, subtests, driver_mozilla_firefox,
            user_authorization_mozilla_firefox
    ):
        driver = driver_mozilla_firefox
        shop = ShopPage(driver)

        logger.info("\nТест-кейс 10: Проверка отображения товаров в корзине")

        # Сохраняем текущее количество товара в корзине
        quantity_before = int(shop.get_quantity_goods_in_cart())
        logger.info(f"Текущее количество товаров в корзине:"
                    f"{quantity_before}")

        # --- Подтест 1: Увеличение количества товара в корзине ---
        shop.add_product_1()
        logger.info("Товар добавлен в корзину")

        quantity_after_add = int(shop.get_product_1_quantity())
        logger.info(f"Количество товара после добавления:"
                    f"{quantity_after_add}")

        with subtests.test(label="Добавление товара в корзину"):
            assert quantity_after_add == quantity_before + 1, \
                (f"Количество не увеличилось. Было: {quantity_before},"
                 f"стало: {quantity_after_add}")
        logger.info(f"Товар успешно добавлен: было {quantity_before},"
                    f"стало {quantity_after_add}")

        # --- Подтест 2: Уменьшение количества товара в корзине ---
        shop.remove_product_1()
        logger.info("Товар удалён из корзины")

        # Получаем количество товаров после удаления
        quantity_after_remove = int(shop.get_product_1_quantity())
        logger.info(f"Количество товара после удаления:"
                    f" {quantity_after_remove}")

        with subtests.test(label="Удаление товара из корзины"):
            assert quantity_after_remove == quantity_after_add - 1, \
                (f"Количество не уменьшилось. Было: {quantity_after_add}, "
                 f"стало: {quantity_after_remove}")
        logger.info(f"Товар успешно удалён: было {quantity_after_add}, "
                    f"стало {quantity_after_remove}")

    # --- Корректность корзины ---
    # Тест-кейс 11: Проверка корректного отображения товаров в корзине
    def test_cart_items_display(self, subtests,
                                driver_mozilla_firefox,
                                user_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        shop = ShopPage(driver)
        cart = CartPage(driver)

        logger.info("\nТест-кейс 11: Проверка корректного отображения товаров "
                    "в корзине")

        # Добавляем товар в корзину
        shop.add_product_1()
        logger.info("Товар добавлен")

        # Переход в корзину
        shop.open_cart()
        logger.info("Клик иконке 'Корзинка'")

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
                logger.info(f"{label} в корзине отображается корректно")

    # Тест-кейс 12: Проверка корректного пересчета итоговой цены в корзине
    def test_cart_price_recalculation(self, driver_mozilla_firefox,
                                      user_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        shop = ShopPage(driver)
        cart = CartPage(driver)

        logger.info("\nТест-кейс 13: Проверка корректного пересчета итоговой "
                    "цены в корзине")

        # Переход в корзину
        shop.open_cart()
        logger.info("Клик по пункту меню 'Корзинка'")

        # Сохранить количество товара в корзине ДО добавления
        quantity_before_add = int(cart.get_product_1_quantity())
        logger.info(f"Количество товара: {quantity_before_add} в корзине")

        # Сохранить цену товара
        price = float(cart.get_product_1_price().split()[0])
        logger.info(f"Цена товара {price}")

        # Сохранить итоговую цену ДО добавления товара
        total_1 = float(cart.get_total().split()[-2])
        logger.info(f'Итоговая цена: {total_1} в корзине')

        # Добавить один товар в корзину
        cart.add_product_1()
        logger.info("Товар добавлен в корзину")

        # Сохранить количество товара ПОСЛЕ добавления
        quantity_after_add = int(cart.get_product_1_quantity())
        logger.info(f"Количества товара после добавления: {quantity_after_add}"
                    f" в корзине")

        # Проверка корректного пересчета итоговой цены
        total_2 = float(cart.get_total().split()[-2])
        logger.info(f"Итоговая цена после добавления товара: {total_2} в "
                    f"корзине")

        assert total_2 == price * quantity_after_add,\
            "Итоговая цена пересчитывается некорректно"
        logger.info("Итоговая цена пересчиталась корректно")

    # Тест-кейс 13: Проверка очистки корзины
    def test_clear_cart(self, driver_mozilla_firefox,
                        user_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        shop = ShopPage(driver)
        cart = CartPage(driver)

        logger.info("\nТест-кейс 13: Проверка очистки корзины")

        # Переход в корзину
        shop.open_cart()
        logger.info("Клик по иконке 'Корзинка'")

        # Сохранить количество товара в корзине ДО очистки
        quantity_before_clear = int(cart.get_product_1_quantity())
        logger.info(f"Количество товара: {quantity_before_clear} в корзине")

        # Уменьшать количество товара в корзине до очистки
        for _ in range(quantity_before_clear):
            cart.remove_product_1()
        logger.info("Корзина очистилась")

        # Проверка корректности сообщения о пустой корзине
        empty_cart_message = cart.get_empty_cart_message().strip().lower()
        assert_text_equal(
            empty_cart_message,
            EMPTY_CART_MESSAGE.lower(),
            "Корзина не очистилась!"
        )
        logger.info("Сообщение о пустой корзине корректно")

    # Тест-кейс 14: Проверка неактивности кнопки 'Оформить заказ' при пустой
    # корзине
    def test_make_order_button_disabled_when_cart_empty(
            self,
            driver_mozilla_firefox,
            user_authorization_mozilla_firefox
    ):
        driver = driver_mozilla_firefox
        shop = ShopPage(driver)
        cart = CartPage(driver)

        logger.info("\nТест-кейс 14: Проверка неактивности кнопки "
                    "'Оформить заказ' при пустой корзине")

        # Переход в корзину
        shop.open_cart()
        logger.info("Клик по иконке 'Корзинка'")

        # Проверяем недоступность кнопки "Оформить заказ"
        is_visible = cart.is_make_order_button_visible()
        if not is_visible:
            logger.info("Кнопка 'Оформить заказ' не видима при пустой "
                        "корзине")
        else:
            is_enabled = cart.is_make_order_button_enabled()
            assert not is_enabled, ("Кнопка 'Оформить заказ' активна при "
                                    "пустой корзине")

    # Тест-кейс 15: Проверка активности кнопки Оформить заказ при
    # непустой корзине
    def test_make_order_button_enabled(self, driver_mozilla_firefox,
                                       user_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        shop = ShopPage(driver)
        cart = CartPage(driver)

        logger.info("\nТест-кейс 15: Проверка активности кнопки "
                    "'Оформить заказ' при непустой корзине")

        # Добавляем товар
        shop.add_product_1()
        logger.info("Товар добавлен в корзину")

        # Переход в корзину
        shop.open_cart()
        logger.info("Клик по иконке 'Корзинка'")

        # Проверяем доступность кнопки "Оформить заказ"
        is_visible = cart.is_make_order_button_visible()
        if is_visible:
            logger.info("Кнопка 'Оформить заказ' видна при непустой корзине")
            is_enabled = cart.is_make_order_button_enabled()
            assert is_enabled, ("Кнопка 'Оформить заказ' неактивна "
                                "при непустой корзине")
            logger.info("Кнопка 'Оформить заказ' активна при непустой корзине")
        else:
            logger.info("Кнопка 'Оформить заказ' не видима при пустой корзине")

    # --- Оформление и совершение заказа ---
    # Тест-кейс 16: Проверка перенаправления на страницу заполнения личных
    # данных при нажатии на кнопку Оформить заказ
    def test_making_order_button_work(self, driver_mozilla_firefox,
                                      user_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        shop = ShopPage(driver)
        cart = CartPage(driver)
        make_order = MakeOrderPage(driver)

        logger.info(
            "\nТест-кейс 16: Проверка перенаправления на страницу"
            "заполнения личных данных"
            "при нажатии на кнопку Оформить заказ"
        )

        # Переход в корзину
        shop.open_cart()
        logger.info("Клик по иконке 'Корзинка'")

        # Нажать на кнопку Офомить заказ
        cart.make_order()
        logger.info("Клик по кнопке 'Оформить заказ'")

        # Проверка нахождения на странице ввода личных данных
        making_order_text = make_order.get_make_order_header_text().lower()
        assert_text_equal(
            making_order_text,
            MAKE_ORDER_HEADER_TEXT.lower(),
            "Кнопка Оформить заказ не переводит на страницу заполнения данных"
        )
        logger.info("Кнопка Оформить заказ переводит на страницу "
                    "заполнения личных данных")

    # Тест-кейс 17: Проверка перенаправления на страницу каталога
    # со страницы заполнения личных данных при нажатии на кнопку
    # Обратно в магазин
    def test_button_back_to_shop_from_personal_page(
            self,
            driver_mozilla_firefox,
            user_authorization_mozilla_firefox
    ):
        driver = driver_mozilla_firefox
        shop = ShopPage(driver)
        cart = CartPage(driver)

        logger.info(
            "\nТест-кейс 17: Проверка перенаправления на страницу каталога"
            "со страницы заполнения личных данных при нажатии на кнопку"
            " 'Обратно в магазин'"
        )

        # Переход в корзину
        shop.open_cart()
        logger.info("Клик по иконке 'Корзинка'")

        # Нажать на кнопку Офомить заказ
        cart.make_order()
        logger.info("Нажата кнопка 'Оформить заказ'")
        make_order = MakeOrderPage(driver)

        # Нажать на кнопку Обратно к товарам
        make_order.back_shop()
        logger.info("Нажата кнопка 'Обратно в магазин'")

        # Проверка нахождения на каталоге
        catalog_text = shop.get_shop_title_text().strip().lower()
        assert_text_equal(
            catalog_text,
            PRODUCTS_HEADER_TEXT.lower(),
            "Кнопка Обратно в магазин не переводит на страницу каталога"
        )

        logger.info("Кнопка 'Обратно в магазин' переводит на страницу каталога")

    # Тест-кейс 18: Проверка перенаправления на страницу подтверждения заказа
    # после заполнения личных данных
    def test_making_order(self, driver_mozilla_firefox,
                          user_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        shop = ShopPage(driver)
        cart = CartPage(driver)
        make_order = MakeOrderPage(driver)
        finish_order = FinishOrderPage(driver)

        logger.info(
            "\nТест-кейс 18: Проверка перенаправления на страницу "
            "подтверждения заказа"
            "после заполнения личных данных"
        )

        # Переход в корзину
        shop.open_cart()
        logger.info("Совершен переход в корзину")

        # Нажать на кнопку Оформить заказ
        cart.make_order()
        logger.info("Нажата кнопка 'Оформить заказ'")

        # Заполнение личной информации
        make_order.send_name(TEST_USER_NAME)
        make_order.send_first_name(TEST_USER_FIRST_NAME)
        make_order.send_last_name(TEST_USER_LAST_NAME)
        make_order.send_address(TEST_USER_ADDRESS)
        make_order.send_card_number(TEST_USER_CARD)
        logger.info("Заполнена личная информация")

        # Нажать на кнопку Завершить заказ
        make_order.open_finish_order()
        logger.info("Нажата кнопка 'Оформить заказ'")

        # Проверка нахождения на странице подтверждения заказа
        make_order_check = finish_order.get_finish_order_title().strip().lower()
        assert_text_equal(
            make_order_check,
            FINISH_ORDER_HEADER_TEXT.lower(),
            "Пользователь не попадает на страницу подтверждения заказа"
        )
        logger.info("Пользователь попадает на страницу подтверждения "
                    "оформления заказа")

    # Тест-кейс 19: Проверка перенаправления на страницу каталога со страницы
    # подтверждения заказа при нажатии на кнопку Обратно в магазин
    def test_back_to_shop_from_order(self, driver_mozilla_firefox,
                                     user_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        shop = ShopPage(driver)
        cart = CartPage(driver)
        make_order = MakeOrderPage(driver)
        finish_order = FinishOrderPage(driver)

        logger.info("\nТест-кейс 19: Проверка перенаправления на страницу "
                    "каталога со страницы подтверждения заказа при нажатии"
                    " на кнопку Обратно в магазин")

        # Переход в корзину
        shop.open_cart()
        logger.info("Совершен переход в корзину")

        # Нажать на кнопку Оформить заказ
        cart.make_order()
        logger.info("Нажата кнопка 'Оформить заказ'")

        # Заполнение личной информации
        make_order.send_name(TEST_USER_NAME)
        make_order.send_first_name(TEST_USER_FIRST_NAME)
        make_order.send_last_name(TEST_USER_LAST_NAME)
        make_order.send_address(TEST_USER_ADDRESS)
        make_order.send_card_number(TEST_USER_CARD)
        logger.info("Заполнена личная информация")

        # Нажать на кнопку Завершить заказ
        make_order.open_finish_order()
        logger.info("Нажата кнопка 'Оформить заказ'")

        # Нажать на кнопку Обратно в магазин
        finish_order.back_shop()
        logger.info("Нажата кнопка 'Обратно в магазин'")

        # Проверка нахождения на странице каталога
        shop_text = shop.get_shop_title_text().strip().lower()
        assert_text_equal(
            shop_text,
            PRODUCTS_HEADER_TEXT,
            "Кнопка Обратно в магазин не переводит в каталог"
        )
        logger.info("Кнопка 'Обратно в магазин' переводит в каталог")

    # Тест-кейс 20: Проверка корректности данных на странице подтверждения заказа
    def test_correct_data_order_page(
            self,
            subtests,
            driver_mozilla_firefox,
            user_authorization_mozilla_firefox
    ):
        driver = driver_mozilla_firefox
        shop = ShopPage(driver)
        cart = CartPage(driver)
        make_order = MakeOrderPage(driver)
        finish_order = FinishOrderPage(driver)

        logger.info("\nТест-кейс 20: Проверка корректности данных на странице "
                    "подтверждения заказа")

        # Переход в корзину
        shop.open_cart()
        logger.info("Совершен переход в корзину")

        # Сохраняем количество и сумму до оформления
        quantity_goods_in_cart = cart.get_product_1_quantity()
        total_in_cart = cart.get_total()

        # Оформляем заказ
        cart.make_order()
        logger.info("Нажата кнопка 'Оформить заказ'")

        # Заполняем личную информацию
        make_order.send_name(TEST_USER_NAME)
        make_order.send_first_name(TEST_USER_FIRST_NAME)
        make_order.send_last_name(TEST_USER_LAST_NAME)
        make_order.send_address(TEST_USER_ADDRESS)
        make_order.send_card_number(TEST_USER_CARD)
        logger.info("Заполнена личная информация")

        # Нажать кнопку 'Оформить заказ'
        make_order.open_finish_order()
        logger.info("Нажата кнопка 'Оформить заказ'")

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
                logger.info(f"{label} отображается корректно")

        # Проверка итоговой суммы — сравниваем числовые значения
        total_order = float(finish_order.get_finish_order_total().split()[-2])
        expected_total = float(total_in_cart.split()[-2])
        with subtests.test(label="Итоговая сумма"):
            assert total_order == expected_total, \
                f"Итоговая сумма некорректна: {total_order} ≠ {expected_total}"
            logger.info("Итоговая сумма корректна")

    # Тест-кейс 21: Проверка успешного оформления заказа
    def test_good_make_order(self, driver_mozilla_firefox,
                             user_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        shop = ShopPage(driver)
        cart = CartPage(driver)
        make_order = MakeOrderPage(driver)
        finish_order = FinishOrderPage(driver)
        good_order = GoodOrderPage(driver)

        logger.info("\nТест-кейс 21: Проверка успешного оформления заказа")

        # Переход в корзину
        shop.open_cart()
        logger.info("Совершен переход в корзину")

        # Нажать на кнопку Оформить заказ
        cart.make_order()
        logger.info("Нажата кнопка 'Оформить заказ'")

        # Заполнение личной информации
        make_order.send_name(TEST_USER_NAME)
        make_order.send_first_name(TEST_USER_FIRST_NAME)
        make_order.send_last_name(TEST_USER_LAST_NAME)
        make_order.send_address(TEST_USER_ADDRESS)
        make_order.send_card_number(TEST_USER_CARD)
        logger.info("Заполнена личная информация")

        # Нажать на кнопку Завершить заказ
        make_order.open_finish_order()
        logger.info("Нажата кнопка 'Оформить заказ'")

        # Нажать на кнопку "Завершить заказ"
        finish_order.finish_order()
        logger.info("Нажата кнопка 'Завершить заказ'")

        # Проверка сообщения об успешном оформлении заказа
        good_order_text = good_order.get_good_order_page_title().strip().lower()
        assert_text_equal(
            good_order_text,
            GOOD_ORDER_SUCCESS_TEXT.lower(),
            "Заказ не оформляется"
        )

        logger.info("Заказ успешно оформляется")

    # --- Добавление нового товара в ассортимент (профиль администратора) ---
    # Тест-кейс 22: Проверка кнопки Обратно к товарам на странице создания
    # товара
    def test_button_back_shop_from_edit(self, driver_mozilla_firefox,
                                        admin_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        menu = MenuPage(driver)
        edit = EditGoodsPage(driver)
        make_good = MakeGoodPage(driver)

        logger.info("\nТест кейс 22: Проверка кнопки Обратно к товарам на "
                    "странице редактирования товаров")

        # Нажать иконку меню
        menu.open_menu()
        logger.info("Открылось меню")

        # Нажать Редактирование товаров
        menu.open_edit()
        logger.info("Перешли на страницу редактирования товаров")

        # Нажать кнопку добавления товара
        edit.add_good()
        logger.info("Перешли на страницу создания нового товара")

        # Нажать кнопку Обратно к товарам
        make_good.back_goods()
        logger.info("Нажата кнопка 'Обратно к товарам'")

        # Проверка нахождения на странице редактирования товаров
        edit_goods_text = edit.get_edit_header_text().strip().lower()
        assert_text_equal(
            edit_goods_text,
            EDIT_GOODS_HEADER_TEXT.lower(),
            "Кнопка Обратно к товарам не переводит на страницу списка товаров"
        )
        logger.info("Кнопка Обратно к товарам переводит на страницу списка товаров")

    # Тест-кейс 26: Проверка корректного создания товаров
    def test_make_goods(self, subtests, driver_mozilla_firefox,
                        admin_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        menu = MenuPage(driver)
        edit = EditGoodsPage(driver)
        make_good = MakeGoodPage(driver)

        logger.info("\nТест-кейс 23: Проверка корректного создания товара")

        # Открытие меню и переход к созданию товара
        menu.open_menu()
        logger.info("Открылось меню")

        # Клик на 'Редактирование товаров'
        menu.open_edit()
        logger.info("Перешли на страницу редактирования товаров")

        # Клик на 'Добавить товар'
        edit.add_good()
        logger.info("Перешли на страницу создания нового товара")

        # Заполнение формы нового товара
        make_good.enter_name(NEW_GOOD_NAME)
        make_good.enter_description(NEW_GOOD_DESCRIPTION)
        make_good.enter_category(NEW_GOOD_CATEGORY)
        make_good.enter_price(NEW_GOOD_PRICE)
        make_good.enter_url(NEW_GOOD_IMAGE_URL)

        # Клик на 'Создать товар'
        make_good.make_good()
        logger.info("Товар создан")

        # Получение фактических значений
        actual_name = edit.get_name().strip().lower()
        actual_description = edit.get_description().strip().lower()
        actual_category = edit.get_category().strip().lower()
        actual_price = edit.get_price().strip().lower()
        actual_image_url = edit.get_image_maked_good()

        # Подготовка ожидаемых значений
        expected_name = NEW_GOOD_NAME.lower()
        expected_description = NEW_GOOD_DESCRIPTION.lower()
        expected_category = (f"категория: {NEW_GOOD_CATEGORY}").lower()
        expected_price = (f"цена: {NEW_GOOD_PRICE}.00 ₽").lower()
        expected_image_url = NEW_GOOD_IMAGE_URL

        # Подготовка проверок
        checks = [
            ("Название", actual_name, expected_name),
            ("Описание", actual_description, expected_description),
            ("Категория", actual_category, expected_category),
            ("Цена", actual_price, expected_price),
            ("URL изображения", actual_image_url, expected_image_url),
        ]

        # Подтесты с assert_text_equal
        for label, actual, expected in checks:
            with subtests.test(label=label):
                assert_text_equal(actual, expected,
                                  f"{label} товара создается некорректно")
                logger.info(f"{label} товара создается корректно")

    # --- Редактирование имеющегося товара (профиль администратора) ---
    # Тест-кейс 24: Проверка кнопки Обратно к товарам на странице редактирования
    # товара
    def test_back_from_edit_product(self, driver_mozilla_firefox,
                                    admin_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        menu = MenuPage(driver)
        edit = EditGoodsPage(driver)
        edit_product = EditProductPage(driver)

        logger.info("\nТест кейс 24: Проверка кнопки Обратно к товарам на "
                    "странице редактирования товаров")

        # Открыть меню
        menu.open_menu()
        logger.info("Открылось меню")

        # Нажать Редактирование товаров
        menu.open_edit()
        logger.info("Перешли на страницу редактирования товаров")

        # Нажать иконку редактирование конкретного товара
        edit.open_edit_product()
        logger.info("Перешли на страницу редактирования конкретного товара")

        # Нажать кнопку Обратно к товарам
        edit_product.back_goods()
        logger.info("Нажали кнопку 'Обратно к товарам'")

        edit_header_text = edit.get_edit_header_text().strip().lower()
        assert_text_equal(
            edit_header_text,
            EDIT_GOODS_HEADER_TEXT.lower(),
            "Кнопка Обратно к товарам не переводит на страницу списка товаров"
        )

        logger.info("Кнопка 'Обратно к товарам' переводит на страницу списка "
                    "товаров")

    # Тест-кейс 25: Проверка редактирования товара
    def test_edit_goods(self, subtests, driver_mozilla_firefox,
                        admin_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        menu = MenuPage(driver)
        edit = EditGoodsPage(driver)
        edit_product = EditProductPage(driver)

        logger.info("\nТест-кейс 25: Проверка редактирования товара")

        # Открыть меню и перейти к редактированию товаров
        menu.open_menu()
        logger.info("Открылось меню")

        menu.open_edit()
        logger.info("Перешли на страницу редактирования товаров")

        edit.open_edit_product()
        logger.info("Клик по иконке редактирования конкретного товара")

        # Внести новые значения в форму
        edit_product.clear_and_enter_name(EDITED_GOOD_NAME)
        edit_product.clear_and_enter_description(EDITED_GOOD_DESCRIPTION)
        edit_product.clear_and_enter_category(EDITED_GOOD_CATEGORY)
        edit_product.clear_and_enter_price(EDITED_GOOD_PRICE)
        edit_product.cleat_and_enter_url(EDITED_GOOD_IMAGE_URL)

        # Сохранить изменения
        edit_product.edit_product()
        logger.info("Товар отредактирован")

        # Получить отредактированные значения с интерфейса
        actual_name = edit.get_name().strip().lower()
        actual_description = edit.get_description().strip().lower()
        actual_category = edit.get_category().strip().lower()
        actual_price = edit.get_price().strip().lower()
        actual_image_url = edit.get_image_maked_good()

        # Подготовить ожидаемые значения
        expected_name = EDITED_GOOD_NAME.lower()
        expected_description = EDITED_GOOD_DESCRIPTION.lower()
        expected_category = f"категория: {EDITED_GOOD_CATEGORY}".lower()
        expected_price = f"цена: {EDITED_GOOD_PRICE}.00 ₽".lower()
        expected_image_url = EDITED_GOOD_IMAGE_URL

        # Подготовка проверок
        data = [
            ("Название", actual_name, expected_name),
            ("Описание", actual_description,expected_description),
            ("Категория", actual_category,expected_category),
            ("Цена", actual_price, expected_price),
            ("URL изображения", actual_image_url, expected_image_url),
        ]

        # Подтесты с assert_text_equal
        for label, actual, expected in data:
            with subtests.test(label=label):
                assert_text_equal(actual, expected,
                                  f"{label} товара редактируется некорректно")
                logger.info(f"{label} товара редакируется корректно")

    # Удаление товара (профиль администратора)
    # Тест-кейс 26: Проверка удаления товара
    def test_delete_goods(self, driver_mozilla_firefox,
                          admin_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        menu = MenuPage(driver)
        edit = EditGoodsPage(driver)

        logger.info("Тест-кейс 26: Проверка удаления товара")

        # Открыть меню
        menu.open_menu()
        logger.info("Открылось меню")

        # Нажать Редактирование товаров
        menu.open_edit()
        logger.info("Перешли на страницу редактирования товаров")

        # Сохранить название товара
        good_name = edit.get_name()
        edit.delete_product()
        logger.info(f"Нажата кнопка удаления товара {good_name}")

        # Ожидаем исчезновения конкретного товара
        WebDriverWait(driver_mozilla_firefox, 10).until(
            EC.invisibility_of_element_located(
                (By.XPATH, f'//div[contains(text(), "{good_name}")]'))
        )
        logger.info("Товар исчез из списка")

    # 9 Негативные сценарии
    # Тест-кейс 27: Проверка добавления количества товара больше максимального
    def test_more_max_goods(self, driver_mozilla_firefox,
                            user_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        shop = ShopPage(driver)

        logger.info("\nТест-кейс 27: Проверка добавления количества товара "
                    "больше максимального")

        # Кликнуть на кнопку добавления товаров 101 раз
        for _ in range(MAX_QUANTITY + 1):
            shop.add_product_1()

        # Проверка, что в корзине не больше 100 штук
        count_goods = shop.get_quantity_goods_in_cart()
        assert int(count_goods) <= MAX_QUANTITY, \
            f"В корзину добавляется больше {MAX_QUANTITY} единиц товара"
        logger.info("В корзину добавляется не более 100 единиц товара")

    # Тест-кейс 28: Проверка добавления товаров на стоимость больше максимальной
    def test_more_max_total(self, driver_mozilla_firefox,
                            user_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        shop = ShopPage(driver)
        cart = CartPage(driver)

        logger.info("Тест-кейс 28: Проверка добавления товаров на стоимость "
                    "больше максимальной")

        # Переход в корзину
        shop.open_cart()
        logger.info("Совершен переход в корзину")

        current_total = 0
        while current_total <= MAX_TOTAL:
            cart.add_product_1()
            current_total = int(cart.get_total().split()[-2])

        assert current_total <= MAX_TOTAL, \
            "Итоговая сумма корзины больше максимальной"
        logger.info("Итоговая сумма не превышает максимальной")

    # Тест-кейс 29: Проверка оформления заказа без заполнения личных данных
    def test_without_personal_data(self, driver_mozilla_firefox,
                                   user_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        shop = ShopPage(driver)
        cart = CartPage(driver)
        make_order = MakeOrderPage(driver)

        logger.info("\nТест-кейс 29: Проверка оформления заказа без заполнения"
                    " личных данных")

        # Переход в корзину
        shop.open_cart()
        logger.info("Совершен переход в корзину")

        # Нажать на кнопку Офомить заказ
        cart.make_order()
        logger.info("Совершен переход на страницу заполнения личных данных")

        # Нажать на кнопку Оформить заказ
        make_order.open_finish_order()
        logger.info("Нажата кнопка 'Оформить заказ'")

        # Сохранить текст сообщения об ошибке
        error_message = make_order.get_error_message().strip().lower()
        assert_text_equal(
            error_message,
            MISSING_PERSONAL_DATA_ERROR.lower(),
            "Тест провален! Текст сообщения об ошибке некорректный"
        )

        logger.info("Текст сообщения об ошибке корректный")

    # 10 Производительность
    # Тест-кейс 30: Проверка времени загрузки главной страницы
    def test_time_load(self):
        driver = webdriver.Firefox()

        logger.info("\nТест-кейс 30: Проверка времени загрузки главной страницы")

        driver.set_page_load_timeout(10)  # страхуемся от подвисания

        try:
            # Открываем главную страницу
            driver.get(BASE_URL)

            # Выполняем JavaScript для получения времени загрузки
            load_event_end = driver.execute_script(
                "return window.performance.timing.loadEventEnd")
            navigation_start = driver.execute_script(
                "return window.performance.timing.navigationStart")

            load_time_ms = load_event_end - navigation_start
            logger.info(f"Время загрузки: {load_time_ms} мс")
            assert load_time_ms <= MAX_LOAD_TIME_MS, \
                f"Главная страница загружалась слишком долго: {load_time_ms} мс"

            logger.info("Главная страница загрузилась вовремя")
        finally:
            driver.quit()

    # 11 Доступность
    # Тест-кейс 34: Проверка альтернативного текста для изображений
    def test_alt_image(self, driver_mozilla_firefox,
                       user_authorization_mozilla_firefox):
        driver = driver_mozilla_firefox
        shop = ShopPage(driver)

        logger.info("\nТест-кейс 34: Проверка альтернативного текста для "
                    "изображений")

        # Получить альтернативный текст для изображений
        alt_text_image = shop.get_alt_text_image()
        assert alt_text_image, "У изображения отсутствует alt-text"
        logger.info(f"У изображения присутствует alt-text: {alt_text_image}")
