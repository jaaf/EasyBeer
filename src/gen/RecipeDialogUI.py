# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'recipedialog3.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1469, 936)
        Form.setStyleSheet("")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1453, 920))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.recipe_list_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.recipe_list_label.setMaximumSize(QtCore.QSize(16777215, 70))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.recipe_list_label.setFont(font)
        self.recipe_list_label.setObjectName("recipe_list_label")
        self.verticalLayout_2.addWidget(self.recipe_list_label)
        self.recipe_list_widget = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.recipe_list_widget.sizePolicy().hasHeightForWidth())
        self.recipe_list_widget.setSizePolicy(sizePolicy)
        self.recipe_list_widget.setMinimumSize(QtCore.QSize(400, 0))
        self.recipe_list_widget.setMaximumSize(QtCore.QSize(16777215, 150))
        self.recipe_list_widget.setObjectName("recipe_list_widget")
        self.verticalLayout_2.addWidget(self.recipe_list_widget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.recipe_edit_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.recipe_edit_button.setFont(font)
        self.recipe_edit_button.setObjectName("recipe_edit_button")
        self.horizontalLayout.addWidget(self.recipe_edit_button)
        self.recipe_delete_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.recipe_delete_button.setFont(font)
        self.recipe_delete_button.setObjectName("recipe_delete_button")
        self.horizontalLayout.addWidget(self.recipe_delete_button)
        self.recipe_new_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.recipe_new_button.setFont(font)
        self.recipe_new_button.setObjectName("recipe_new_button")
        self.horizontalLayout.addWidget(self.recipe_new_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.recipe_name_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.recipe_name_label.setFont(font)
        self.recipe_name_label.setObjectName("recipe_name_label")
        self.verticalLayout_3.addWidget(self.recipe_name_label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.recipe_name_edit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.recipe_name_edit.setMinimumSize(QtCore.QSize(400, 0))
        self.recipe_name_edit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.recipe_name_edit.setObjectName("recipe_name_edit")
        self.horizontalLayout_2.addWidget(self.recipe_name_edit)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.targets_name_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.targets_name_label.setFont(font)
        self.targets_name_label.setObjectName("targets_name_label")
        self.horizontalLayout_3.addWidget(self.targets_name_label)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.targeted_original_gravity_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.targeted_original_gravity_label.setFont(font)
        self.targeted_original_gravity_label.setObjectName("targeted_original_gravity_label")
        self.horizontalLayout_6.addWidget(self.targeted_original_gravity_label)
        self.targeted_original_gravity_edit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.targeted_original_gravity_edit.setMinimumSize(QtCore.QSize(0, 30))
        self.targeted_original_gravity_edit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.targeted_original_gravity_edit.setObjectName("targeted_original_gravity_edit")
        self.horizontalLayout_6.addWidget(self.targeted_original_gravity_edit)
        self.label_5 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.targeted_bitterness_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.targeted_bitterness_label.setFont(font)
        self.targeted_bitterness_label.setObjectName("targeted_bitterness_label")
        self.horizontalLayout_6.addWidget(self.targeted_bitterness_label)
        self.targeted_bitterness_edit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.targeted_bitterness_edit.setMinimumSize(QtCore.QSize(0, 30))
        self.targeted_bitterness_edit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.targeted_bitterness_edit.setObjectName("targeted_bitterness_edit")
        self.horizontalLayout_6.addWidget(self.targeted_bitterness_edit)
        self.targeted_bitterness_unit_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.targeted_bitterness_unit_label.setFont(font)
        self.targeted_bitterness_unit_label.setObjectName("targeted_bitterness_unit_label")
        self.horizontalLayout_6.addWidget(self.targeted_bitterness_unit_label)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.recipe_cancel_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.recipe_cancel_button.setFont(font)
        self.recipe_cancel_button.setObjectName("recipe_cancel_button")
        self.horizontalLayout_4.addWidget(self.recipe_cancel_button)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem7)
        self.recipe_update_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.recipe_update_button.setFont(font)
        self.recipe_update_button.setObjectName("recipe_update_button")
        self.horizontalLayout_4.addWidget(self.recipe_update_button)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem8)
        self.recipe_add_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.recipe_add_button.setFont(font)
        self.recipe_add_button.setObjectName("recipe_add_button")
        self.horizontalLayout_4.addWidget(self.recipe_add_button)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem9)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem10)
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem11)
        self.verticalLayout_8.addLayout(self.horizontalLayout_5)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(-1, 30, -1, -1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.mash_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.mash_label.setFont(font)
        self.mash_label.setObjectName("mash_label")
        self.verticalLayout_5.addWidget(self.mash_label)
        self.line_2 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line_2.setLineWidth(2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_5.addWidget(self.line_2)
        self.malt_header_layout = QtWidgets.QHBoxLayout()
        self.malt_header_layout.setObjectName("malt_header_layout")
        self.malt_for_mash_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.malt_for_mash_label.setMinimumSize(QtCore.QSize(300, 0))
        self.malt_for_mash_label.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.malt_for_mash_label.setFont(font)
        self.malt_for_mash_label.setObjectName("malt_for_mash_label")
        self.malt_header_layout.addWidget(self.malt_for_mash_label)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.malt_header_layout.addItem(spacerItem12)
        self.verticalLayout_5.addLayout(self.malt_header_layout)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.malt_layout = QtWidgets.QVBoxLayout()
        self.malt_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.malt_layout.setObjectName("malt_layout")
        self.verticalLayout_4.addLayout(self.malt_layout)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        spacerItem13 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem13)
        self.line_5 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line_5.setLineWidth(2)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout_5.addWidget(self.line_5)
        self.rest_header_layout = QtWidgets.QHBoxLayout()
        self.rest_header_layout.setObjectName("rest_header_layout")
        self.mash_rests_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.mash_rests_label.setMinimumSize(QtCore.QSize(300, 0))
        self.mash_rests_label.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.mash_rests_label.setFont(font)
        self.mash_rests_label.setObjectName("mash_rests_label")
        self.rest_header_layout.addWidget(self.mash_rests_label)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.rest_header_layout.addItem(spacerItem14)
        self.verticalLayout_5.addLayout(self.rest_header_layout)
        self.rest_layout = QtWidgets.QVBoxLayout()
        self.rest_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.rest_layout.setObjectName("rest_layout")
        self.verticalLayout_5.addLayout(self.rest_layout)
        spacerItem15 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem15)
        self.verticalLayout_8.addLayout(self.verticalLayout_5)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(-1, 30, -1, -1)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.boiling_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.boiling_label.setFont(font)
        self.boiling_label.setObjectName("boiling_label")
        self.verticalLayout_6.addWidget(self.boiling_label)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.boiling_time_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.boiling_time_label.setFont(font)
        self.boiling_time_label.setObjectName("boiling_time_label")
        self.horizontalLayout_7.addWidget(self.boiling_time_label)
        self.boiling_time_edit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.boiling_time_edit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.boiling_time_edit.setObjectName("boiling_time_edit")
        self.horizontalLayout_7.addWidget(self.boiling_time_edit)
        self.boiling_time_unit_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.boiling_time_unit_label.setFont(font)
        self.boiling_time_unit_label.setObjectName("boiling_time_unit_label")
        self.horizontalLayout_7.addWidget(self.boiling_time_unit_label)
        spacerItem16 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem16)
        self.verticalLayout_6.addLayout(self.horizontalLayout_7)
        self.line_3 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line_3.setMinimumSize(QtCore.QSize(0, 10))
        self.line_3.setLineWidth(2)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_6.addWidget(self.line_3)
        self.hop_header_layout = QtWidgets.QHBoxLayout()
        self.hop_header_layout.setObjectName("hop_header_layout")
        self.hop_list_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.hop_list_label.setMinimumSize(QtCore.QSize(300, 0))
        self.hop_list_label.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.hop_list_label.setFont(font)
        self.hop_list_label.setObjectName("hop_list_label")
        self.hop_header_layout.addWidget(self.hop_list_label)
        spacerItem17 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hop_header_layout.addItem(spacerItem17)
        self.verticalLayout_6.addLayout(self.hop_header_layout)
        self.hop_layout = QtWidgets.QVBoxLayout()
        self.hop_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.hop_layout.setObjectName("hop_layout")
        self.verticalLayout_6.addLayout(self.hop_layout)
        self.line_4 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line_4.setLineWidth(2)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_6.addWidget(self.line_4)
        self.adjunct_header_layout = QtWidgets.QHBoxLayout()
        self.adjunct_header_layout.setObjectName("adjunct_header_layout")
        self.adjuncts_list_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.adjuncts_list_label.setMinimumSize(QtCore.QSize(300, 0))
        self.adjuncts_list_label.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.adjuncts_list_label.setFont(font)
        self.adjuncts_list_label.setObjectName("adjuncts_list_label")
        self.adjunct_header_layout.addWidget(self.adjuncts_list_label)
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.adjunct_header_layout.addItem(spacerItem18)
        self.verticalLayout_6.addLayout(self.adjunct_header_layout)
        self.adjunct_layout = QtWidgets.QVBoxLayout()
        self.adjunct_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.adjunct_layout.setObjectName("adjunct_layout")
        self.verticalLayout_6.addLayout(self.adjunct_layout)
        spacerItem19 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem19)
        self.verticalLayout_8.addLayout(self.verticalLayout_6)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.boiling_label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.boiling_label_2.setFont(font)
        self.boiling_label_2.setObjectName("boiling_label_2")
        self.verticalLayout_7.addWidget(self.boiling_label_2)
        self.yeast_header_layout = QtWidgets.QHBoxLayout()
        self.yeast_header_layout.setObjectName("yeast_header_layout")
        self.yeast_list_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.yeast_list_label.setMinimumSize(QtCore.QSize(300, 0))
        self.yeast_list_label.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.yeast_list_label.setFont(font)
        self.yeast_list_label.setObjectName("yeast_list_label")
        self.yeast_header_layout.addWidget(self.yeast_list_label)
        spacerItem20 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.yeast_header_layout.addItem(spacerItem20)
        self.verticalLayout_7.addLayout(self.yeast_header_layout)
        self.yeast_layout = QtWidgets.QVBoxLayout()
        self.yeast_layout.setObjectName("yeast_layout")
        self.verticalLayout_7.addLayout(self.yeast_layout)
        self.fermentation_explain_edit = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        self.fermentation_explain_edit.setObjectName("fermentation_explain_edit")
        self.verticalLayout_7.addWidget(self.fermentation_explain_edit)
        self.verticalLayout_8.addLayout(self.verticalLayout_7)
        self.recipe_close_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.recipe_close_button.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.recipe_close_button.setFont(font)
        self.recipe_close_button.setObjectName("recipe_close_button")
        self.verticalLayout_8.addWidget(self.recipe_close_button)
        spacerItem21 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem21)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.recipe_list_label.setText(_translate("Form", "Recipe Database list"))
        self.recipe_edit_button.setText(_translate("Form", "Edit"))
        self.recipe_delete_button.setText(_translate("Form", "Delete"))
        self.recipe_new_button.setText(_translate("Form", "New"))
        self.recipe_name_label.setText(_translate("Form", "TextLabel"))
        self.targets_name_label.setText(_translate("Form", "Targets"))
        self.targeted_original_gravity_label.setText(_translate("Form", "Orignal gravity"))
        self.label_5.setText(_translate("Form", "SG"))
        self.targeted_bitterness_label.setText(_translate("Form", "Bitterness"))
        self.targeted_bitterness_unit_label.setText(_translate("Form", "IBU"))
        self.recipe_cancel_button.setText(_translate("Form", "Cancel"))
        self.recipe_update_button.setText(_translate("Form", "Update this recipe"))
        self.recipe_add_button.setText(_translate("Form", "Record this recipe"))
        self.mash_label.setText(_translate("Form", "Mashing"))
        self.malt_for_mash_label.setText(_translate("Form", "Malts for mash"))
        self.mash_rests_label.setText(_translate("Form", "Mash Rests"))
        self.boiling_label.setText(_translate("Form", "Boiling"))
        self.boiling_time_label.setText(_translate("Form", "Boiling time"))
        self.boiling_time_unit_label.setText(_translate("Form", "min."))
        self.hop_list_label.setText(_translate("Form", "Hops"))
        self.adjuncts_list_label.setText(_translate("Form", "Adjuncts"))
        self.boiling_label_2.setText(_translate("Form", "Fermentation"))
        self.yeast_list_label.setText(_translate("Form", "Yeast"))
        self.recipe_close_button.setText(_translate("Form", "Close"))

