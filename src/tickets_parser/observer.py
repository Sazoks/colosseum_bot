import random
import datetime
from typing import Optional
from apscheduler.job import Job
from apscheduler.schedulers.background import BackgroundScheduler
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class DateTimeObserver:
    """
    Класс для мониторинга даты и времени.

    Мониторит указанную дату и время и, если дата и время доступны,
    сообщает об этом парсеру билетов.
    """

    def __init__(self, url: str, observer_date: datetime.date,
                 observer_time: datetime.time) -> None:
        """
        Инициализатор класса.

        :param url: Адрес страницы для парсинга.
        :param observer_date: Наблюдаемая дата.
        :param observer_time: Наблюдаемое время.
        """

        self.__url = url
        self.__observed_date = observer_date
        self.__observed_time = observer_time
        self.__scheduler = BackgroundScheduler()
        self.__current_job: Optional[Job] = None
        self.__worked = False

        # Объект веб-драйвера. Изначально не проинициализирован.
        # Инициализируется при старте наблюдателя.
        self.__driver: Optional[webdriver.Chrome] = None

    @property
    def worked(self) -> bool:
        return self.__worked

    def start(self) -> None:
        """
        Запуск наблюдения за датой и временем.

        Инициализирует веб-драйвер, открывает указанную при инициализации
        наблюдателя страницу, добавляет в планировщик задачу на мониторинг
        доступных билетов, запускает планировщик.
        """

        self.__worked = True
        self.__driver = webdriver.Chrome(ChromeDriverManager().install())
        self.__driver.get(self.__url)
        self._add_check_task()
        self.__scheduler.start()

    def stop(self) -> None:
        """
        Остановка наблюдателя.

        Закрывает веб-драйвер, выключает планировщик задач.
        """

        self.__worked = False
        self.__driver.close()
        self.__driver = None
        self.__scheduler.shutdown()

    def _check_allowed_tickets(self) -> None:
        """Проверка доступных билетов"""

        # Если наблюдатель в активном режиме, парсим доступные билеты.
        # Если нет, работающая задача выполнится, и больше задач на парсинг
        # поступать не будет.
        if self.__worked:
            print('123')
            return
            driver = webdriver.Chrome()
            driver.get(self.__url)


            driver.close()

            # После успешного парсинга добавляем в планировщик новую задачу.
            self._add_check_task()

    def _add_check_task(self) -> None:
        """Добавление задачи проверки доступных билетов"""

        # Настраиваем одноразовое событие на выполнение через delay минут.
        delay = random.randint(1, 3)
        delay = 0  # FIXME: Убрать. Нужно для ручного тестирования.
        run_date = datetime.datetime.now() + datetime.timedelta(minutes=delay)
        self.__current_job = self.__scheduler.add_job(
            func=self._check_allowed_tickets,
            trigger='date',
            run_date=run_date,
        )
