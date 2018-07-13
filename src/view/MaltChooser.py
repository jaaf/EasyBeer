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
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

from gen import MaltChooserUI
import view.styles as sty




class MaltChooser(QWidget,MaltChooserUI.Ui_Form ):
   
    def __init__(self,owner):
        QWidget.__init__(self,None,QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.owner=owner
        self.malt_key_list=self.owner.model.malt_list
        for key in self.malt_key_list:
            self.malt_list_widget.addItem(key)  
        self.owner.model.subscribe_model_changed(['malt'],self.on_model_changed_malt_chooser)
        self.init_dialog_and_connections() 
        self.set_ro() 
        
    def add_malt_view(self):
        maltT=self.owner.model.get_malt(str(self.malt_list_widget.currentItem().text()))
        self.owner.add_malt_view(maltT)
        self.hide()      
    
   
        
    def load_selected_malt(self):
        #load the selected yeast
        #using hasattr allows the addition of new properties during development
        
        if self.malt_list_widget.currentItem():
            maltT=self.owner.model.get_malt(self.malt_list_widget.currentItem().text())
            if hasattr(maltT,'name'):
                self.name_edit.setText(maltT.name)
            print('malt name loaded')   
            if hasattr(maltT,'maker'):
                self.maker_edit.setText(maltT.maker)
    
            if hasattr(maltT,'max_yield'):
                self.max_yield_edit.setText(str(maltT.max_yield))              
                
                
            if hasattr(maltT,'color'):    
                self.color_edit.setText(str(maltT.color))
                
            if hasattr(maltT,'kolbach_min'):    
                self.kolbach_min.setText(str(maltT.kolbach_min))
                
            if hasattr(maltT,'kolbach_max'):    
                self.kolbach_max.setText(str(maltT.kolbach_max))


        
    def selection_changed_malt(self):
        print('selection changed')
        self.load_selected_malt()     
        
    def init_dialog_and_connections(self):
        self.add_button.clicked.connect(self.add_malt_view)    
        self.close_button.clicked.connect(self.close)
        self.malt_list_widget.currentItemChanged.connect(self.selection_changed_malt)
        self.malt_list_widget.currentItemChanged.connect(self.selection_changed_malt)
        
    def set_ro(self):
        self.color_edit.setReadOnly(True)
        self.color_edit.setStyleSheet(sty.field_styles['read_only'])
        self.max_yield_edit.setReadOnly(True) 
        self.max_yield_edit.setStyleSheet(sty.field_styles['read_only'])
        self.color_edit.setReadOnly(True)  
        self.color_edit.setStyleSheet(sty.field_styles['read_only']) 
        self.maker_edit.setReadOnly(True)  
        self.maker_edit.setStyleSheet(sty.field_styles['read_only']) 
        self.name_edit.setReadOnly(True)  
        self.name_edit.setStyleSheet(sty.field_styles['read_only']) 
        self.kolbach_max.setReadOnly(True)  
        self.kolbach_max.setStyleSheet(sty.field_styles['read_only']) 
        self.kolbach_min.setReadOnly(True)  
        self.kolbach_min.setStyleSheet(sty.field_styles['read_only'])         
                
    def set_translatable_text(self):
        self.add_button.setText(self.tr('Add this malt'))   
        self.close_button.setText(self.tr('Close'))
        self.name_label.setText(self.tr('Name'))
        self.color_label.setText(self.tr('Color'))
        self.max_yield_label.setText(self.tr('Maximum Yield'))
        self.add_button.setText(self.tr('Add this malt'))
        
    def showEvent(self, ev):
        pass
        #self.set_translatable_text()  
        #self.setReadOnly(True)  
        
    def on_model_changed_malt_chooser(self, target):
        if target == 'malt':
            self.malt_list_widget.clear()
            self.malt_key_list=self.owner.model.malt_list
            for key in self.malt_key_list:
                self.malt_list_widget.addItem(key)   
            self.selection_changed_malt()#to force updating of the dialog       
        
