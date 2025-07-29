from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def wait_for_element(
        driver,
        by,
        locator,
        timeout=15,
        condition="visible"
):
    try:
        wait = WebDriverWait(driver, timeout)
        condition_map = {
            "visible": EC.visibility_of_element_located,
            "present": EC.presence_of_element_located,
            "clickable": EC.element_to_be_clickable,
        }
        condition_func = condition_map.get(condition, EC.visibility_of_element_located)
        return wait.until(condition_func((by, locator)))
    except TimeoutException:
        raise TimeoutException(f"Элемент не найден: {locator} ({condition})")
    except NoSuchElementException:
        raise NoSuchElementException(f"Нет такого элемента: {locator}")