import time
import requests
from decouple import config
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
        # self._start_solve_captcha()

    def _start_solve_captcha(self) -> None:
        """Метод решения рекапчи"""

        # Собираем нужные параметры из файла с переменными окружения.
        API_KEY = config('API_KEY')
        DATA_SITE_KEY = config('DATA_SITE_KEY')
        PAGE_URL = config('PAGE_URL')

        # Составляем нужный URL-сервиса для запроса на решение капчи.
        service_url = f'http://2captcha.com/in.php?key={API_KEY}' \
                      f'&method=userrecaptcha&googlekey={DATA_SITE_KEY}' \
                      f'&pageurl={PAGE_URL}&json=1'
        # Посылаем запрос на решение капчи и делаем timeout.
        response = requests.post(service_url)
        time.sleep(30)
        # Если капча успешно принята в обработку, вернет ее id.
        print(response.json())

        # Составляем URL для получения решения капчи.
        captcha_id = response.json().get('request')
        resolve_url = f'http://2captcha.com/res.php?key={API_KEY}' \
                     f'&action=get&id={int(captcha_id)}&json=1'
        time.sleep(5)

        # Посылаем запросы до тех пор, пока не получим решение капчи
        # от сервиса.
        while True:
            response = requests.get(resolve_url)
            print(response.json())
            if response.json().get('status') == 1:
                captcha_resolve_token = response.json().get('request')
                break
            time.sleep(5)

        # Вставляем в скрытое поле решения капчи наше решение.
        self.__driver.execute_script(
            f'document.getElementById("g-recaptcha-response")'
            f'.innerHTML="{captcha_resolve_token}";'
        )
        time.sleep(3)
        # С помощью callback-функции, встроенной на сайт, отправляем решение
        # капчи на сервер.
        self.__driver.execute_script(
            f"___grecaptcha_cfg.clients['0']['L']['L']['callback']"
            f"('{captcha_resolve_token}')"
        )
