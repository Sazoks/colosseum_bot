import time
from typing import (
    List,
    Union,
    Optional,
)
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException


def wait_element(
        base_element: Union[WebElement, webdriver.Chrome],
        select_by: str,
        select_value: str,
        many: bool = False
) -> Optional[Union[WebElement, List[WebElement]]]:
    """
    Функция ожидания загрузки веб-элемента по селектору.

    :param base_element: Базовый элемент, откуда искать, либо драйвер.
    :param select_by: По какому селектру искать элемент.
    :param select_value: Значение селектора.
    :param many:
        Флаг, указывающий, нужно выбирать один или множество элементво.
    :return: Найденные по указанному селектору веб-элементы.
    """

    # Пытаем получить доступ к элементу до тех пор, пока
    # успешно не получим его.
    while True:
        try:
            if not many:
                return base_element.find_element(select_by, select_value)
            else:
                return base_element.find_elements(select_by, select_value)
        except NoSuchElementException as e:
            print(e)
            time.sleep(1)
