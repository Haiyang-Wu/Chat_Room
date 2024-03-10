# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 600)
        Form.setMinimumSize(QSize(400, 600))
        Form.setMaximumSize(QSize(400, 600))
        icon = QIcon()
        icon.addFile(u"../imgs/logo.png", QSize(), QIcon.Normal, QIcon.Off)
        Form.setWindowIcon(icon)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.stackedWidget = QStackedWidget(Form)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.horizontalLayout_5 = QHBoxLayout(self.page)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(30)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(100, 100))
        self.label.setMaximumSize(QSize(100, 100))
        self.label.setStyleSheet(u"border-radius: 50px;\n"
"background-color: rgb(255, 255, 255);\n"
"image: url(imgs/logo.png);\n"
"padding: 10px;\n"
"")

        self.horizontalLayout_4.addWidget(self.label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.lineEdit = QLineEdit(self.page)
        self.lineEdit.setObjectName(u"lineEdit")
        font = QFont()
        font.setPointSize(13)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet(u"border-radius: 5px;\n"
"background-color: rgb(255, 255, 255);\n"
"padding: 5px;")
        self.lineEdit.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.lineEdit)

        self.lineEdit_3 = QLineEdit(self.page)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setStyleSheet(u"border-radius: 5px;\n"
"background-color: rgb(255, 255, 255);\n"
"padding: 5px;")
        self.lineEdit_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.lineEdit_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkBox = QCheckBox(self.page)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout_2.addWidget(self.checkBox)

        self.pushButton_3 = QPushButton(self.page)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setStyleSheet(u"border: none;\n"
"color: rgb(69, 119, 163);")

        self.horizontalLayout_2.addWidget(self.pushButton_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton = QPushButton(self.page)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 40))
        font1 = QFont()
        font1.setPointSize(20)
        self.pushButton.setFont(font1)
        self.pushButton.setStyleSheet(u"QPushButton{\n"
"    border-radius: 15px;\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(67, 151, 244);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(15, 110, 210);\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color: rgb(10, 89, 178);\n"
"}\n"
"")

        self.horizontalLayout_3.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.page)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(0, 40))
        self.pushButton_2.setFont(font1)
        self.pushButton_2.setStyleSheet(u"QPushButton{\n"
"    border-radius: 15px;\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(224, 224, 224);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(194, 194, 194);\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color: rgb(163, 163, 163);\n"
"}\n"
"")

        self.horizontalLayout_3.addWidget(self.pushButton_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.horizontalLayout_5.addLayout(self.verticalLayout)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.horizontalLayout_7 = QHBoxLayout(self.page_2)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(30)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)

        self.label_3 = QLabel(self.page_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(100, 100))
        self.label_3.setMaximumSize(QSize(100, 100))
        self.label_3.setStyleSheet(u"border-radius: 50px;\n"
"background-color: rgb(255, 255, 255);\n"
"image: url(imgs/logo.png);\n"
"padding: 10px;\n"
"")

        self.horizontalLayout_6.addWidget(self.label_3)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_5)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.lineEdit_4 = QLineEdit(self.page_2)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setStyleSheet(u"border-radius: 5px;\n"
"background-color: rgb(255, 255, 255);\n"
"padding: 5px;")
        self.lineEdit_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.lineEdit_4)

        self.lineEdit_5 = QLineEdit(self.page_2)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setStyleSheet(u"border-radius: 5px;\n"
"background-color: rgb(255, 255, 255);\n"
"padding: 5px;")
        self.lineEdit_5.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.lineEdit_5)

        self.lineEdit_6 = QLineEdit(self.page_2)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setStyleSheet(u"border-radius: 5px;\n"
"background-color: rgb(255, 255, 255);\n"
"padding: 5px;")
        self.lineEdit_6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.lineEdit_6)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.pushButton_6 = QPushButton(self.page_2)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setMinimumSize(QSize(0, 40))
        self.pushButton_6.setFont(font1)
        self.pushButton_6.setStyleSheet(u"QPushButton{\n"
"    border-radius: 15px;\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(224, 224, 224);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(194, 194, 194);\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color: rgb(163, 163, 163);\n"
"}\n"
"")

        self.horizontalLayout_8.addWidget(self.pushButton_6)

        self.pushButton_5 = QPushButton(self.page_2)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setMinimumSize(QSize(0, 40))
        self.pushButton_5.setFont(font1)
        self.pushButton_5.setStyleSheet(u"QPushButton{\n"
"    border-radius: 15px;\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(67, 151, 244);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(15, 110, 210);\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color: rgb(10, 89, 178);\n"
"}\n"
"")

        self.horizontalLayout_8.addWidget(self.pushButton_5)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)


        self.horizontalLayout_7.addLayout(self.verticalLayout_2)

        self.stackedWidget.addWidget(self.page_2)

        self.horizontalLayout.addWidget(self.stackedWidget)


        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"NCL Chatting Room", None))
        self.label.setText("")
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"please enter your account", None))
        self.lineEdit_3.setPlaceholderText(QCoreApplication.translate("Form", u"please enter your password", None))
        self.checkBox.setText(QCoreApplication.translate("Form", u"I have read and agree", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"service contract", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"Log in", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"Register", None))
        self.label_3.setText("")
        self.lineEdit_4.setPlaceholderText(QCoreApplication.translate("Form", u"please enter your account", None))
        self.lineEdit_5.setPlaceholderText(QCoreApplication.translate("Form", u"please enter your password", None))
        self.lineEdit_6.setPlaceholderText(QCoreApplication.translate("Form", u"please verify your password", None))
        self.pushButton_6.setText(QCoreApplication.translate("Form", u"Log in", None))
        self.pushButton_5.setText(QCoreApplication.translate("Form", u"Register", None))
    # retranslateUi

