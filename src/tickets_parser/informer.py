import logging
import datetime as dt
from enum import (
    Enum,
    auto,
)
from PyQt5 import QtWidgets


class Informer:
    """
    Класс информатора.

    Обеспечивает информацию о состоянии бота в целом.
    """

    class MessageLevel(Enum):
        INFO = auto()
        ERROR = auto()

    def __init__(self, file_name: str, ui_view: QtWidgets.QTextEdit) -> None:
        """
        Инициализатор класса.

        :param file_name: Имя файла для логирования.
        :param ui_view: Элемент интерфейса для вывода сообщений пользователю.
        """

        # Настройка логгера.
        self.__file_name = file_name
        self.__logger = logging.getLogger('main_logger')
        self.__logger.setLevel(logging.INFO)
        self.__logger.addHandler(self._create_logger_handler())

        # Настройка объекта UI для вывода информации пользователю.
        self.__ui_view = ui_view

    def _create_logger_handler(self) -> logging.FileHandler:
        """
        Создание и настройка обработчика файла логирования.

        :return: Настроенный обработчик для файла логирования.
        """

        file_handler = logging.FileHandler(self.__file_name)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)

        return file_handler

    def push_message(self, msg: str, level: MessageLevel) -> None:
        """
        Логирование сообщения и вывод его пользователю.

        :param msg: Текст сообщения.
        :param level: Уровень сообщения.
        """

        if level == self.MessageLevel.INFO:
            self.__logger.info(msg)
            msg_for_ui = f'{dt.datetime.now()} - INFO - {msg}'
            self.__ui_view.append(msg_for_ui)
        elif level == self.MessageLevel.ERROR:
            self.__logger.error(msg)
            msg_for_ui = f'{dt.datetime.now()} - ERROR - {msg}'
            self.__ui_view.append(msg_for_ui)
