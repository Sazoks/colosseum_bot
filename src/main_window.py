import datetime as dt
from PyQt5 import QtWidgets

from ui.main_window import Ui_MainWindow
from tickets_parser.observer.datetime_observer import DateTimeObserver


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

        # Наблюдатель за доступными билетами.
        self.__observer = DateTimeObserver()

        # Подключаем обработчик сигнала для старта мониторинга.
        self.ui.start_monitoring.clicked.connect(self._init_observer_slot)
        # Подключаем обработчик сигнала для остановки мониторинга.
        self.ui.stop_monitoring.clicked.connect(self._stop_observer_slot)

    def _init_observer_slot(self) -> None:
        if not self.__observer.worked:
            self.__observer.set_params(
                url='https://ecm.coopculture.it/index.php?option=com_snapp&view='
                    'event&id=3793660E-5E3F-9172-2F89-016CB3FAD609&catalogid=B79'
                    'E95CA-090E-FDA8-2364-017448FF0FA0&lang=it',
                observer_date=dt.date(2022, 5, 31),
                observer_time=dt.time(13, 15, 0),
            )  # FIXME: Добавить дату и время.
            self.__observer.start()

    def _stop_observer_slot(self) -> None:
        if self.__observer.worked:
            self.__observer.stop()
