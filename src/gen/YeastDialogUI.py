# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/yeastdialog.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(998, 599)
        Form.setWindowTitle("")
        self.close_button = QtWidgets.QPushButton(Form)
        self.close_button.setGeometry(QtCore.QRect(830, 530, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.close_button.setFont(font)
        self.close_button.setObjectName("close_button")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(520, 11, 620, 540))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.detail_label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.detail_label.setFont(font)
        self.detail_label.setObjectName("detail_label")
        self.verticalLayout_4.addWidget(self.detail_label)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.name_label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.name_label.setFont(font)
        self.name_label.setObjectName("name_label")
        self.verticalLayout_2.addWidget(self.name_label)
        self.name_edit = QtWidgets.QLineEdit(self.layoutWidget)
        self.name_edit.setMinimumSize(QtCore.QSize(450, 0))
        self.name_edit.setObjectName("name_edit")
        self.verticalLayout_2.addWidget(self.name_edit)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.maker_label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.maker_label.setFont(font)
        self.maker_label.setObjectName("maker_label")
        self.verticalLayout_4.addWidget(self.maker_label)
        self.maker_edit = QtWidgets.QLineEdit(self.layoutWidget)
        self.maker_edit.setObjectName("maker_edit")
        self.verticalLayout_4.addWidget(self.maker_edit)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.max_allowed_temperature_label = QtWidgets.QLabel(self.layoutWidget)
        self.max_allowed_temperature_label.setMinimumSize(QtCore.QSize(220, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.max_allowed_temperature_label.setFont(font)
        self.max_allowed_temperature_label.setObjectName("max_allowed_temperature_label")
        self.horizontalLayout_2.addWidget(self.max_allowed_temperature_label)
        self.max_allowed_temperature_edit = QtWidgets.QLineEdit(self.layoutWidget)
        self.max_allowed_temperature_edit.setMinimumSize(QtCore.QSize(50, 0))
        self.max_allowed_temperature_edit.setMaximumSize(QtCore.QSize(50, 16777215))
        self.max_allowed_temperature_edit.setObjectName("max_allowed_temperature_edit")
        self.horizontalLayout_2.addWidget(self.max_allowed_temperature_edit)
        self.max_allowed_temperature_unit_label = QtWidgets.QLabel(self.layoutWidget)
        self.max_allowed_temperature_unit_label.setObjectName("max_allowed_temperature_unit_label")
        self.horizontalLayout_2.addWidget(self.max_allowed_temperature_unit_label)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.max_advised_temperature_label = QtWidgets.QLabel(self.layoutWidget)
        self.max_advised_temperature_label.setMinimumSize(QtCore.QSize(220, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.max_advised_temperature_label.setFont(font)
        self.max_advised_temperature_label.setObjectName("max_advised_temperature_label")
        self.horizontalLayout_3.addWidget(self.max_advised_temperature_label)
        self.max_advised_temperature_edit = QtWidgets.QLineEdit(self.layoutWidget)
        self.max_advised_temperature_edit.setMinimumSize(QtCore.QSize(50, 0))
        self.max_advised_temperature_edit.setMaximumSize(QtCore.QSize(50, 16777215))
        self.max_advised_temperature_edit.setObjectName("max_advised_temperature_edit")
        self.horizontalLayout_3.addWidget(self.max_advised_temperature_edit)
        self.max_advised_temperature_unit_label = QtWidgets.QLabel(self.layoutWidget)
        self.max_advised_temperature_unit_label.setObjectName("max_advised_temperature_unit_label")
        self.horizontalLayout_3.addWidget(self.max_advised_temperature_unit_label)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.min_advised_temperature_label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.min_advised_temperature_label.setFont(font)
        self.min_advised_temperature_label.setObjectName("min_advised_temperature_label")
        self.horizontalLayout_4.addWidget(self.min_advised_temperature_label)
        self.min_advised_temperature_edit = QtWidgets.QLineEdit(self.layoutWidget)
        self.min_advised_temperature_edit.setMinimumSize(QtCore.QSize(50, 0))
        self.min_advised_temperature_edit.setMaximumSize(QtCore.QSize(50, 16777215))
        self.min_advised_temperature_edit.setObjectName("min_advised_temperature_edit")
        self.horizontalLayout_4.addWidget(self.min_advised_temperature_edit)
        self.min_advised_temperature_unit_label = QtWidgets.QLabel(self.layoutWidget)
        self.min_advised_temperature_unit_label.setObjectName("min_advised_temperature_unit_label")
        self.horizontalLayout_4.addWidget(self.min_advised_temperature_unit_label)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.min_allowed_temperature_label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.min_allowed_temperature_label.setFont(font)
        self.min_allowed_temperature_label.setObjectName("min_allowed_temperature_label")
        self.horizontalLayout_5.addWidget(self.min_allowed_temperature_label)
        self.min_allowed_temperature_edit = QtWidgets.QLineEdit(self.layoutWidget)
        self.min_allowed_temperature_edit.setMinimumSize(QtCore.QSize(50, 0))
        self.min_allowed_temperature_edit.setMaximumSize(QtCore.QSize(50, 16777215))
        self.min_allowed_temperature_edit.setObjectName("min_allowed_temperature_edit")
        self.horizontalLayout_5.addWidget(self.min_allowed_temperature_edit)
        self.min_allowed_temperature_unit_label = QtWidgets.QLabel(self.layoutWidget)
        self.min_allowed_temperature_unit_label.setObjectName("min_allowed_temperature_unit_label")
        self.horizontalLayout_5.addWidget(self.min_allowed_temperature_unit_label)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.form_label = QtWidgets.QLabel(self.layoutWidget)
        self.form_label.setMinimumSize(QtCore.QSize(200, 0))
        self.form_label.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.form_label.setFont(font)
        self.form_label.setObjectName("form_label")
        self.horizontalLayout_8.addWidget(self.form_label)
        self.form_combo = QtWidgets.QComboBox(self.layoutWidget)
        self.form_combo.setMinimumSize(QtCore.QSize(100, 0))
        self.form_combo.setMaximumSize(QtCore.QSize(100, 16777215))
        self.form_combo.setObjectName("form_combo")
        self.horizontalLayout_8.addWidget(self.form_combo)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.attenuation_label = QtWidgets.QLabel(self.layoutWidget)
        self.attenuation_label.setMinimumSize(QtCore.QSize(200, 0))
        self.attenuation_label.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.attenuation_label.setFont(font)
        self.attenuation_label.setObjectName("attenuation_label")
        self.horizontalLayout_6.addWidget(self.attenuation_label)
        self.attenuation_combo = QtWidgets.QComboBox(self.layoutWidget)
        self.attenuation_combo.setMinimumSize(QtCore.QSize(100, 0))
        self.attenuation_combo.setMaximumSize(QtCore.QSize(100, 16777215))
        self.attenuation_combo.setObjectName("attenuation_combo")
        self.horizontalLayout_6.addWidget(self.attenuation_combo)
        self.attenuation_help_button = QtWidgets.QPushButton(self.layoutWidget)
        self.attenuation_help_button.setMaximumSize(QtCore.QSize(25, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.attenuation_help_button.setFont(font)
        self.attenuation_help_button.setObjectName("attenuation_help_button")
        self.horizontalLayout_6.addWidget(self.attenuation_help_button)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.floculation_label = QtWidgets.QLabel(self.layoutWidget)
        self.floculation_label.setMinimumSize(QtCore.QSize(200, 0))
        self.floculation_label.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.floculation_label.setFont(font)
        self.floculation_label.setObjectName("floculation_label")
        self.horizontalLayout_7.addWidget(self.floculation_label)
        self.floculation_combo = QtWidgets.QComboBox(self.layoutWidget)
        self.floculation_combo.setMinimumSize(QtCore.QSize(100, 0))
        self.floculation_combo.setMaximumSize(QtCore.QSize(100, 16777215))
        self.floculation_combo.setObjectName("floculation_combo")
        self.horizontalLayout_7.addWidget(self.floculation_combo)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem3)
        self.add_button = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_button.sizePolicy().hasHeightForWidth())
        self.add_button.setSizePolicy(sizePolicy)
        self.add_button.setMinimumSize(QtCore.QSize(300, 0))
        self.add_button.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.add_button.setFont(font)
        self.add_button.setObjectName("add_button")
        self.verticalLayout_4.addWidget(self.add_button)
        self.layoutWidget1 = QtWidgets.QWidget(Form)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 10, 481, 491))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.yeast_list_label = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.yeast_list_label.setFont(font)
        self.yeast_list_label.setObjectName("yeast_list_label")
        self.verticalLayout.addWidget(self.yeast_list_label)
        self.yeast_list_widget = QtWidgets.QListWidget(self.layoutWidget1)
        self.yeast_list_widget.setMinimumSize(QtCore.QSize(0, 400))
        self.yeast_list_widget.setObjectName("yeast_list_widget")
        self.verticalLayout.addWidget(self.yeast_list_widget)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.edit_button = QtWidgets.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.edit_button.setFont(font)
        self.edit_button.setObjectName("edit_button")
        self.horizontalLayout.addWidget(self.edit_button)
        self.delete_button = QtWidgets.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.delete_button.setFont(font)
        self.delete_button.setObjectName("delete_button")
        self.horizontalLayout.addWidget(self.delete_button)
        self.new_button = QtWidgets.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.new_button.setFont(font)
        self.new_button.setObjectName("new_button")
        self.horizontalLayout.addWidget(self.new_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.layoutWidget.raise_()
        self.layoutWidget.raise_()
        self.close_button.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.close_button.setText(_translate("Form", "Close"))
        self.detail_label.setText(_translate("Form", "Selected Yeast Details"))
        self.name_label.setText(_translate("Form", "Name"))
        self.maker_label.setText(_translate("Form", "Maker"))
        self.max_allowed_temperature_label.setText(_translate("Form", "Maximum allowed temperature"))
        self.max_allowed_temperature_unit_label.setText(_translate("Form", "°C"))
        self.max_advised_temperature_label.setText(_translate("Form", "Maximum advised temperature"))
        self.max_advised_temperature_unit_label.setText(_translate("Form", "°C"))
        self.min_advised_temperature_label.setText(_translate("Form", "Minimum Advised Temperature"))
        self.min_advised_temperature_unit_label.setText(_translate("Form", "°C"))
        self.min_allowed_temperature_label.setText(_translate("Form", "Minimun Allowed Temperature"))
        self.min_allowed_temperature_unit_label.setText(_translate("Form", "°C"))
        self.form_label.setText(_translate("Form", "Form"))
        self.attenuation_label.setText(_translate("Form", "Attenuation"))
        self.attenuation_help_button.setText(_translate("Form", "?"))
        self.floculation_label.setText(_translate("Form", "Floculation"))
        self.add_button.setText(_translate("Form", "Add "))
        self.yeast_list_label.setText(_translate("Form", "Yeast list"))
        self.edit_button.setText(_translate("Form", "Edit"))
        self.delete_button.setText(_translate("Form", "Delete"))
        self.new_button.setText(_translate("Form", "New"))

