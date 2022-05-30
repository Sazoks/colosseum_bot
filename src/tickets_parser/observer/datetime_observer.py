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

from .datetime_checker import DateTimeChecker


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

            # Создаем чекер даты и времени.
            datetime_checker = DateTimeChecker(
                self.__driver,
                self.__observed_date,
                self.__observed_time,
            )

            time.sleep(5)

            # Проверяем, доступны ли дата и время для покупки билетов.
            allowed_time_element = datetime_checker.start_check()

            # Если элемент с нужным временем есть, начинаем процесс сбора
            # билетов в корзину.
            if allowed_time_element is not None:
                print('Время есть!')
            else:
                print('Времени нет!')

            return

            # После успешного парсинга добавляем в планировщик новую задачу,
            # на мониторинг. Цикл повторяется до тех пор, пока флаг
            # self__worked установлен в True.
            self._add_check_task()

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
