# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'simple.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.led_input = QLineEdit(self.centralwidget)
        self.led_input.setObjectName(u"led_input")
        self.led_input.setGeometry(QRect(180, 200, 113, 21))
        self.lbl_output = QLabel(self.centralwidget)
        self.lbl_output.setObjectName(u"lbl_output")
        self.lbl_output.setGeometry(QRect(180, 240, 111, 16))
        self.btn_process = QPushButton(self.centralwidget)
        self.btn_process.setObjectName(u"btn_process")
        self.btn_process.setGeometry(QRect(200, 280, 75, 24))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.lbl_output.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.btn_process.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
    # retranslateUi

