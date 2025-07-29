# Импортирование библиотек
import allure
import pytest

# Импортирование пользовательских библиотек
from conftest import driver, user_authorization
from constants import (
    PRODUCT_1_DESCRIPTION,
    PRODUCT_1_NAME,
    PRODUCT_1_PRICE,
)
from helpers.assertions import assert_text_equal
from pageobjects.shop_page import ShopPage


class TestProductCart:
    @allure.title("Проверка отображения данных товара {browser_name}")
    @allure.description(
        "Проверка, что в карточке товара присутствует название, описание, "
        "цена, изображение"
    )
    @pytest.mark.parametrize(
        "browser_name",
        [
            "Mozilla Firefox",
            "Google Chrome",
            "Microsoft Edge",
            "Yandex Browser",
        ],
    )
    def test_product_card_display(
        self, subtests, driver, user_authorization, browser_name
    ):
        allure.dynamic.parameter("Браузер", browser_name)
        with allure.step("Открытие страницы и иницилизация объектов"):
            shop = ShopPage(driver)

        with allure.step("Сохранение фактических значений карточки товара"):
            actual_name = shop.get_product_1_name().lower()
            actual_description = shop.get_product_1_description().lower()
            actual_price = shop.get_product_1_price().lower()

            expected_name = PRODUCT_1_NAME.lower()
            expected_description = PRODUCT_1_DESCRIPTION.lower()
            expected_price = PRODUCT_1_PRICE.lower()

        with allure.step("Проверка полученных значений в карточке товара"):
            data = [
                ("Название", actual_name, expected_name),
                ("Описание", actual_description, expected_description),
                ("Цена", actual_price, expected_price),
            ]
            for label, actual, expected in data:
                with allure.step(f"Проверка {label}"):
                    with subtests.test(label=label):
                        allure.attach(
                            actual,
                            name="Фактическое значение",
                            attachment_type=allure.attachment_type.TEXT,
                        )
                        allure.attach(
                            expected,
                            name="Ожидаемое значение",
                            attachment_type=allure.attachment_type.TEXT,
                        )
                        assert_text_equal(
                            actual, expected, f"{label} товара некорректно"
                        )

        with allure.step("Проверка загрузки изображения"):
            image = shop.get_product_1_image()
            try:
                assert image.get_attribute("src") != "", (
                    "Изображение товара не загружено (src-пустой)"
                )
            except AssertionError as e:
                allure.attach(
                    str(e),
                    name="Текст ошибки",
                    attachment_type=allure.attachment_type.TEXT,
                )
                assert False, str(e)

    @allure.title("Проверка изменения количества товара в {browser_name}")
    @allure.description(
        "Проверка, что кнопки изменения количества товара увеличивают и "
        "уменьшают количество товара"
    )
    @pytest.mark.parametrize(
        "browser_name",
        [
            "Mozilla Firefox",
            "Google Chrome",
            "Microsoft Edge",
            "Yandex Browser",
        ],
    )
    def test_button_changing_quantity_goods(
        self, subtests, driver, user_authorization, browser_name
    ):
        allure.dynamic.parameter("Браузер", browser_name)
        with allure.step("Открытие страницы и иницилизация объектов"):
            shop = ShopPage(driver)

        with allure.step("Получить текущее количество (до добавления)"):
            quantity_before_add = int(shop.get_product_1_quantity())
            allure.attach(
                f"Количество товаров до добавления: {quantity_before_add}",
                name="Quantity before add",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Увеличить количество товара на 1 шт"):
            shop.add_product_1()

        with allure.step("Получить текущее количество (после добавления)"):
            quantity_after_add = int(shop.get_product_1_quantity())
            allure.attach(
                f"Количество товаров после добавления: {quantity_after_add}",
                name="Quantity after add",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Проверка увеличения количества товара на 1 штуку"):
            with subtests.test(label="Добавление товара"):
                try:
                    assert quantity_after_add == quantity_before_add + 1, (
                        "Количество товара не увеличилось!"
                    )
                except AssertionError as e:
                    allure.attach(
                        str(e),
                        name="Текст ошибки",
                        attachment_type=allure.attachment_type.TEXT,
                    )
                    assert False, str(e)

        with allure.step("Уменьшить количество товара на 1 шт"):
            shop.remove_product_1()

        with allure.step("Получить текущее количество (после удаления)"):
            quantity_after_remove = int(shop.get_product_1_quantity())
            allure.attach(
                f"Количество товаров после удаления: {quantity_after_remove}",
                name="Quantity after remove",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Проверка уменьшения количества товара на 1 штуку"):
            with subtests.test(label="Удаление товара"):
                try:
                    assert quantity_after_remove == quantity_after_add - 1, (
                        "Количество товара не уменьшилось!"
                    )
                except AssertionError as e:
                    allure.attach(
                        str(e),
                        name="Текст ошибки",
                        attachment_type=allure.attachment_type.TEXT,
                    )
                    assert False, str(e)

    @allure.title(
        "Проверка видимости изменения количества товара в корзине "
        "{browser_name}"
    )
    @allure.description(
        "Проверка, что кнопки изменения количества товара увеличивают "
        "и уменьшают количество товара в корзине"
    )
    @pytest.mark.parametrize(
        "browser_name",
        [
            "Mozilla Firefox",
            "Google Chrome",
            "Microsoft Edge",
            "Yandex Browser",
        ],
    )
    def test_visibility_changing_quantity_goods_in_cart(
        self, subtests, driver, user_authorization, browser_name
    ):
        allure.dynamic.parameter("Браузер", browser_name)
        with allure.step("Открытие страницы и иницилизация объектов"):
            shop = ShopPage(driver)

        with allure.step(
            "Получить текущее количество товаров в корзине (до добавления)"
        ):
            quantity_before_add = int(shop.get_quantity_goods_in_cart())
            allure.attach(
                f"Количество товаров в корзине до добавления: "
                f"{quantity_before_add}",
                name="Quantity before add",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Увеличить количество товара в корзине на 1 шт"):
            shop.add_product_1()

        with allure.step(
                "Получить текущее количество в корзине (после добавления)"
        ):
            quantity_after_add = int(shop.get_quantity_goods_in_cart())
            allure.attach(
                f"Количество товаров в корзине после добавления: "
                f"{quantity_after_add}",
                name="Quantity after add",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step(
            "Проверка увеличения количества товара в корзине на 1 штуку"
        ):
            with subtests.test(label="Добавление товара"):
                try:
                    assert quantity_after_add == quantity_before_add + 1, (
                        "Количество товара не увеличилось"
                    )
                except AssertionError as e:
                    allure.attach(
                        str(e),
                        name="Текст ошибки",
                        attachment_type=allure.attachment_type.TEXT,
                    )
                    assert False, str(e)

        with allure.step("Уменьшить количество товара в корзине на 1 шт"):
            shop.remove_product_1()

        with allure.step(
            "Получить текущее количество товаров в корзине (после удаления)"
        ):
            quantity_after_remove = int(shop.get_quantity_goods_in_cart())
            allure.attach(
                f"Количество товаров в корзине после удаления: "
                f"{quantity_after_remove}",
                name="Quantity after remove",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step(
            "Проверка уменьшения количества товара в корзине на 1 штуку"
        ):
            with subtests.test(label="Удаление товара"):
                try:
                    assert quantity_after_remove == quantity_after_add - 1, (
                        "Количество товара не уменьшилось!"
                    )
                except AssertionError as e:
                    allure.attach(
                        str(e),
                        name="Текст ошибки",
                        attachment_type=allure.attachment_type.TEXT,
                    )
                    assert False, str(e)
