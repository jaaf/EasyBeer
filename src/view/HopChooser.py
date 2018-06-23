# -*- coding: utf-8 -*-­

#EasyBeer
#Copyright (C) 2018 José FOURNIER

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 3
#of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,QHBoxLayout,QLabel,QLineEdit,QMessageBox,QFrame

from gen import HopChooserUI
import view.styles as sty




class HopChooser(QWidget,HopChooserUI.Ui_Form ):
   
    def __init__(self,owner):
        QWidget.__init__(self,None,QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        
        self.owner=owner
        self.hop_key_list=self.owner.model.hop_list
        for key in self.hop_key_list:
            self.hop_list_widget.addItem(key)  
        self.owner.model.subscribe_model_changed(['hop'],self.on_model_changed_hop_chooser)     
        self.set_connections()  
        
        
    def save_hop(self):
        hopT=self.owner.model.get_hop(str(self.hop_list_widget.currentItem().text()))
        self.owner.save_hop(hopT)  
        self.hide()    
    
   
        
    def load_selected_hop(self):
        
        if self.hop_list_widget.currentItem():
            hopT=self.owner.model.get_hop(self.hop_list_widget.currentItem().text())
            
            if hasattr(hopT,'name'):
                self.name_edit.setText(hopT.name)
            if hasattr(hopT,'alpha_acid'):
                self.alpha_acid_edit.setText(str(hopT.alpha_acid))    
            if hasattr(hopT,'form'):
                self.form_edit.setText(str(hopT.form))   
        
        
    def selection_changed_hop(self):
        print('selection changed')
        self.load_selected_hop()     
        
    def set_connections(self):
        self.hop_add_button.clicked.connect(self.save_hop)    
        self.hop_list_widget.currentItemChanged.connect(self.selection_changed_hop)
        self.hop_list_widget.currentItemChanged.connect(self.selection_changed_hop)
        self.close_button.clicked.connect(self.close)
        
    def set_ro(self):
        self.alpha_acid_edit.setReadOnly(True)
        self.alpha_acid_edit.setStyleSheet(sty.field_styles['read_only'])
        self.name_edit.setReadOnly(True)
        self.name_edit.setStyleSheet(sty.field_styles['read_only'])
        self.form_edit.setReadOnly(True)
        self.form_edit.setStyleSheet(sty.field_styles['read_only'])
            
        
    def set_translatable_textes(self):
        self.hop_list_label.setText(self.tr('Available hops'))
        self.name_label.setText(self.tr('Name '))
        self.alpha_acid_label.setText(self.tr('Alpha acids'))
        self.form_label.setText(self.tr('Form'))
        self.hop_add_button.setText(self.tr('Add this hop'))
        self.close_button.setText(self.tr('Close'))
            
    def showEvent(self, ev):
        self.set_translatable_textes()
        self.set_ro()    
        
    def on_model_changed_hop_chooser(self,target):
        if target == 'hop':
            self.hop_list_widget.clear()
            self.hop_key_list=self.owner.model.hop_list
            print (self.hop_list_widget)
            for key in self.hop_key_list:
                self.hop_list_widget.addItem(key) 
            self.selection_changed_hop()#to force updating of the dialog
               
        
        