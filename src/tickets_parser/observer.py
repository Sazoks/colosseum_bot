import time
import random
import datetime as dt
from typing import Optional
from PyQt5.QtWidgets import QMessageBox
from apscheduler.job import Job
from apscheduler.schedulers.background import BackgroundScheduler
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from .datetime_checker import DateTimeChecker
from .ticket_collector import TicketCollector
from .informer import Informer


class Observer:
    """
    Класс для мониторинга даты и времени.

    Мониторит указанную дату и время и, если дата и время доступны,
    сообщает об этом парсеру билетов.
    """

    def __init__(self,
                 url: Optional[str] = None,
                 observer_date: Optional[dt.date] = None,
                 observer_time: Optional[dt.time] = None,
                 count_tickets: int = 1,
                 max_tickets: bool = False,
                 informer: Optional[Informer] = None) -> None:
        """
        Инициализатор класса.

        :param url: URL-адрес наблюдаемой страницы.
        :param observer_date: Наблюдаемая дата.
        :param observer_time: Наблюдаемое время.
        :param count_tickets:
            Количество билетов, которые необходимо добавить в корзину.
        :param max_tickets: Брать ли все доступные билеты, которые есть.
        :param informer: Объект информера для отслеживания состояния бота.
        """

        # Параметры наблюдателя.
        self.__url = url
        self.__observed_date = observer_date
        self.__observed_time = observer_time
        self.__count_tickets = count_tickets
        self.__max_tickets = max_tickets

        # Системные параметры наблюдателя.
        self.__scheduler: Optional[BackgroundScheduler] = None
        self.__current_job: Optional[Job] = None
        self.__worked = False
        self.__driver: Optional[webdriver.Chrome] = None
        self.__informer = informer

    def set_params(self, url: str,
                   observer_date: dt.date,
                   observer_time: dt.time,
                   count_tickets: int = 1,
                   max_tickets: bool = False,
                   informer: Optional[Informer] = None) -> None:
        """
        Установка параметров для наблюдателя.

        :param url: URL-адрес наблюдаемой страницы.
        :param observer_date: Наблюдаемая дата.
        :param observer_time: Наблюдаемое время.
        :param count_tickets:
            Количество билетов, которые необходимо добавить в корзину.
        :param max_tickets: Брать ли все доступные билеты, которые есть.
        :param informer: Объект информера для отслеживания состояния бота.
        """

        self.__url = url
        self.__observed_date = observer_date
        self.__observed_time = observer_time
        self.__count_tickets = count_tickets
        self.__max_tickets = max_tickets
        self.__informer = informer

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
            self.__informer.push_message(
                'Запуск бота...',
                Informer.MessageLevel.INFO,
            )

            self.__worked = True

            # Устанавливаем окно барузера на весь экран.
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--start-maximized")
            self.__driver = webdriver.Chrome(
                ChromeDriverManager().install(),
                options=chrome_options,
            )

            self.__scheduler = BackgroundScheduler()
            self._add_check_task()
            self.__scheduler.start()

            self.__informer.push_message(
                'Бот запущен',
                Informer.MessageLevel.INFO,
            )
        else:
            print('Ошибка. Необходимо настроить все параметры: URL-адрес '
                  'страницы, наблюдаемые дату и время.')

    def stop(self) -> None:
        """
        Остановка наблюдателя.

        Закрывает веб-драйвер, выключает планировщик задач.
        """

        self.__informer.push_message(
            'Остановка бота...',
            Informer.MessageLevel.INFO,
        )

        if self.__worked:
            self.__worked = False
            self.__scheduler.shutdown()
            self.__scheduler = None

            # Пользователь может сначала закрыть окно браузера, а затем
            # нажать на кнопку "Стоп", что вызовет ошибку.
            # Исключим такое поведение.
            try:
                self.__driver.close()
            except WebDriverException as e:
                print(e)

            self.__driver = None

        self.__informer.push_message(
            'Бот остановлен',
            Informer.MessageLevel.INFO,
        )

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
            # Плашка с куки мешается при взаимодействии с элементами страницы.
            # Попытаемся закрыть ее, если она есть.
            try:
                self._close_cookie_card()
            except Exception:
                pass

            # Создаем чекер даты и времени.
            datetime_checker = DateTimeChecker(
                driver=self.__driver,
                observed_date=self.__observed_date,
                observed_time=self.__observed_time,
                informer=self.__informer,
            )

            # Проверяем, доступны ли дата и время для покупки билетов.
            # Если дата и время доступны, до возвращается веб-элементы
            # карточки со временем и кнопкой открытия модального окна для
            # выбора билетов.
            # Это необходимо для следующего этапа - добавления билетов в
            # корзину и обхода капчи.
            allowed_time_element = datetime_checker.start_check()

            # Если элемент с нужным временем есть, начинаем процесс сбора
            # билетов в корзину.
            if allowed_time_element is not None:
                # Запускаем сборщик билетов в корзину.
                ticket_collector = TicketCollector(
                    driver=self.__driver,
                    time_info=allowed_time_element,
                    count_tickets=self.__count_tickets,
                    max_tickets=self.__max_tickets,
                    informer=self.__informer,
                )
                ticket_collector.start_collect()
                self.__informer.push_message(
                    'Билеты собраны. Чтобы запустить новое сканирование, остановите бота, '
                    'укажите новые дату и время и нажмите на кнопку "Начать мониторинг"',
                    Informer.MessageLevel.INFO,
                )
                return
            else:
                self.__informer.push_message(
                    f'Билеты на {self.__observed_date} {self.__observed_time} '
                    f'не обнаружены',
                    Informer.MessageLevel.INFO,
                )

            # После успешного парсинга добавляем в планировщик новую задачу,
            # на мониторинг. Цикл повторяется до тех пор, пока флаг
            # self__worked установлен в True.
            self._add_check_task()

    def _close_cookie_card(self) -> None:
        """Метод закрытия плашки с куки"""

        self.__driver.find_element(By.CLASS_NAME, 'gdpr_denyClose').click()

    def _add_check_task(self) -> None:
        """Добавление задачи проверки доступных билетов"""

        # Настраиваем одноразовое событие на выполнение через delay минут.
        delay = random.randint(1, 3)
        self.__informer.push_message(
            f'Следующее сканирование начнется через {delay} минут',
            Informer.MessageLevel.INFO,
        )
        run_date = dt.datetime.now() + dt.timedelta(minutes=delay)
        self.__current_job = self.__scheduler.add_job(
            func=self._check_allowed_tickets,
            trigger='date',
            run_date=run_date,
        )
