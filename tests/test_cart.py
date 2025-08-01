# Импортирование библиотек
import allure
import pytest

# Импортирование пользовательских библиотек
from constants import (
    EMPTY_CART_MESSAGE,
    MAKE_ORDER_HEADER_TEXT,
    PRODUCT_1_NAME,
    PRODUCT_1_PRICE
    )
from helpers.assertions import assert_text_equal
from pageobjects.cart_page import CartPage
from pageobjects.make_order_page import MakeOrderPage
from pageobjects.shop_page import ShopPage


class TestCart:
    @allure.title("Проверка отображения данных товара {browser_name}")
    @allure.description(
        "Проверка, что в корзине товар отображается корректно: название, "
        "количество, цена"
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
    def test_cart_items_display(
            self, subtests, driver, user_authorization, browser_name
    ):
        allure.dynamic.parameter("Браузер", browser_name)
        with allure.step("Открытие страницы и иницилизация объектов"):
            shop = ShopPage(driver)
            cart = CartPage(driver)

        with allure.step("Добавление 1-го товара в корзину"):
            shop.add_product_1()

        with allure.step("Переход в корзину"):
            shop.open_cart()

        with allure.step("Сохранение фактических значений товара в корзине"):
            # Получение фактических значений
            actual_name = cart.get_product_1_name().lower()
            actual_quantity = int(cart.get_product_1_quantity())
            actual_price = cart.get_product_1_price().lower()

        with (allure.step("Проверка полученных значений в карточке товара")):
            # Подготовка ожидаемых значений
            expected_name = PRODUCT_1_NAME.lower()
            expected_quantity = 1
            expected_price = PRODUCT_1_PRICE.lower()

            data = [
                (
                    "Название товара",
                    actual_name,
                    expected_name,
                    assert_text_equal
                ),
                (
                    "Количество товара",
                    actual_quantity,
                    expected_quantity,
                    None
                ),
                (
                    "Цена товара",
                    actual_price,
                    expected_price,
                    assert_text_equal
                )
            ]
            for label, actual, expected, custom_assert in data:
                with allure.step(f"Проверка {label}"):
                    with ((subtests.test(label=label))):
                        if custom_assert:
                            custom_assert(
                                actual,
                                expected,
                                f"{label} некорректно отображается в корзине"
                            )
                        else:
                            try:
                                assert actual == expected,\
                                f"{label}некорректно: {actual} ≠ {expected}"
                            except AssertionError as e:
                                # В случае несовпадения - логирование ошибки
                                allure.attach(
                                    str(e),
                                    name=f"Текст ошибки",
                                    attachment_type=allure.attachment_type.TEXT
                                )
                                # Принудительное падение теста
                                assert False, str(e)

    @allure.title(
        "Проверка корректного пересчета итоговой цены в корзине в "
        "{browser_name}"
    )
    @allure.description(
        "Проверка, что в корзине итоговая цена пересчитывается корректно при"
        " добавлении"
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
    def test_cart_price_recalculation(
            self, driver, user_authorization,browser_name
    ):
        allure.dynamic.parameter("Браузер", browser_name)
        with allure.step("Открытие страницы и иницилизация объектов"):
            shop = ShopPage(driver)
            cart = CartPage(driver)

        with allure.step("Переход в корзину"):
            shop.open_cart()

        with allure.step("Сохранение количества товаров ДО добавления"):
            quantuty_before_add = int(cart.get_product_1_quantity())
            allure.attach(
                f"Количество до добавления: {str(quantuty_before_add)}",
                name="Quantity before add",
                attachment_type=allure.attachment_type.TEXT)

        with allure.step("Сохранение цены товара"):
            price = float(cart.get_product_1_price().split()[0])
            allure.attach(
                f"Цена товара: {str(price)}",
                name="Price",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Сохранение итоговой цены ДО добавления"):
            total_1 = float(cart.get_total().split()[-2])
            allure.attach(
                f"Итоговая цена ДО добавления: {total_1}",
                name = "Total before add",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Добавить 1 товар"):
            cart.add_product_1()

        with allure.step("Сохранение количества товаров ПОСЛЕ добавления"):
            quantuty_after_add = int(cart.get_product_1_quantity())
            allure.attach(
                f"Количество до добавления: {str(quantuty_after_add)}",
                name="Quantity after add",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Сохранение итоговой цены ПОСЛЕ добавления"):
            total_2 = float(cart.get_total().split()[-2])
            allure.attach(
                f"Итоговая цена ПОСЛЕ добавления {total_2}",
                name="Total after add",
                attachment_type=allure.attachment_type.TEXT
            )

        with (allure.step("Проверка корректного пересчета итоговой цены")):
            try:
                assert total_2 == price * quantuty_after_add,\
                "Итоговая цена пересчитывается некорректно"
            except AssertionError as e:
                # В случае несовпадения - логирование ошибки
                allure.attach(
                    str(e),
                    name=f"Текст ошибки",
                    attachment_type=allure.attachment_type.TEXT
                )
                # Принудительное падение теста
                assert False, str(e)

    @allure.title("Проверка корректной очистки корзины в {browser_name}")
    @allure.description(
        "Проверка, что корзина корректно очищается и сообщение о пустой "
        "корзине корректна"
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
    def test_clear_cart(self, driver, user_authorization, browser_name):
        allure.dynamic.parameter("Браузер", browser_name)
        with allure.step("Открытие страницы и иницилизация объектов"):
            shop = ShopPage(driver)
            cart = CartPage(driver)

        with allure.step("Переход в корзину"):
            shop.open_cart()

        with allure.step("Сохранить количество товара в корзине ДО удаления"):
            quantity_before_clear = int(cart.get_product_1_quantity())
            allure.attach(
                f"Количество товара ДО удаления {quantity_before_clear}",
                name="Quantity before clear",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Уменьшать количество товара в корзине до очистки"):
            for _ in range(quantity_before_clear):
                cart.remove_product_1()

        with allure.step("Проверка корректности сообщения о пустой корзине"):
            empty_cart_message = cart.get_empty_cart_message().lower()
            assert_text_equal(
                empty_cart_message,
                EMPTY_CART_MESSAGE.lower(),
                "Корзина не очистилась!"
            )

    @allure.title(
        "Проверка неактивности кнопки 'Оформить заказ' при пустой корзине в "
        "{browser_name}"
    )
    @allure.description(
        "Проверка, что в пустой корзине кнопка 'Оформить заказ' не "
        "отображается или неактивна"
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
    def test_make_order_button_disabled_when_cart_empty(
            self, driver, user_authorization, browser_name
    ):
        allure.dynamic.parameter("Браузер", browser_name)
        with allure.step("Открытие страницы и иницилизация объектов"):
            shop = ShopPage(driver)
            cart = CartPage(driver)

        with allure.step("Переход в корзину"):
            shop.open_cart()

        with allure.step("Проверка недоступности кнопки 'Оформить заказ'"):
            # Проверяем недоступность кнопки "Оформить заказ"
            is_visible = cart.is_make_order_button_visible()
            if not is_visible:
                with allure.step("Кнопка невидима при пустой корзине"):
                    pass
            else:
                is_enabled = cart.is_make_order_button_enabled()
                try:
                    assert not is_enabled, (
                        "Кнопка 'Оформить заказ' активна при пустой корзине"
                    )
                except AssertionError as e:
                    # В случае несовпадения - логирование ошибки
                    allure.attach(
                        str(e),
                        name=f"Текст ошибки",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    # Принудительное падение теста
                    assert False, str(e)

    @allure.title(
        "Проверка активности кнопки 'Оформить заказ' при непустой корзине в "
        "{browser_name}"
    )
    @allure.description(
        "Проверка, что в непустой корзине кнопка 'Оформить заказ' "
        "отображается и активна"
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
    def test_make_order_button_enabled(
            self, driver, user_authorization, browser_name
    ):
        allure.dynamic.parameter("Браузер", browser_name)
        with allure.step("Открытие страницы и иницилизация объектов"):
            shop = ShopPage(driver)
            cart = CartPage(driver)

        with allure.step("Добавить 1 товар в корзину"):
            shop.add_product_1()

        with allure.step("Переход в корзину"):
            shop.open_cart()

        with allure.step("Проверка доступности кнопки 'Оформить заказ'"):
            is_visible = cart.is_make_order_button_visible()
            try:
                assert is_visible, (
                    "Кнопка 'Оформить заказ' не видима при непустой корзине"
                )
            except AssertionError as e:
                # В случае несовпадения - логирование ошибки
                allure.attach(
                    str(e),
                    name=f"Текст ошибки",
                    attachment_type=allure.attachment_type.TEXT
                )
                # Принудительное падение теста
                assert False, str(e)
            is_enabled = cart.is_make_order_button_enabled()
            try:
                assert is_enabled, (
                    "Кнопка 'Оформить заказ' неактивна при непустой корзине"
                )
            except AssertionError as e:
                # В случае несовпадения - логирование ошибки
                allure.attach(
                    str(e),
                    name=f"Текст ошибки",
                    attachment_type=allure.attachment_type.TEXT
                )
                # Принудительное падение теста
                assert False, str(e)

    @allure.title(
        "Проверка работоспособности кнопки 'Оформить заказ' в {browser_name}"
    )
    @allure.description(
        "Проверка, что в непустой корзине кнопка 'Оформить заказ' переводит "
        "на страницу заполнения личных данных"
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

    def test_making_order_button_work(
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

        with allure.step(
                "Проверка нахождения на странице заполнения личных данных"
        ):
            making_order = make_order.get_make_order_header_text().lower()
            assert_text_equal(
                making_order,
                MAKE_ORDER_HEADER_TEXT.lower(),
                "Кнопка Оформить заказ не переводит на страницу заполнения"
            )