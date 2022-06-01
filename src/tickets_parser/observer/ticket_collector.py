import time
import requests
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

        # Настройка количества билетов, которые нужно купить.
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

        # Ждем загрузки доступных билетов.
        time.sleep(6)

        # Указание количества билетов, которые надо добавить в корзину,
        # в поле ввода.
        input_count_tickets = self.__driver.find_element(
            By.ID,
            'qB6B0B700-CEEA-3087-359F-016CB3FAF5CB',
        )
        input_count_tickets.clear()
        input_count_tickets.send_keys(self.__count_tickets)

        # Прокручиваем страницу вниз до кнопки добавления в корзину.
        self.__driver.execute_script(
            'document.getElementById("myModal").scrollTo(0, document.body.scrollHeight);'
        )

        # Добавим выбранные билеты в корзину, нажав на кнопку добавления.
        add_to_cart_btn = self.__driver.find_element(
            By.CSS_SELECTOR,
            '.btn.btn-primary.addtocart',
        )
        webdriver.ActionChains(self.__driver).click(add_to_cart_btn).perform()

        # Решаем капчу.
        self._start_solve_captcha()

    def _start_solve_captcha(self):
        API_KEY = '8f1b9c417de334c6460566bb1c7e22a3'
        data_sitekey = '6LcCKasUAAAAAHzTzs_rUYyCJ3AY4awLzzw0UyQ8'
        page_url = 'https://ecm.coopculture.it/index.php?option=com_snapp&view=event&id=3793660E-5E3F-9172-2F89-016CB3FAD609&catalogid=B79E95CA-090E-FDA8-2364-017448FF0FA0&lang=it'

        service_url = f'http://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&googlekey={data_sitekey}&pageurl={page_url}&json=1'
        response = requests.post(service_url)
        time.sleep(30)
        print(response.json())

        rd1 = response.json().get('request')
        result_url = f'http://2captcha.com/res.php?key={API_KEY}&action=get&id={int(rd1)}&json=1'
        time.sleep(5)
        while True:
            r2 = requests.get(result_url)
            print(r2.json())
            if r2.json().get('status') == 1:
                form_token = r2.json().get('request')
                break
            time.sleep(5)

        self.__driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{form_token}";')
        time.sleep(3)
        self.__driver.execute_script(f"___grecaptcha_cfg.clients['0']['L']['L']['callback']('{form_token}')")
