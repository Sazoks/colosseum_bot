# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.date_input = QtWidgets.QDateEdit(self.centralwidget)
        self.date_input.setObjectName("date_input")
        self.verticalLayout.addWidget(self.date_input)
        self.time_input = QtWidgets.QTimeEdit(self.centralwidget)
        self.time_input.setObjectName("time_input")
        self.verticalLayout.addWidget(self.time_input)
        self.tickets_input = QtWidgets.QSpinBox(self.centralwidget)
        self.tickets_input.setObjectName("tickets_input")
        self.verticalLayout.addWidget(self.tickets_input)
        self.max_tickets = QtWidgets.QCheckBox(self.centralwidget)
        self.max_tickets.setObjectName("max_tickets")
        self.verticalLayout.addWidget(self.max_tickets)
        self.start_monitoring = QtWidgets.QPushButton(self.centralwidget)
        self.start_monitoring.setObjectName("start_monitoring")
        self.verticalLayout.addWidget(self.start_monitoring)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 6)
        self.gridLayout.setColumnStretch(2, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.max_tickets.setText(_translate("MainWindow", "Максимум билетов"))
        self.start_monitoring.setText(_translate("MainWindow", "Начать мониторинг"))
