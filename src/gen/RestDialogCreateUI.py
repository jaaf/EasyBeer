# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'restdialogcreate.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(996, 612)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.main_label = QtWidgets.QLabel(Form)
        self.main_label.setMinimumSize(QtCore.QSize(600, 0))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.main_label.setFont(font)
        self.main_label.setMidLineWidth(0)
        self.main_label.setObjectName("main_label")
        self.verticalLayout.addWidget(self.main_label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.name_label = QtWidgets.QLabel(Form)
        self.name_label.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.name_label.setFont(font)
        self.name_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.name_label.setObjectName("name_label")
        self.gridLayout.addWidget(self.name_label, 1, 0, 1, 1)
        self.ph_layout = QtWidgets.QHBoxLayout()
        self.ph_layout.setObjectName("ph_layout")
        self.ph_min = QtWidgets.QLineEdit(Form)
        self.ph_min.setMinimumSize(QtCore.QSize(50, 0))
        self.ph_min.setMaximumSize(QtCore.QSize(100, 16777215))
        self.ph_min.setObjectName("ph_min")
        self.ph_layout.addWidget(self.ph_min)
        self.optimal_ph_min = QtWidgets.QLineEdit(Form)
        self.optimal_ph_min.setMinimumSize(QtCore.QSize(50, 0))
        self.optimal_ph_min.setMaximumSize(QtCore.QSize(100, 16777215))
        self.optimal_ph_min.setObjectName("optimal_ph_min")
        self.ph_layout.addWidget(self.optimal_ph_min)
        self.optimal_ph_max = QtWidgets.QLineEdit(Form)
        self.optimal_ph_max.setMinimumSize(QtCore.QSize(50, 0))
        self.optimal_ph_max.setMaximumSize(QtCore.QSize(100, 16777215))
        self.optimal_ph_max.setObjectName("optimal_ph_max")
        self.ph_layout.addWidget(self.optimal_ph_max)
        self.ph_max = QtWidgets.QLineEdit(Form)
        self.ph_max.setMinimumSize(QtCore.QSize(50, 0))
        self.ph_max.setMaximumSize(QtCore.QSize(100, 16777215))
        self.ph_max.setObjectName("ph_max")
        self.ph_layout.addWidget(self.ph_max)
        self.gridLayout.addLayout(self.ph_layout, 2, 2, 1, 1)
        self.choose_label = QtWidgets.QLabel(Form)
        self.choose_label.setMinimumSize(QtCore.QSize(400, 0))
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(14)
        font.setItalic(True)
        self.choose_label.setFont(font)
        self.choose_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.choose_label.setObjectName("choose_label")
        self.gridLayout.addWidget(self.choose_label, 0, 0, 1, 1)
        self.name_combo = QtWidgets.QComboBox(Form)
        self.name_combo.setMinimumSize(QtCore.QSize(500, 0))
        self.name_combo.setObjectName("name_combo")
        self.gridLayout.addWidget(self.name_combo, 0, 2, 1, 1)
        self.temperature_label = QtWidgets.QLabel(Form)
        self.temperature_label.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.temperature_label.setFont(font)
        self.temperature_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.temperature_label.setObjectName("temperature_label")
        self.gridLayout.addWidget(self.temperature_label, 3, 0, 1, 1)
        self.temperature_layout = QtWidgets.QHBoxLayout()
        self.temperature_layout.setObjectName("temperature_layout")
        self.temperature_min = QtWidgets.QLineEdit(Form)
        self.temperature_min.setMinimumSize(QtCore.QSize(50, 0))
        self.temperature_min.setMaximumSize(QtCore.QSize(100, 16777215))
        self.temperature_min.setObjectName("temperature_min")
        self.temperature_layout.addWidget(self.temperature_min)
        self.optimal_temperature_min = QtWidgets.QLineEdit(Form)
        self.optimal_temperature_min.setMinimumSize(QtCore.QSize(50, 0))
        self.optimal_temperature_min.setMaximumSize(QtCore.QSize(100, 16777215))
        self.optimal_temperature_min.setObjectName("optimal_temperature_min")
        self.temperature_layout.addWidget(self.optimal_temperature_min)
        self.optimal_temperature_max = QtWidgets.QLineEdit(Form)
        self.optimal_temperature_max.setMinimumSize(QtCore.QSize(50, 0))
        self.optimal_temperature_max.setMaximumSize(QtCore.QSize(100, 16777215))
        self.optimal_temperature_max.setObjectName("optimal_temperature_max")
        self.temperature_layout.addWidget(self.optimal_temperature_max)
        self.temperature_max = QtWidgets.QLineEdit(Form)
        self.temperature_max.setMinimumSize(QtCore.QSize(50, 0))
        self.temperature_max.setMaximumSize(QtCore.QSize(100, 16777215))
        self.temperature_max.setObjectName("temperature_max")
        self.temperature_layout.addWidget(self.temperature_max)
        self.gridLayout.addLayout(self.temperature_layout, 3, 2, 1, 1)
        self.ph_range_label = QtWidgets.QLabel(Form)
        self.ph_range_label.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.ph_range_label.setFont(font)
        self.ph_range_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ph_range_label.setObjectName("ph_range_label")
        self.gridLayout.addWidget(self.ph_range_label, 2, 0, 1, 1)
        self.name_edit = QtWidgets.QLineEdit(Form)
        self.name_edit.setObjectName("name_edit")
        self.gridLayout.addWidget(self.name_edit, 1, 2, 1, 1)
        self.temp_unit_label = QtWidgets.QLabel(Form)
        self.temp_unit_label.setText("")
        self.temp_unit_label.setObjectName("temp_unit_label")
        self.gridLayout.addWidget(self.temp_unit_label, 3, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.usage_guidance_edit = QtWidgets.QTextEdit(Form)
        self.usage_guidance_edit.setMaximumSize(QtCore.QSize(16777215, 500))
        self.usage_guidance_edit.setObjectName("usage_guidance_edit")
        self.verticalLayout.addWidget(self.usage_guidance_edit)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.edit_button = QtWidgets.QPushButton(Form)
        self.edit_button.setMaximumSize(QtCore.QSize(130, 16777215))
        self.edit_button.setObjectName("edit_button")
        self.horizontalLayout_3.addWidget(self.edit_button)
        self.delete_button = QtWidgets.QPushButton(Form)
        self.delete_button.setMaximumSize(QtCore.QSize(130, 16777215))
        self.delete_button.setObjectName("delete_button")
        self.horizontalLayout_3.addWidget(self.delete_button)
        self.new_button = QtWidgets.QPushButton(Form)
        self.new_button.setMaximumSize(QtCore.QSize(130, 16777215))
        self.new_button.setObjectName("new_button")
        self.horizontalLayout_3.addWidget(self.new_button)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cancel_button = QtWidgets.QPushButton(Form)
        self.cancel_button.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.cancel_button.setFont(font)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        self.update_button = QtWidgets.QPushButton(Form)
        self.update_button.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.update_button.setFont(font)
        self.update_button.setObjectName("update_button")
        self.horizontalLayout.addWidget(self.update_button)
        self.add_button = QtWidgets.QPushButton(Form)
        self.add_button.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.add_button.setFont(font)
        self.add_button.setObjectName("add_button")
        self.horizontalLayout.addWidget(self.add_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.main_label.setText(_translate("Form", "Rest Database"))
        self.name_label.setText(_translate("Form", "Name"))
        self.choose_label.setText(_translate("Form", "Choose a rest beside or create a new one"))
        self.temperature_label.setText(_translate("Form", "Temperature Range"))
        self.ph_range_label.setText(_translate("Form", "PH range"))
        self.edit_button.setText(_translate("Form", "Edit"))
        self.delete_button.setText(_translate("Form", "Delete"))
        self.new_button.setText(_translate("Form", "New"))
        self.cancel_button.setText(_translate("Form", "Cancel"))
        self.update_button.setText(_translate("Form", "Update this rest"))
        self.add_button.setText(_translate("Form", "Save this rest"))

