# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'maltdialog.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MaltDialog(object):
    def setupUi(self, MaltDialog):
        MaltDialog.setObjectName("MaltDialog")
        MaltDialog.resize(833, 416)
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        MaltDialog.setFont(font)
        MaltDialog.setWindowTitle("")
        self.close_button = QtWidgets.QPushButton(MaltDialog)
        self.close_button.setGeometry(QtCore.QRect(10, 370, 141, 31))
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.close_button.setFont(font)
        self.close_button.setObjectName("close_button")
        self.layoutWidget = QtWidgets.QWidget(MaltDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 92, 341, 271))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.edit_button = QtWidgets.QPushButton(self.layoutWidget)
        self.edit_button.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.edit_button.setFont(font)
        self.edit_button.setObjectName("edit_button")
        self.horizontalLayout.addWidget(self.edit_button)
        self.delete_button = QtWidgets.QPushButton(self.layoutWidget)
        self.delete_button.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.delete_button.setFont(font)
        self.delete_button.setObjectName("delete_button")
        self.horizontalLayout.addWidget(self.delete_button)
        self.new_button = QtWidgets.QPushButton(self.layoutWidget)
        self.new_button.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.new_button.setFont(font)
        self.new_button.setObjectName("new_button")
        self.horizontalLayout.addWidget(self.new_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.malt_list_label = QtWidgets.QLabel(MaltDialog)
        self.malt_list_label.setGeometry(QtCore.QRect(20, 0, 271, 41))
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.malt_list_label.setFont(font)
        self.malt_list_label.setObjectName("malt_list_label")
        self.malt_list_widget = QtWidgets.QListWidget(MaltDialog)
        self.malt_list_widget.setGeometry(QtCore.QRect(10, 40, 341, 261))
        self.malt_list_widget.setObjectName("malt_list_widget")
        self.layoutWidget1 = QtWidgets.QWidget(MaltDialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(370, 20, 454, 345))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.detail_label = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.detail_label.setFont(font)
        self.detail_label.setObjectName("detail_label")
        self.verticalLayout_6.addWidget(self.detail_label)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.name_label = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.name_label.setFont(font)
        self.name_label.setObjectName("name_label")
        self.verticalLayout_2.addWidget(self.name_label)
        self.name_edit = QtWidgets.QLineEdit(self.layoutWidget1)
        self.name_edit.setMinimumSize(QtCore.QSize(450, 0))
        self.name_edit.setObjectName("name_edit")
        self.verticalLayout_2.addWidget(self.name_edit)
        self.verticalLayout_6.addLayout(self.verticalLayout_2)
        self.maker_label = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.maker_label.setFont(font)
        self.maker_label.setObjectName("maker_label")
        self.verticalLayout_6.addWidget(self.maker_label)
        self.maker_edit = QtWidgets.QLineEdit(self.layoutWidget1)
        self.maker_edit.setObjectName("maker_edit")
        self.verticalLayout_6.addWidget(self.maker_edit)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_6.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.max_yield_label = QtWidgets.QLabel(self.layoutWidget1)
        self.max_yield_label.setMinimumSize(QtCore.QSize(220, 0))
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.max_yield_label.setFont(font)
        self.max_yield_label.setObjectName("max_yield_label")
        self.horizontalLayout_2.addWidget(self.max_yield_label)
        self.max_yield_edit = QtWidgets.QLineEdit(self.layoutWidget1)
        self.max_yield_edit.setMinimumSize(QtCore.QSize(60, 0))
        self.max_yield_edit.setMaximumSize(QtCore.QSize(70, 16777215))
        self.max_yield_edit.setObjectName("max_yield_edit")
        self.horizontalLayout_2.addWidget(self.max_yield_edit)
        self.max_yield_unti_label = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.max_yield_unti_label.setFont(font)
        self.max_yield_unti_label.setObjectName("max_yield_unti_label")
        self.horizontalLayout_2.addWidget(self.max_yield_unti_label)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.color_label = QtWidgets.QLabel(self.layoutWidget1)
        self.color_label.setMinimumSize(QtCore.QSize(220, 0))
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.color_label.setFont(font)
        self.color_label.setObjectName("color_label")
        self.horizontalLayout_3.addWidget(self.color_label)
        self.color_edit = QtWidgets.QLineEdit(self.layoutWidget1)
        self.color_edit.setMinimumSize(QtCore.QSize(60, 0))
        self.color_edit.setMaximumSize(QtCore.QSize(70, 16777215))
        self.color_edit.setObjectName("color_edit")
        self.horizontalLayout_3.addWidget(self.color_edit)
        self.color_unit_label = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.color_unit_label.setFont(font)
        self.color_unit_label.setObjectName("color_unit_label")
        self.horizontalLayout_3.addWidget(self.color_unit_label)
        self.verticalLayout_6.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.kolbach_index_label = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.kolbach_index_label.setFont(font)
        self.kolbach_index_label.setObjectName("kolbach_index_label")
        self.horizontalLayout_4.addWidget(self.kolbach_index_label)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.kolbach_min_label = QtWidgets.QLabel(self.layoutWidget1)
        self.kolbach_min_label.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.kolbach_min_label.setFont(font)
        self.kolbach_min_label.setAlignment(QtCore.Qt.AlignCenter)
        self.kolbach_min_label.setObjectName("kolbach_min_label")
        self.verticalLayout_4.addWidget(self.kolbach_min_label)
        self.kolbach_min = QtWidgets.QLineEdit(self.layoutWidget1)
        self.kolbach_min.setMaximumSize(QtCore.QSize(70, 50))
        self.kolbach_min.setObjectName("kolbach_min")
        self.verticalLayout_4.addWidget(self.kolbach_min)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.kolbach_max_label = QtWidgets.QLabel(self.layoutWidget1)
        self.kolbach_max_label.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.kolbach_max_label.setFont(font)
        self.kolbach_max_label.setAlignment(QtCore.Qt.AlignCenter)
        self.kolbach_max_label.setObjectName("kolbach_max_label")
        self.verticalLayout_5.addWidget(self.kolbach_max_label)
        self.kolbach_max = QtWidgets.QLineEdit(self.layoutWidget1)
        self.kolbach_max.setMaximumSize(QtCore.QSize(70, 50))
        self.kolbach_max.setObjectName("kolbach_max")
        self.verticalLayout_5.addWidget(self.kolbach_max)
        self.horizontalLayout_4.addLayout(self.verticalLayout_5)
        spacerItem1 = QtWidgets.QSpacerItem(98, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem2)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.cancel_button = QtWidgets.QPushButton(self.layoutWidget1)
        self.cancel_button.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.cancel_button.setFont(font)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout_6.addWidget(self.cancel_button)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.update_button = QtWidgets.QPushButton(self.layoutWidget1)
        self.update_button.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.update_button.setFont(font)
        self.update_button.setObjectName("update_button")
        self.horizontalLayout_6.addWidget(self.update_button)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.add_button = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_button.sizePolicy().hasHeightForWidth())
        self.add_button.setSizePolicy(sizePolicy)
        self.add_button.setMinimumSize(QtCore.QSize(100, 0))
        self.add_button.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setBold(True)
        font.setWeight(75)
        self.add_button.setFont(font)
        self.add_button.setObjectName("add_button")
        self.horizontalLayout_6.addWidget(self.add_button)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_6.addLayout(self.horizontalLayout_5)
        self.layoutWidget.raise_()
        self.layoutWidget.raise_()
        self.close_button.raise_()
        self.malt_list_label.raise_()
        self.malt_list_widget.raise_()

        self.retranslateUi(MaltDialog)
        QtCore.QMetaObject.connectSlotsByName(MaltDialog)

    def retranslateUi(self, MaltDialog):
        _translate = QtCore.QCoreApplication.translate
        self.close_button.setText(_translate("MaltDialog", "Close"))
        self.edit_button.setText(_translate("MaltDialog", "Edit"))
        self.delete_button.setText(_translate("MaltDialog", "Delete"))
        self.new_button.setText(_translate("MaltDialog", "New"))
        self.malt_list_label.setText(_translate("MaltDialog", "Malt List"))
        self.detail_label.setText(_translate("MaltDialog", "Selected Malt Details"))
        self.name_label.setText(_translate("MaltDialog", "Name"))
        self.maker_label.setText(_translate("MaltDialog", "Maker"))
        self.max_yield_label.setText(_translate("MaltDialog", "Maximum Yield (FGDB) "))
        self.max_yield_unti_label.setText(_translate("MaltDialog", "%"))
        self.color_label.setText(_translate("MaltDialog", "Color"))
        self.color_unit_label.setText(_translate("MaltDialog", "EBC"))
        self.kolbach_index_label.setText(_translate("MaltDialog", "Kolbach Index"))
        self.kolbach_min_label.setText(_translate("MaltDialog", "Min"))
        self.kolbach_max_label.setText(_translate("MaltDialog", "Max"))
        self.cancel_button.setText(_translate("MaltDialog", "Cancel"))
        self.update_button.setText(_translate("MaltDialog", "Update"))
        self.add_button.setText(_translate("MaltDialog", "Add "))

