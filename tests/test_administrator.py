import allure
import pytest

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from constants import (
    EDIT_GOODS_HEADER_TEXT,
    NEW_GOOD_NAME,
    NEW_GOOD_DESCRIPTION,
    NEW_GOOD_CATEGORY,
    NEW_GOOD_PRICE,
    NEW_GOOD_IMAGE_URL,
    EDITED_GOOD_NAME,
    EDITED_GOOD_DESCRIPTION,
    EDITED_GOOD_CATEGORY,
    EDITED_GOOD_PRICE,
    EDITED_GOOD_IMAGE_URL
)
from helpers.assertions import assert_text_equal
from pageobjects.edit_goods_page import EditGoodsPage
from pageobjects.edit_product_page import EditProductPage
from pageobjects.make_good_page import MakeGoodPage
from pageobjects.menu_page import MenuPage


class TestAdministrator:
    @allure.title(
        "Проверка кнопки Обратно к товарам на странице создания товаров в "
        "{browser_name}"
    )
    @allure.description(
        "Проверка, что кнопка Обратно к товарам на странице создания товаров "
        "переводит на страницу со списком товаров"
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
    def test_button_back_from_make_good(
            self, driver, admin_authorization, browser_name
    ):
        with allure.step("Открытие страницы и иницилизация объектов"):
            menu = MenuPage(driver)
            edit = EditGoodsPage(driver)
            make_good = MakeGoodPage(driver)

        with allure.step("Открыть меню и нажать на 'Редактирование товаров'"):
            menu.open_menu()
            menu.open_edit()

        with allure.step("Клик по кнопке Добавить товар"):
            edit.add_good()

        with allure.step("Клик по кнопке Обратно к товарам"):
            make_good.back_goods()

        with allure.step(
                "Проверка нахождения на странице редактирования товаров"
        ):
            edit_header_text = edit.get_edit_header_text().lower()
            # Сравнение заголовка страницы редактирования товаров с ожидаемым
            assert_text_equal(
                edit_header_text,
                EDIT_GOODS_HEADER_TEXT.lower(),
                "Кнопка Обратно к товарам не переводит на страницу к товарам"
            )

    @allure.title(
        "Проверка кнопки Обратно к товарам на странице редактирования товаров "
        "в {browser_name}"
    )
    @allure.description(
        "Проверка, что кнопка Обратно к товарам на странице редактирования "
        "товаров переводит на страницу со списком товаров"
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
    def test_button_back_from_edit_good(
            self, driver, admin_authorization, browser_name
    ):
        with allure.step("Открытие страницы и иницилизация объектов"):
            menu = MenuPage(driver)
            edit = EditGoodsPage(driver)
            edit_good = EditProductPage(driver)

        with allure.step("Открыть меню и нажать на 'Редактирование товаров'"):
            menu.open_menu()
            menu.open_edit()

        with allure.step("Клик по кнопке редактирования 1-го товара"):
            edit.open_edit_product_1()

        with allure.step("Клик по кнопке Обратно к товарам"):
            edit_good.back_goods()

        with allure.step(
                "Проверка нахождения на странице редактирования товаров"
        ):
            edit_header_text = edit.get_edit_header_text().lower()
            # Сравнение заголовка страницы редактирования товаров с ожидаемым
            assert_text_equal(
                edit_header_text,
                EDIT_GOODS_HEADER_TEXT.lower(),
                "Кнопка Обратно к товарам не переводит на страницу к товарам"
            )

    @allure.title(
        "Проверка создания, редактирования и удаления товара в {browser_name}"
    )
    @allure.description("Проверка создания, редактирования и удаления товара")
    @pytest.mark.parametrize(
        "browser_name",
        [
            "Mozilla Firefox",
            "Google Chrome",
            "Microsoft Edge",
            "Yandex Browser"
        ]
    )
    def test_make_edit_delete_good(
            self, subtests, driver, admin_authorization, browser_name
    ):
        with allure.step("Открытие страницы и иницилизация объектов"):
            menu = MenuPage(driver)
            edit = EditGoodsPage(driver)
            make_good = MakeGoodPage(driver)
            edit_product = EditProductPage(driver)

        with allure.step("Открыть меню и нажать на 'Редактирование товаров'"):
            menu.open_menu()
            menu.open_edit()

        # Тестирования создания товара
        with allure.step("Проверка создания товаров"):
            with allure.step("Клик по кнопке Добавить товар"):
                edit.add_good()

            with allure.step("Заполнить данные нового товара"):
                # Заполнение формы нового товара
                make_good.enter_name(NEW_GOOD_NAME)
                make_good.enter_description(NEW_GOOD_DESCRIPTION)
                make_good.enter_category(NEW_GOOD_CATEGORY)
                make_good.enter_price(NEW_GOOD_PRICE)
                make_good.enter_url(NEW_GOOD_IMAGE_URL)

            with allure.step("Клик по кнопке 'Создать товар'"):
                make_good.make_good()

            with allure.step(
                    "Сохранение фактических значений созданного товара"
            ):
                actual_name_maked_good = edit.get_name().lower()
                actual_description_maked_good = edit.get_description().lower()
                actual_category_maked_good = edit.get_category().lower()
                actual_price_maked_good = edit.get_price().lower()
                actual_image_url_maked_good = edit.get_image_maked_good()

            with allure.step("Проверка полученных значений"):
                # Подготовка ожидаемых значений
                expected_name_maked_good = NEW_GOOD_NAME.lower()
                expected_description_maked_good = NEW_GOOD_DESCRIPTION.lower()
                expected_category_maked_good = (
                    f"категория: {NEW_GOOD_CATEGORY}"
                ).lower()
                expected_price_maked_good = (
                    f"цена: {NEW_GOOD_PRICE}.00 ₽"
                ).lower()
                expected_image_url_maked_good = NEW_GOOD_IMAGE_URL

                # Подготовка проверок
                data_maked_goods = [
                    (
                        "Название",
                        actual_name_maked_good,
                        expected_name_maked_good
                    ),
                    (
                        "Описание",
                        actual_description_maked_good,
                        expected_description_maked_good
                    ),
                    (
                        "Категория",
                        actual_category_maked_good,
                        expected_category_maked_good
                    ),
                    (
                        "Цена",
                        actual_price_maked_good,
                        expected_price_maked_good
                    ),
                    (
                        "URL изображения",
                        actual_image_url_maked_good,
                        expected_image_url_maked_good
                    )
                ]

                # Прогон по значениям и сравнение с ожидаемыми
                for label, actual, expected in data_maked_goods:
                    with allure.step(f"Проверка {label}"):
                        with subtests.test(label=label):
                            # Логирование ожидаемых и фактических значений
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

                            # Сравнение текстовых значений
                            assert_text_equal(
                                actual,
                                expected,
                                f"{label} товара некорректно"
                            )

        # Тестирования редактирования товара
        with allure.step("Проверка редактирования товара"):
            with allure.step("Клик по кнопке Редактировать товар"):
                edit.open_edit_product_5()

            with allure.step("Ввести новые значения"):
                # Заполнение формы редактирования товара
                edit_product.clear_and_enter_name(EDITED_GOOD_NAME)
                edit_product.clear_and_enter_description(
                    EDITED_GOOD_DESCRIPTION
                )
                edit_product.clear_and_enter_category(EDITED_GOOD_CATEGORY)
                edit_product.clear_and_enter_price(EDITED_GOOD_PRICE)
                edit_product.clear_and_enter_url(EDITED_GOOD_IMAGE_URL)

            with allure.step("Клик по кнопке 'Обновить товар'"):
                edit_product.edit_product()

            with allure.step(
                    "Сохранение фактических значений обновленного товара"
            ):
                actual_name_edited_good = edit.get_name()
                actual_description_edited_good = edit.get_description()
                actual_category_edited_good = edit.get_category()
                actual_price_edited_good = edit.get_price()
                actual_image_url_edited_good = edit.get_image_maked_good()

            with allure.step("Проверка полученных значений"):
                # Подготовить ожидаемые значения
                expected_name_edited_good = EDITED_GOOD_NAME
                expected_description_edited_good = (
                    EDITED_GOOD_DESCRIPTION.lower()
                )
                expected_category_edited_good = (
                    f"категория: {EDITED_GOOD_CATEGORY}"
                ).lower()
                expected_price_edited_good = (
                    f"цена: {EDITED_GOOD_PRICE}.00 ₽"
                ).lower()
                expected_image_url_edited_good = EDITED_GOOD_IMAGE_URL

                # Подготовка проверок
                data_edited_good = [
                    (
                        "Название",
                        actual_name_edited_good,
                        expected_name_edited_good
                    ),
                    (
                        "Описание",
                        actual_description_edited_good,
                        expected_description_edited_good
                    ),
                    (
                        "Категория",
                        actual_category_edited_good,
                        expected_category_edited_good
                    ),
                    (
                        "Цена",
                        actual_price_edited_good,
                        expected_price_edited_good
                    ),
                    (
                        "URL изображения",
                        actual_image_url_edited_good,
                        expected_image_url_edited_good
                    )
                ]

                # Прогон по значениям и сравнение с ожидаемыми
                for label, actual, expected in data_edited_good:
                    with allure.step(f"Проверка {label}"):
                        with subtests.test(label=label):
                            # Логирование ожидаемых и фактических значений
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

                            # Сравнение текстовых значений
                            assert_text_equal(
                                actual,
                                expected,
                                f"{label} товара некорректно"
                            )

        # Тестирования удаления товара
        with allure.step("Проверка удаления товара"):
            with allure.step("Сохранить название удаляемого товара"):
                good_name = edit.get_name()
            with allure.step("Нажать кнопку удаления товара"):
                edit.delete_product()

            with allure.step("Ожидание удаление товара"):
                try:
                    # Ожидание исчезновения товара
                    WebDriverWait(driver, 10).until(
                        EC.invisibility_of_element_located(
                            (
                                By.XPATH,
                                f'//div[contains(text(), "{good_name}")]'
                            )
                        )
                    )
                except TimeoutException:
                    # В случае неудачи логировать ошибку
                    error_message = f"{good_name} не удалился"
                    allure.attach(
                        error_message,
                        name=f"Текст ошибки",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    # Принудительное падение теста
                    assert False, error_message