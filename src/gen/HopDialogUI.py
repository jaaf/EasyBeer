# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/hopdialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(971, 364)
        self.list_label = QtWidgets.QLabel(Form)
        self.list_label.setGeometry(QtCore.QRect(20, 20, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.list_label.setFont(font)
        self.list_label.setObjectName("list_label")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 60, 431, 261))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.hop_list_widget = QtWidgets.QListWidget(self.layoutWidget)
        self.hop_list_widget.setObjectName("hop_list_widget")
        self.verticalLayout.addWidget(self.hop_list_widget)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.edit_button = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.edit_button.setFont(font)
        self.edit_button.setObjectName("edit_button")
        self.horizontalLayout.addWidget(self.edit_button)
        self.delete_button = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.delete_button.setFont(font)
        self.delete_button.setObjectName("delete_button")
        self.horizontalLayout.addWidget(self.delete_button)
        self.new_button = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.new_button.setFont(font)
        self.new_button.setObjectName("new_button")
        self.horizontalLayout.addWidget(self.new_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.detail_label = QtWidgets.QLabel(Form)
        self.detail_label.setGeometry(QtCore.QRect(530, 20, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.detail_label.setFont(font)
        self.detail_label.setObjectName("detail_label")
        self.close_button = QtWidgets.QPushButton(Form)
        self.close_button.setGeometry(QtCore.QRect(810, 310, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.close_button.setFont(font)
        self.close_button.setObjectName("close_button")
        self.add_button = QtWidgets.QPushButton(Form)
        self.add_button.setGeometry(QtCore.QRect(540, 240, 181, 32))
        self.add_button.setMaximumSize(QtCore.QSize(250, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.add_button.setFont(font)
        self.add_button.setObjectName("add_button")
        self.layoutWidget1 = QtWidgets.QWidget(Form)
        self.layoutWidget1.setGeometry(QtCore.QRect(530, 60, 411, 161))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.name_label = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name_label.sizePolicy().hasHeightForWidth())
        self.name_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.name_label.setFont(font)
        self.name_label.setObjectName("name_label")
        self.gridLayout.addWidget(self.name_label, 0, 0, 1, 1)
        self.name_edit = QtWidgets.QLineEdit(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name_edit.sizePolicy().hasHeightForWidth())
        self.name_edit.setSizePolicy(sizePolicy)
        self.name_edit.setMinimumSize(QtCore.QSize(0, 0))
        self.name_edit.setObjectName("name_edit")
        self.gridLayout.addWidget(self.name_edit, 0, 1, 1, 3)
        self.alpha_acid_label = QtWidgets.QLabel(self.layoutWidget1)
        self.alpha_acid_label.setMinimumSize(QtCore.QSize(220, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.alpha_acid_label.setFont(font)
        self.alpha_acid_label.setObjectName("alpha_acid_label")
        self.gridLayout.addWidget(self.alpha_acid_label, 1, 0, 1, 2)
        self.alpha_acid_edit = QtWidgets.QLineEdit(self.layoutWidget1)
        self.alpha_acid_edit.setMinimumSize(QtCore.QSize(100, 0))
        self.alpha_acid_edit.setMaximumSize(QtCore.QSize(50, 16777215))
        self.alpha_acid_edit.setObjectName("alpha_acid_edit")
        self.gridLayout.addWidget(self.alpha_acid_edit, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_3.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 3, 1, 1)
        self.form_label = QtWidgets.QLabel(self.layoutWidget1)
        self.form_label.setMinimumSize(QtCore.QSize(220, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.form_label.setFont(font)
        self.form_label.setObjectName("form_label")
        self.gridLayout.addWidget(self.form_label, 2, 0, 1, 2)
        self.form_list = QtWidgets.QComboBox(self.layoutWidget1)
        self.form_list.setObjectName("form_list")
        self.gridLayout.addWidget(self.form_list, 2, 2, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.list_label.setText(_translate("Form", "Hop List"))
        self.edit_button.setText(_translate("Form", "Edit"))
        self.delete_button.setText(_translate("Form", "Delete"))
        self.new_button.setText(_translate("Form", "New"))
        self.detail_label.setText(_translate("Form", "Selected Hop Details"))
        self.close_button.setText(_translate("Form", "Close"))
        self.add_button.setText(_translate("Form", "Add"))
        self.name_label.setText(_translate("Form", "Name"))
        self.alpha_acid_label.setText(_translate("Form", "Alpha Acid"))
        self.label_3.setText(_translate("Form", "%"))
        self.form_label.setText(_translate("Form", "Form"))

