import time
from typing import (
    List,
    Optional,
)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class TicketCollector:
    """
    Класс для добавления билетов в корзину.

    Отвечает за обход капчи и добавление билетов в корзину.
    """

    def __init__(self, driver: webdriver.Chrome, time_info: WebElement, *,
                 count_tickets: int = 1,  max_tickets: bool = False) -> None:
        """
        Инициализатор класса.

        :param driver: Веб-драйвер для управления браузером.
        :param time_info: Веб-элемент с информацией о времени.
        :param count_tickets: Количество билетов, которое нужно собрать.
        :param max_tickets: Нужно ли собирать максимальное количесвто билетов.
        """

        self.__driver = driver
        self.__time_info = time_info
        self.__max_tickets = self._parse_max_tickets()
        self.__count_tickets = count_tickets
        if max_tickets or self.__count_tickets > self.__max_tickets:
            self.__count_tickets = self.__max_tickets

    def _parse_max_tickets(self) -> int:
        """
        Считывание максимального количества доступных билетов для покупки.

        :return: Максимально количество билетов.
        """

        # Получение кнопки для открытия модального окна.
        open_modal_btn = self.__time_info.find_element(
            By.CSS_SELECTOR,
            '.btn-modalproduct.btn.btn-success.btn-block.showPerformance',
        )
        # Получение кол-ва доступных билетов.
        count_allowed_tickets_str = open_modal_btn.find_element(
            By.TAG_NAME, 'span'
        ).text

        # Убираем скобки (первый и последний символы) и конвертируем строку
        # в число.
        count_allowed_tickets = int(
            count_allowed_tickets_str[1:len(count_allowed_tickets_str) - 1]
        )

        return count_allowed_tickets

    def start_collect(self) -> None:
        """Процесс добавления билетов в корзину"""

        # Открываем модальное окно, щелкая по кнопке.
        modal_btn = self.__time_info.find_element(
            By.CSS_SELECTOR,
            '.btn-modalproduct.btn.btn-success.btn-block.showPerformance'
        )
        webdriver.ActionChains(self.__driver).click(modal_btn).perform()

        time.sleep(6)

        # Указание количества билетов, которые надо добавить в корзину,
        # в поле ввода.
        input_count_tickets = self.__driver.find_element(
            By.ID,
            'qB6B0B700-CEEA-3087-359F-016CB3FAF5CB',
        )
        input_count_tickets.clear()
        input_count_tickets.send_keys(self.__count_tickets)
