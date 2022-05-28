from PyQt5 import QtWidgets
from typing import Optional

from ui.main_window import Ui_MainWindow
from tickets_parser.observer import DateTimeObserver


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
        self.__observer: Optional[DateTimeObserver] = None

        # Подключаем обработчик сигнала для старта мониторинга.
        self.ui.start_monitoring.clicked.connect(self._init_observer_slot)
        # Подключаем обработчик сигнала для остановки мониторинга.
        self.ui.stop_monitoring.clicked.connect(self._stop_observer_slot)

    def _init_observer_slot(self) -> None:
        self.__observer = DateTimeObserver(
            url='https://ecm.coopculture.it/index.php?option=com_snapp&view='
                'event&id=3793660E-5E3F-9172-2F89-016CB3FAD609&catalogid=B79'
                'E95CA-090E-FDA8-2364-017448FF0FA0&lang=it',
            observer_date=...,
            observer_time=...,
        )  # FIXME: Добавить дату и время.
        self.__observer.start()

    def _stop_observer_slot(self) -> None:
        if self.__observer is not None:
            self.__observer.stop()
