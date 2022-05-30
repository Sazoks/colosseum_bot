import time
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

    def __init__(self, driver: webdriver.Chrome, time_info: WebElement,
                 count_tickets: int, max_tickets: bool = False) -> None:
        """
        Инициализатор класса.

        :param driver: Веб-драйвер для управления браузером.
        :param time_info: Веб-элемент с информацией о времени.
        """

        self.__driver = driver
        self.__time_info = time_info
        self.__count_tickets = 2

    def _parse_max_tickets(self) -> int:
        """
        Считывание максимального количества доступных билетов для покупки.

        :return: Максимально количество билетов.
        """

        # Получение кнопки для открытия модального окна.
        open_modal_btn = self.__driver.find_element(
            By.CSS_SELECTOR,
            'btn-modalproduct.btn.btn-success.btn-block.showPerformance',
        )
        # Получение кол-ва доступных билетов.
        count_allowed_tickets_str = open_modal_btn.find_element(
            By.TAG_NAME, 'span'
        ).text
        

    def start_collect(self) -> None:
        """Процесс добавления билетов в корзину"""

        # Открываем модальное окно, щелкая по кнопке.
        modal_btn = self.__driver.find_element(
            By.CSS_SELECTOR,
            '.btn-modalproduct.btn.btn-success.btn-block.showPerformance'
        )
        webdriver.ActionChains(self.__driver).click(modal_btn).perform()

        time.sleep(2)

        # Выбор количества билетов.
        add_ticket_btn = self.__driver.find_element(
            By.CSS_SELECTOR,
            'input-group-addon.quantity.glyphicon.glyphicon-plus',
        )
