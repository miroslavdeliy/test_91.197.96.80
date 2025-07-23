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
                       SHOP_TITLE_TEXT, TEST_USER_NAME,
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