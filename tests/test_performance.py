import allure
import pytest

from constants import MAX_LOAD_TIME_MS


class TestPerformance:

    @allure.title("Проверка времени загрузки главной страницы в  {browser_name}")
    @allure.description("Проверка что время загрузки главной страницы не превышает допустимое")
    @pytest.mark.parametrize("browser_name", ["Mozilla Firefox", "Google Chrome", "Microsoft Edge", "Yandex Browser"])
    def test_time_load(self, driver, browser_name):
        allure.dynamic.parameter("Браузер", browser_name)
        with allure.step("Получение времени начала и окончания загрузки страницы"):
            # Выполняем JavaScript для получения времени загрузки
            load_event_end = driver.execute_script("return window.performance.timing.loadEventEnd")
            navigation_start = driver.execute_script("return window.performance.timing.navigationStart")
            load_time_ms = load_event_end - navigation_start
            allure.attach(str(load_time_ms), name=f"Время загрузки", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверка, что время загрузки не превышает допустимое"):
            try:
                assert load_time_ms <= MAX_LOAD_TIME_MS, f"Главная страница загружалась слишком долго: {load_time_ms} мс"
            except AssertionError as e:
                # В случае несовпадения - логирование ошибки
                allure.attach(str(e), name=f"Текст ошибки", attachment_type=allure.attachment_type.TEXT)
                # Принудительное падение теста
                assert False, str(e)