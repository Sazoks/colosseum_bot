import sys
from PyQt5 import QtWidgets

from main_window import MainWindow


def main():
    app = QtWidgets.QApplication([])
    _main_window = MainWindow()
    _main_window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
