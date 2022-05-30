import time
import datetime as dt
from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class DateTimeChecker:
    """
    Класс для проверки даты и времени на доступность.

    Отвечает за нахождение и проверку даты и времени на доступность.
    """

    def __init__(self, driver: webdriver.Chrome,
                 observed_date: dt.date, observed_time: dt.time) -> None:
        """
        Инициализатор класса.

        :param driver: Веб-драйвер для управления браузером.
        :param observed_date: Наблюдаемая дата.
        :param observed_time: Наблюдаемое время.
        """

        self.__driver = driver
        self.__observed_date = observed_date
        self.__observed_time = observed_time

    def start_check(self) -> WebElement:
        """
        Проверка указанных даты и времени на доступность.

        :return:
            Возвращает элемент, содержащий доступную дату и кнопку для старта
            процесса добавления билетов в корзину.
        """

        # Объект кнопки для переключения на следующий месяц.
        next_month_btn = self.__get_next_month_btn()
        # Получение текущего месяца и года из кнопки.
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

        # Текущая ячейка с датой в календаре.
        current_day_element: Optional[WebElement] = None

        # Находим в цикле нужную ячейку с датой.
        for day_element in days_elements:
            date_object = dt.datetime.strptime(
                day_element.get_attribute('data-date'), '%d/%m/%Y'
            ).date()
            if self.__observed_date == date_object:
                current_day_element = day_element
                break

        # Если дата доступна, открываем список со временем для старта
        # проверки доступности времени.
        if current_day_element is not None \
               and self.__allowed_day(current_day_element):
            webdriver.ActionChains(self.__driver).click(current_day_element).perform()

        time.sleep(3)

        self.__allowed_time()

        return False

    def __allowed_time(self) -> Optional[WebElement]:
        """
        Проверка доступности веб-элемента с нужным временем.

        :return: True, если время доступно, иначе False.
        """

        # Получаем количество страниц с временами.
        pages = self.__get_count_time_pages()
        current_time_elem: Optional[WebElement] = None

        # TODO: Доделать итерацию по всем страницам списка со временем.
        #   Сделать проверку, что если нужное время меньше первого времени в
        #   текущем списке, то поиск можно оставноить. Это оптимизация, потому
        #   что все времена расположены в порядке возрастания.
        # Проходимся по каждой странице.
        for _ in range(pages):
            # Получаем список текущих времен с кнопками для выбора билетов.
            current_time_list = self.__driver.find_elements(
                By.CSS_SELECTOR,
                '.perf_row.row-height2.text-center',
            )

            # Ищем в текущем списке нужное время.
            for time_elem in current_time_list:
                current_time_str = time_elem.find_element(By.TAG_NAME, 'div') \
                    .find_element(By.TAG_NAME, 'div').text
                current_time_obj = dt.datetime.strptime(current_time_str, '%H:%M').time()
                if self.__observed_time == current_time_obj:
                    return time_elem

            # Если в текущем списке нужн

        return current_time_elem

    def __get_count_time_pages(self) -> int:
        """Получение количества страниц списка со временем"""

        # Открытый список с навигационной панелью.
        navigation = self.__driver.find_element(By.ID, 'prfrmncPages')

        # Если панель навигации пуста, значит, есть только одна страница.
        if navigation.text == '':
            return 1

        # Если панель навигации не пуста, собираем все элементы списка.
        li_list = navigation.find_element(By.TAG_NAME, 'ul') \
            .find_elements(By.TAG_NAME, 'li')

        # Предпоследний элемент - элемент, содержащий номер последней страницы.
        value = int(li_list[-2].find_element(By.TAG_NAME, 'a').text)

        return value

    def __allowed_day(self, day_element: WebElement) -> bool:
        """
        Проверка ячейки с датой календаря на доступность.

        Цвет заднего фона ячейки определяет доступноть даты.

        :return: True, если дата доступна, иначе False.
        """

        # Получение родительского элемента. У него и проверяем цвет фона.
        parent = day_element.find_element(By.XPATH, '..')

        ALLOWED_DATE_COLOR = 'rgba(206, 234, 208, 1)'
        css_rgb = parent.value_of_css_property('background-color')

        return css_rgb == ALLOWED_DATE_COLOR

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
