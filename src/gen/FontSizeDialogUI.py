# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fontsizedialog.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(637, 161)
        self.combo = QtWidgets.QComboBox(Form)
        self.combo.setGeometry(QtCore.QRect(10, 100, 271, 36))
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setItalic(True)
        self.combo.setFont(font)
        self.combo.setObjectName("combo")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 70, 551, 20))
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.close_button = QtWidgets.QPushButton(Form)
        self.close_button.setGeometry(QtCore.QRect(470, 100, 92, 36))
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.close_button.setFont(font)
        self.close_button.setObjectName("close_button")
        self.main_label = QtWidgets.QLabel(Form)
        self.main_label.setGeometry(QtCore.QRect(10, 10, 561, 20))
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.main_label.setFont(font)
        self.main_label.setObjectName("main_label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "chose a size and see the effect in the dialogs instantly"))
        self.close_button.setText(_translate("Form", "Close"))
        self.main_label.setText(_translate("Form", "Font Size Selection"))

