import datetime as dt
from PyQt5 import QtWidgets

from ui.main_window import Ui_MainWindow
from tickets_parser.observer import Observer
from tickets_parser.informer import Informer


class MainWindow(QtWidgets.QMainWindow):
    """
    Класс главного окна.

    Обрабатывает все сигналы главного окна.
    """

    def __init__(self) -> None:
        """Инициализатор класса"""

        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Colosseum Bot')

        # Информер для получения информации о состоянии бота.
        self.__informer = Informer('logs.log', self.ui.bot_info_input)
        # Наблюдатель за доступными билетами.
        self.__observer = Observer()

        # Подключаем обработчик сигнала для старта мониторинга.
        self.ui.start_monitoring.clicked.connect(self._init_observer_slot)
        # Подключаем обработчик сигнала для остановки мониторинга.
        self.ui.stop_monitoring.clicked.connect(self._stop_observer_slot)

    def _init_observer_slot(self) -> None:
        """Инициализация наблюдателя за билетами"""

        # Считываение всех значений.
        date = dt.datetime.strptime(self.ui.date_input.text(), '%d.%m.%Y').date()
        time = dt.datetime.strptime(self.ui.time_input.text(), '%H:%M').time()
        count_tickets = self.ui.tickets_input.value()
        max_tickets = self.ui.max_tickets.isChecked()

        # Настройка и запуск наблюдателя.
        if not self.__observer.worked:
            self.__set_active_start_monitor_btn(False)
            self.__observer.set_params(
                url='https://ecm.coopculture.it/index.php?option=com_snapp&view='
                    'event&id=3793660E-5E3F-9172-2F89-016CB3FAD609&catalogid=B79'
                    'E95CA-090E-FDA8-2364-017448FF0FA0&lang=it',
                observer_date=date,
                observer_time=time,
                count_tickets=count_tickets,
                max_tickets=max_tickets,
                informer=self.__informer,
            )
            self.__observer.start()
            self.__set_active_start_monitor_btn(True)

    def __set_active_start_monitor_btn(self, active: bool) -> None:
        """
        Метод блокировки кнопки старта мониторинга.

        :param active:
            Статус кнопки старта мониторинга.
            True - кнопка активна. False - кнопка неактивна.
        """

        if not active:
            self.ui.start_monitoring.setText('Запуск...')
            self.ui.start_monitoring.setDisabled(True)
        else:
            self.ui.start_monitoring.setText('Начать мониторинг')
            self.ui.start_monitoring.setDisabled(False)

    def _stop_observer_slot(self) -> None:
        """Остановка наблюдателя за билетами"""

        if self.__observer.worked:
            self.__set_active_stop_monitor_btn(False)
            self.__observer.stop()
            self.__set_active_stop_monitor_btn(True)

    def __set_active_stop_monitor_btn(self, active: bool) -> None:
        """
        Метод блокировки кнопки остановки мониторинга.

        :param active:
            Статус кнопки остановки мониторинга.
            True - кнопка активна. False - кнопка неактивна.
        """

        if not active:
            self.ui.stop_monitoring.setText('Остановка...')
            self.ui.stop_monitoring.setDisabled(True)
        else:
            self.ui.stop_monitoring.setText('Стоп')
            self.ui.stop_monitoring.setDisabled(False)
