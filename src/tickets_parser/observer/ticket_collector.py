from typing import (
    List,
)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class TicketCollector:
    """
    Класс для добавления билетов в корзину.

    Отвечает за обход капчи и добавление билетов в корзину.
    """

    def __init__(self, driver: webdriver.Chrome) -> None:
        """
        Инициализатор класса.

        :param driver: Веб-драйвер для управления браузером.
        """

        self.__driver = driver

    def start_collect(self) -> None:
        """Процесс добавления билетов в корзину"""

        ...
