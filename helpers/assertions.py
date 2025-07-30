import allure

from constants import SHOP_HEADER_TEXT

def assert_login_successful(shop, role: str = "Пользователь"):

    actual_text = shop.get_shop_header_text().strip().lower()
    try:
        assert actual_text == SHOP_HEADER_TEXT, f"{role} не авторизован!"
    except AssertionError as e:
        # В случае несовпадения - логирование ошибки
        allure.attach(
            str(e),
            name=f"Текст ошибки",
            attachment_type=allure.attachment_type.TEXT
        )
        # Принудительное падение теста
        assert False, str(e)

# Функция сравнения полученных значений с ожидаемыми с помощью assert
def assert_text_equal(actual, expected, message=""):
    try:
        # Сравнение текстовых значений
        assert actual in expected, \
            f"{message}\nОжидалось: '{expected}', получено: '{actual}'"
    except AssertionError as e:
        # В случае несовпадения - логирование ошибки
        allure.attach(
            str(e),
            name=f"Текст ошибки",
            attachment_type=allure.attachment_type.TEXT
        )
        # Принудительное падение теста
        assert False, str(e)
