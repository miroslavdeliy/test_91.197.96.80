import allure
import pytest

from constants import MAX_QUANTITY, MAX_TOTAL, MISSING_PERSONAL_DATA_ERROR
from helpers.assertions import assert_text_equal
from pageobjects.cart_page import CartPage
from pageobjects.make_order_page import MakeOrderPage
from pageobjects.shop_page import ShopPage


class TestNegative:
    @allure.title("Проверка добавления товаров в корзину больше максимального в {browser_name}")
    @allure.description("Проверка добавления в корзину товаров больше максимального и что система не позволяет добавить больше")
    @pytest.mark.parametrize("browser_name", ["Mozilla Firefox", "Google Chrome", "Microsoft Edge", "Yandex Browser"])
    def test_more_max_goods(self, driver, user_authorization, browser_name):
        allure.dynamic.parameter("Браузер", browser_name)
        with allure.step("Открытие страницы и иницилизация объектов"):
            shop = ShopPage(driver)

        with allure.step("Добавление товаров в корзину больше максимального на 1"):
            for _ in range(MAX_QUANTITY + 1):
                shop.add_product_1()

        with allure.step(f"Проверка, что в корзине не больше {MAX_QUANTITY} штук"):
            count_goods = shop.get_quantity_goods_in_cart()
            try:
                assert int(count_goods) <= MAX_QUANTITY, f"В корзину добавляется больше {MAX_QUANTITY} единиц товара"
            except AssertionError as e:
                # В случае несовпадения - логирование ошибки
                allure.attach(str(e), name=f"Текст ошибки", attachment_type=allure.attachment_type.TEXT)
                # Принудительное падение теста
                assert False, str(e)

    @allure.title("Проверка добавления товаров в корзину на стоимость больше максимальной возможной в {browser_name}")
    @allure.description("Проверка добавления в корзину товаров больше максимальной стоимость и что система не позволяет добавить больше")
    @pytest.mark.parametrize("browser_name",
                             ["Mozilla Firefox", "Google Chrome", "Microsoft Edge", "Yandex Browser"])
    def test_more_max_total(self, driver, user_authorization, browser_name):
        allure.dynamic.parameter("Браузер", browser_name)
        with allure.step("Открытие страницы и иницилизация объектов"):
            shop = ShopPage(driver)
            cart = CartPage(driver)

        with allure.step("Перейти в корзину"):
            shop.open_cart()

        with allure.step(f"Увеличивать количество товара, пока общая сумма не превысит {MAX_TOTAL}"):
            current_total = 0
            while current_total <= MAX_TOTAL:
                cart.add_product_1()
                current_total = int(cart.get_total().split()[-2])

        with allure.step(f"Проверка, что обшая сумма не превышает {MAX_TOTAL}"):
            try:
                assert current_total <= MAX_TOTAL, "Итоговая сумма корзины больше максимальной"
            except AssertionError as e:
                # В случае несовпадения - логирование ошибки
                allure.attach(str(e), name=f"Текст ошибки", attachment_type=allure.attachment_type.TEXT)
                # Принудительное падение теста
                assert False, str(e)

    @allure.title("Проверка оформления заказа без заполнения личных данных в {browser_name}")
    @allure.description("Проверка оформления заказа без заполнения личных данных и корректность сообщения об ошибке")
    @pytest.mark.parametrize("browser_name", ["Mozilla Firefox", "Google Chrome", "Microsoft Edge", "Yandex Browser"])
    def test_without_personal_data(self, driver, user_authorization, browser_name):
        allure.dynamic.parameter("Браузер", browser_name)
        with allure.step("Открытие страницы и иницилизация объектов"):
            shop = ShopPage(driver)
            cart = CartPage(driver)
            make_order = MakeOrderPage(driver)

        with allure.step("Перейти в корзину"):
            shop.open_cart()

        with allure.step("Перейти на страницу заполнения личных данных"):
            cart.make_order()

        with allure.step("Нажать на кнопку Оформить заказ без заполнения личных данных"):
            make_order.open_finish_order()

        with allure.step("Проверка корректности сообщения об ошибки"):
            error_message = make_order.get_error_message().lower()
            assert_text_equal(error_message, MISSING_PERSONAL_DATA_ERROR.lower(),"Тест провален! Текст сообщения об ошибке некорректный")