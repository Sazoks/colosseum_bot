import time
import random
import datetime as dt
from typing import Optional
from apscheduler.job import Job
from apscheduler.schedulers.background import BackgroundScheduler
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class DateTimeObserver:
    """
    Класс для мониторинга даты и времени.

    Мониторит указанную дату и время и, если дата и время доступны,
    сообщает об этом парсеру билетов.
    """

    def __init__(self,
                 url: Optional[str] = None,
                 observer_date: Optional[dt.date] = None,
                 observer_time: Optional[dt.time] = None) -> None:
        """
        Инициализатор класса.

        :param url: URL-адрес наблюдаемой страницы.
        :param observer_date: Наблюдаемая дата.
        :param observer_time: Наблюдаемое время.
        """

        # Параметры наблюдателя.
        self.__url = url
        self.__observed_date = observer_date
        self.__observed_time = observer_time

        # Системные параметры наблюдателя.
        self.__scheduler: Optional[BackgroundScheduler] = None
        self.__current_job: Optional[Job] = None
        self.__worked = False

        # Инициализируем веб-драйвер.
        self.__driver: Optional[webdriver.Chrome] = None

    def set_params(self, url: str, observer_date: dt.date,
                   observer_time: dt.time) -> None:
        """
        Установка параметров для наблюдателя.

        :param url: URL-адрес наблюдаемой страницы.
        :param observer_date: Наблюдаемая дата.
        :param observer_time: Наблюдаемое время.
        """

        self.__url = url
        self.__observed_date = observer_date
        self.__observed_time = observer_time

    @property
    def worked(self) -> bool:
        """Получение статуса наблюдателя"""

        return self.__worked

    def start(self) -> None:
        """
        Запуск наблюдения за датой и временем.

        Инициализирует веб-драйвер, добавляет в планировщик задачу на
        мониторинг доступных билетов, запускает планировщик.
        """

        # Запускаем наблюдатель только в том случае, если все параметры
        # заданы верно и наблюдатель уже не запущен.
        if not self.__worked and self._check_params():
            self.__worked = True
            self.__driver = webdriver.Chrome(ChromeDriverManager().install())
            self.__scheduler = BackgroundScheduler()
            self._add_check_task()
            self.__scheduler.start()
        else:
            print('Ошибка. Необходимо настроить все параметры: URL-адрес '
                  'страницы, наблюдаемые дату и время.')

    def stop(self) -> None:
        """
        Остановка наблюдателя.

        Закрывает веб-драйвер, выключает планировщик задач.
        """

        if self.__worked:
            self.__worked = False
            self.__scheduler.shutdown()
            self.__scheduler = None
            self.__driver.close()  # FIXME: Сделать проверку на открытое окно.
            self.__driver = None

    def _check_params(self) -> bool:
        """Проверка параметров наблюдателя"""

        return self.__url is not None and self.__observed_date is not None \
               and self.__observed_time is not None

    def _check_allowed_tickets(self) -> None:
        """Проверка доступных билетов на странице"""

        # Если наблюдатель в активном режиме, парсим доступные билеты.
        # Если нет, работающая задача выполнится, и больше задач на парсинг
        # поступать не будет.
        if self.__worked:
            # Открытие указанной страницы.
            self.__driver.get(self.__url)

            time.sleep(5)

            # Объект кнопки для переключения на следующий месяц.
            next_month_btn = self.__get_next_month_btn()
            # Получение текущего месяца и года.
            current_date = self.__get_current_date(next_month_btn)

            # Переключаем месяца в календаре до тех пор, пока не найдем
            # нужный месяц и год.
            while current_date.month != self.__observed_date.month \
                    or current_date.year != self.__observed_date.year:
                webdriver.ActionChains(self.__driver).click(next_month_btn).perform()
                time.sleep(1)
                next_month_btn = self.__get_next_month_btn()
                current_date = self.__get_current_date(next_month_btn)

            time.sleep(1)

            # Парсим все дни в календаре.
            days_elements = self.__driver.find_elements(
                By.CSS_SELECTOR,
                '.calendar-day > .day-number',
            )
            # Создаем список с датами типа datetime.date.
            days = [
                dt.datetime.strptime(day_element.get_attribute('data-date'), '%d/%m/%Y').date()
                for day_element in days_elements
            ]

            return

            # После успешного парсинга добавляем в планировщик новую задачу,
            # на мониторинг. Цикл повторяется до тех пор, пока флаг
            # self__worked установлен в True.
            self._add_check_task()

    def __get_next_month_btn(self) -> WebElement:
        """
        Получение кнопки переключения следующего месяца.

        Необходимо получать ее каждый раз, т.к. в ней меняются параметры
        следующих месяца и года.

        :return: Кнопка переключения на следующий месяц.
        """

        next_month_btn = self.__driver.find_element(
            By.CSS_SELECTOR,
            '.next.changemonth.glyphicon.glyphicon-chevron-right',
        )

        return next_month_btn

    def __get_current_date(self, next_month_btn: WebElement) -> dt.date:
        """
        Получение текущего месяца и года в календаре.

        :param next_month_btn:
            Кнопка переключения месяцев, из которой вычисляем
            текущие месяц и год.
        :return: Объект даты с вычисленными годом и месяцем.
        """

        # Получение из кнопки следующих месяца и года.
        next_month = int(next_month_btn.get_attribute('data-month'))
        next_year = int(next_month_btn.get_attribute('data-year'))

        # Вычисление текущих месяца и года.
        current_year = next_year
        current_month = next_month - 1
        # Учет того, что следующий месяц может быть первым.
        if current_month == 0:
            current_month = 12
            current_year -= 1

        return dt.date(year=current_year, month=current_month, day=1)

    def _add_check_task(self) -> None:
        """Добавление задачи проверки доступных билетов"""

        # Настраиваем одноразовое событие на выполнение через delay минут.
        delay = random.randint(1, 3)
        delay = 0  # FIXME: Убрать. Нужно для ручного тестирования.
        run_date = dt.datetime.now() + dt.timedelta(minutes=delay)
        self.__current_job = self.__scheduler.add_job(
            func=self._check_allowed_tickets,
            trigger='date',
            run_date=run_date,
        )
