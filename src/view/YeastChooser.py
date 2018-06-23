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

from gen import YeastChooserUI




class YeastChooser(QWidget,YeastChooserUI.Ui_Form ):
   
    def __init__(self,owner):
        QWidget.__init__(self,None,QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        
        self.owner=owner
        self.yeast_key_list=self.owner.model.yeast_list
        for key in self.yeast_key_list:
            self.yeast_list_widget.addItem(key)  
        self.owner.model.subscribe_model_changed(['yeast'],self.on_model_changed_yeast_chooser)    
        self.set_connections()  
     
        
        
    def add_yeast_view(self):
        yeastT=self.owner.model.get_yeast(str(self.yeast_list_widget.currentItem().text()))
        self.owner.set_yeast_view(yeastT)      
    
   
        
    def load_selected_yeast(self):
        #load the selected yeast
        #using hasattr allows the addition of new properties during development
        
        if self.yeast_list_widget.currentItem():
            yeastT=self.owner.model.get_yeast(self.yeast_list_widget.currentItem().text())
            if hasattr(yeastT,'name'):
                self.name_edit.setText(yeastT.name)
                
            if hasattr(yeastT,'maker'):
                self.maker_edit.setText(yeastT.maker)
                
            if hasattr(yeastT,'max_allowed_temperature'):    
                self.max_allowed_temperature_edit.setText(str(yeastT.max_allowed_temperature))
                
            if hasattr(yeastT,'min_allowed_temperature'):    
                self.min_allowed_temperature_edit.setText(str(yeastT.min_allowed_temperature))
                
            if hasattr(yeastT,'max_advised_temperature'):    
                self.max_advised_temperature_edit.setText(str(yeastT.max_advised_temperature))
                
            if hasattr(yeastT,'min_advised_temperature'):    
                self.min_advised_temperature_edit.setText(str(yeastT.min_advised_temperature))
                
            if hasattr(yeastT,'form'):
                self.form_edit.setText(yeastT.form)
            
            if hasattr(yeastT,'attenuation'):
                self.attenuation_edit.setText(yeastT.attenuation)
                
            if hasattr(yeastT,'floculation'):
                self.floculation_edit.setText(yeastT.floculation) 
                  
        
    def selection_changed_yeast(self):
        print('selection changed')
        self.load_selected_yeast()     
        
    def set_connections(self):
        self.add_button.clicked.connect(self.add_yeast_view)    
        self.yeast_list_widget.currentItemChanged.connect(self.selection_changed_yeast)
        self.close_button.clicked.connect(self.close)
        
    def set_ro(self):
        self.name_edit.setReadOnly(True)
        self.maker_edit.setReadOnly(True)
        self.max_allowed_temperature_edit.setReadOnly(True)
        self.min_allowed_temperature_edit.setReadOnly(True)
        self.max_advised_temperature_edit.setReadOnly(True)
        self.min_advised_temperature_edit.setReadOnly(True)
        self.form_edit.setReadOnly(True)
        self.attenuation_edit.setReadOnly(True)
        self.floculation_edit.setReadOnly(True)
            
        
    def set_translatable_textes(self):
        self.setWindowTitle(self.tr('Yeast Chooser'))
        self.yeast_list_label.setText(self.tr('Yeast List'))
        self.detail_label.setText(self.tr('Selected Yeast Details'))
        self.add_button.setText(self.tr('Select this yeast'))
        self.name_label.setText(self.tr('Name'))
        self.maker_label.setText(self.tr('Maker'))
        self.max_allowed_temperature_label.setText(self.tr('Maximum Allowed Temperature'))
        self.min_allowed_temperature_label.setText(self.tr('Minimum Allowed Temperature'))
        self.max_advised_temperature_label.setText(self.tr('Maximum Advised Temperature'))
        self.min_advised_temperature_label.setText(self.tr('Minimum Advised Temperature'))
        self.form_label.setText(self.tr('Form'))
        self.attenuation_label.setText(self.tr('Attenuation'))
        self.floculation_label.setText(self.tr('Floculation'))
            
    def showEvent(self, ev):
        self.set_translatable_textes()
        self.set_ro()  
        
    def on_model_changed_yeast_chooser(self,target):
        self.yeast_list_widget.clear()
        self.yeast_key_list=self.owner.model.yeast_list
        for key in self.yeast_key_list:
            self.yeast_list_widget.addItem(key) 
        self.selection_changed_yeast()#to force updating of the dialog   
        

        