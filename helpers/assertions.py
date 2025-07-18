from constants import SHOP_HEADER_TEXT

def assert_login_successful(shop, role: str = "Пользователь"):

    actual_text = shop.get_shop_header_text().strip().lower()
    assert actual_text == SHOP_HEADER_TEXT, f"{role} не авторизован! Ожидалось: '{SHOP_HEADER_TEXT}', получено: '{actual_text}'"


def assert_text_equal(actual, expected, message=""):
    assert actual in expected, f"{message}\nОжидалось: '{expected}', получено: '{actual}'"