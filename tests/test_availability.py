import allure
import pytest

from pageobjects.shop_page import ShopPage


class TestAvailability:
    @allure.title("Проверка наличия альтернативного текста у изображений в {browser_name}")
    @allure.description("Проверка наличия альтернативного текста у изображений в случае неудачной загрузки")
    @pytest.mark.parametrize("browser_name", ["Mozilla Firefox", "Google Chrome", "Microsoft Edge", "Yandex Browser"])
    def test_alt_image(self, driver, user_authorization, browser_name):
        allure.dynamic.parameter("Браузер", browser_name)

        with allure.step("Открытие страницы и иницилизация объектов"):
            shop = ShopPage(driver)

        with allure.step("Получить альтернативный текст для изображений"):
            alt_text_image = shop.get_alt_text_image()
            try:
                assert alt_text_image, "У изображения отсутствует alt-text"
            except AssertionError as e:
                # В случае несовпадения - логирование ошибки
                allure.attach(str(e), name=f"Текст ошибки", attachment_type=allure.attachment_type.TEXT)
                # Принудительное падение теста
                assert False, str(e)