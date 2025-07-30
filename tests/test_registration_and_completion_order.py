import allure
import pytest

from constants import (
    SHOP_TITLE_TEXT,
    TEST_USER_NAME,
    TEST_USER_FIRST_NAME,
    TEST_USER_LAST_NAME,
    TEST_USER_ADDRESS,
    TEST_USER_CARD,
    FINISH_ORDER_HEADER_TEXT,
    PRODUCT_1_NAME,
    GOOD_ORDER_SUCCESS_TEXT
)
from helpers.assertions import assert_text_equal
from pageobjects.cart_page import CartPage
from pageobjects.finish_order_page import FinishOrderPage
from pageobjects.good_order_page import GoodOrderPage
from pageobjects.make_order_page import MakeOrderPage
from pageobjects.shop_page import ShopPage

class TestRegistrationAndCompletionOrder:
    @allure.title(
        "Проверка работоспособности кнопки 'Обратно к товарам' на странице "
        "заполнения личных данных в {browser_name}"
    )
    @allure.description(
        "Проверка, что кнопка 'Обратно к товарам' переводит на страницу "
        "каталога товаров со страницы заполнения личных данных"
    )
    @pytest.mark.parametrize(
        "browser_name",
        [
            "Mozilla Firefox",
            "Google Chrome",
            "Microsoft Edge",
            "Yandex Browser"
        ]
    )
    def test_button_back_to_shop_from_personal_page(
            self, driver, user_authorization, browser_name
    ):
        allure.dynamic.parameter("Браузер", browser_name)
        with allure.step("Открытие страницы и иницилизация объектов"):
            shop = ShopPage(driver)
            cart = CartPage(driver)
            make_order = MakeOrderPage(driver)

        with allure.step("Переход в корзину"):
            shop.open_cart()

        with allure.step("Нажать на кнопку 'Оформить заказ'"):
            cart.make_order()

        with allure.step("Нажать на кнопку 'Обратно к товарам'"):
            make_order.back_shop()

        with allure.step("Проверка нахождения в каталоге товаров"):
            catalog_text = shop.get_shop_title_text().lower()
            assert_text_equal(
                catalog_text,
                SHOP_TITLE_TEXT.lower(),
                "Кнопка Обратно в магазин не переводит на страницу каталога"
            )

    @allure.title(
        "Проверка работоспособности кнопки 'Оформить заказ' после заполнения "
        "личных данных в {browser_name}"
    )
    @allure.description(
        "Проверка, что кнопка 'Оформить заказ' переводит на страницу "
        "подтверждения заказа со страницы заполнения личных данных"
    )
    @pytest.mark.parametrize(
        "browser_name",
        [
            "Mozilla Firefox",
            "Google Chrome",
            "Microsoft Edge",
            "Yandex Browser"
        ]
    )
    def test_make_order_button(
            self, driver, user_authorization, browser_name
    ):
        with allure.step("Открытие страницы и иницилизация объектов"):
            shop = ShopPage(driver)
            cart = CartPage(driver)
            make_order = MakeOrderPage(driver)
            finish_order = FinishOrderPage(driver)

        with allure.step("Переход в корзину"):
            shop.open_cart()

        with allure.step("Нажать на кнопку 'Оформить заказ'"):
            cart.make_order()

        with allure.step("Заполнение личных данных"):
            make_order.send_name(TEST_USER_NAME)
            make_order.send_first_name(TEST_USER_FIRST_NAME)
            make_order.send_last_name(TEST_USER_LAST_NAME)
            make_order.send_address(TEST_USER_ADDRESS)
            make_order.send_card_number(TEST_USER_CARD)

        with allure.step("Нажать кнопку 'Оформить заказ'"):
            make_order.open_finish_order()

        with allure.step(
                "Проверка нахождения на странице подтверждения заказа"
        ):
            make_order_check = finish_order.get_finish_order_title().lower()
            assert_text_equal(
                make_order_check,
                FINISH_ORDER_HEADER_TEXT.lower(),
                "Пользователь не попадает на страницу подтверждения заказа"
            )

    @allure.title(
        "Проверка работоспособности кнопки 'Обратно в магазин' на странице "
        "подтверждения заказа {browser_name}"
    )
    @allure.description(
        "Проверка, что кнопка 'Обратно в магазин' переводит на страницу "
        "каталога товаров со страницы подтверждения заказа"
    )
    @pytest.mark.parametrize(
        "browser_name",
        [
            "Mozilla Firefox",
            "Google Chrome",
            "Microsoft Edge",
            "Yandex Browser"
        ]
    )
    def test_back_to_shop_from_order(
            self, driver, user_authorization, browser_name
    ):
        with allure.step("Открытие страницы и иницилизация объектов"):
            shop = ShopPage(driver)
            cart = CartPage(driver)
            make_order = MakeOrderPage(driver)
            finish_order = FinishOrderPage(driver)

        with allure.step("Переход в корзину"):
            shop.open_cart()

        with allure.step("Нажать на кнопку 'Оформить заказ'"):
            cart.make_order()

        with allure.step("Заполнение личных данных"):
            make_order.send_name(TEST_USER_NAME)
            make_order.send_first_name(TEST_USER_FIRST_NAME)
            make_order.send_last_name(TEST_USER_LAST_NAME)
            make_order.send_address(TEST_USER_ADDRESS)
            make_order.send_card_number(TEST_USER_CARD)

        with allure.step("Нажать кнопку 'Оформить заказ'"):
            make_order.open_finish_order()

        with allure.step("Нажать кнопку 'Обратно в магазин'"):
            finish_order.back_shop()

        with allure.step("Проверка нахождения на странице каталога товаров"):
            catalog_text = shop.get_shop_title_text().lower()
            assert_text_equal(
                catalog_text,
                SHOP_TITLE_TEXT.lower(),
                "Кнопка Обратно в магазин не работает"
            )

    @allure.title(
        "Проверка корректности данных на странице подтверждения заказа"
        " {browser_name}"
    )
    @allure.description(
        "Проверка, на странице подтверждения заказа данные товара и "
        "покупателя корректно отображаются"
    )
    @pytest.mark.parametrize(
        "browser_name",
        [
            "Mozilla Firefox",
            "Google Chrome",
            "Microsoft Edge",
            "Yandex Browser"
        ]
    )
    def test_correct_data_order_page(
            self, subtests, driver, user_authorization, browser_name
    ):
        with allure.step("Открытие страницы и иницилизация объектов"):
            shop = ShopPage(driver)
            cart = CartPage(driver)
            make_order = MakeOrderPage(driver)
            finish_order = FinishOrderPage(driver)

        with allure.step("Переход в корзину"):
            shop.open_cart()

        with allure.step("Сохранить количество товара и общую сумму"):
            quantity_goods_in_cart = cart.get_product_1_quantity()
            total_in_cart = cart.get_total()

        with allure.step("Нажать на кнопку 'Оформить заказ'"):
            cart.make_order()

        with allure.step("Заполнение личных данных"):
            make_order.send_name(TEST_USER_NAME)
            make_order.send_first_name(TEST_USER_FIRST_NAME)
            make_order.send_last_name(TEST_USER_LAST_NAME)
            make_order.send_address(TEST_USER_ADDRESS)
            make_order.send_card_number(TEST_USER_CARD)

        with allure.step("Нажать кнопку 'Оформить заказ'"):
            make_order.open_finish_order()

        with allure.step("Получаем данные со страницы подтверждения заказа"):
            actual_name_product = (
                finish_order.get_finish_order_name_product().lower()
            )
            actual_name = finish_order.get_finish_order_name().lower()
            actual_first_name = (
                finish_order.get_finish_order_first_name().lower()
            )
            actual_finish_name = (
                finish_order.get_finish_order_last_name().lower()
            )
            actual_address = finish_order.get_finish_order_address().lower()
            actual_card = finish_order.get_finish_order_card_number().lower()
            actual_quantity_goods = (
                finish_order.get_finish_order_quantity_goods().lower()
            )
        with allure.step("Проверка текстовых данных"):
            # Подготавливаем ожидаемые значения
            expected_name_product = PRODUCT_1_NAME.lower()
            expected_name = f"имя: {TEST_USER_NAME}".lower()
            expected_first_name = f"фамилия: {TEST_USER_FIRST_NAME}".lower()
            expected_finish_name = f"отчество: {TEST_USER_LAST_NAME}".lower()
            expected_address = f"адрес доставки: {TEST_USER_ADDRESS}".lower()
            expected_card = f"номер карты: {TEST_USER_CARD}".lower()
            expected_quantity_goods = (
                f"количество товаров: {quantity_goods_in_cart}"
            )

            data = [
                (
                    "Название товара",
                    actual_name_product,
                    expected_name_product,
                    assert_text_equal
                ),
                (
                    "Имя",
                    actual_name,expected_name,
                    assert_text_equal
                ),
                (
                    "Фамилия",
                    actual_first_name,
                    expected_first_name,
                    assert_text_equal
                ),
                (
                    "Отчество",
                    actual_finish_name,
                    expected_finish_name,
                    assert_text_equal
                ),
                (
                    "Адрес доставки",
                    actual_address,
                    expected_address,
                    assert_text_equal
                ),
                (
                    "Номер карты",
                    actual_card,
                    expected_card,
                    assert_text_equal
                ),
                (
                    "Количество товаров",
                    actual_quantity_goods,
                    expected_quantity_goods,
                    assert_text_equal
                )
            ]

            for label, actual, expected, custom_assert in data:
                with allure.step(f"Проверка {label}"):
                    with subtests.test(label=label):
                        allure.attach(
                            actual,
                            name=f"Фактическое значение",
                            attachment_type=allure.attachment_type.TEXT
                        )
                        allure.attach(
                            expected,
                            name=f"Ожидаемое значение",
                            attachment_type=allure.attachment_type.TEXT
                        )
                        custom_assert(
                            actual,
                            expected,
                            f"{label} некорректно отображается"
                        )

        with allure.step("Проверка итоговой суммы"):
            total_order = (
                float(finish_order.get_finish_order_total().split()[-2])
            )
            expected_total = float(total_in_cart.split()[-2])
            with subtests.test(label="Итоговая сумма"):
                allure.attach(
                    str(total_order),
                    name=f"Фактическое значение",
                    attachment_type=allure.attachment_type.TEXT
                )
                allure.attach(
                    str(expected_total),
                    name=f"Ожидаемое значение",
                    attachment_type=allure.attachment_type.TEXT
                )
                try:
                    assert total_order == expected_total,\
                        f"Итоговая сумма некорректна!"
                except AssertionError as e:
                    allure.attach(
                        str(e),
                        name=f"Текст ошибки",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    assert False, str(e)


    @allure.title("Проверка успешного оформления заказа в {browser_name}")
    @allure.description(
        "Проверка, что после подтверждения заказа при нажатии на кнопку "
        "'Завершить заказ' появляется собщение об успешном совершении заказа"
    )
    @pytest.mark.parametrize(
        "browser_name",
        [
            "Mozilla Firefox",
            "Google Chrome",
            "Microsoft Edge",
            "Yandex Browser"
        ]
    )
    def test_good_make_order(self, driver, user_authorization, browser_name):
        with allure.step("Открытие страницы и иницилизация объектов"):
            shop = ShopPage(driver)
            cart = CartPage(driver)
            make_order = MakeOrderPage(driver)
            finish_order = FinishOrderPage(driver)
            good_order = GoodOrderPage(driver)

        with allure.step("Переход в корзину"):
            shop.open_cart()

        with allure.step("Нажать на кнопку 'Оформить заказ'"):
            cart.make_order()

        with allure.step("Заполнение личных данных"):
            make_order.send_name(TEST_USER_NAME)
            make_order.send_first_name(TEST_USER_FIRST_NAME)
            make_order.send_last_name(TEST_USER_LAST_NAME)
            make_order.send_address(TEST_USER_ADDRESS)
            make_order.send_card_number(TEST_USER_CARD)

        with allure.step("Нажать кнопку 'Оформить заказ'"):
            make_order.open_finish_order()

        with allure.step("Нажать кнопку 'Завершить заказ'"):
            finish_order.finish_order()

        with allure.step("Проверка успешного оформления заказа"):
            good_order_text = good_order.get_good_order_page_title().lower()
            assert_text_equal(
                good_order_text,
                GOOD_ORDER_SUCCESS_TEXT.lower(),
                "Заказ не оформляется"
            )