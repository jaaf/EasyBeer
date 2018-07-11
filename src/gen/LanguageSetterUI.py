# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'languagesetter.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(874, 453)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(50, 330, 771, 20))
        self.label.setObjectName("label")
        self.combo = QtWidgets.QComboBox(Dialog)
        self.combo.setGeometry(QtCore.QRect(140, 50, 511, 81))
        self.combo.setIconSize(QtCore.QSize(32, 32))
        self.combo.setObjectName("combo")
        self.button = QtWidgets.QPushButton(Dialog)
        self.button.setGeometry(QtCore.QRect(430, 260, 341, 36))
        self.button.setObjectName("button")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "<div>Icons made by <a href=\"http://www.freepik.com\" title=\"Freepik\">Freepik</a> from <a href=\"https://www.flaticon.com/\" title=\"Flaticon\">www.flaticon.com</a> is licensed by <a href=\"http://creativecommons.org/licenses/by/3.0/\" title=\"Creative Commons BY 3.0\" target=\"_blank\">CC 3.0 BY</a></div>"))
        self.button.setText(_translate("Dialog", "OK"))

