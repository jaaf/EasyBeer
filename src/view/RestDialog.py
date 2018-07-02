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
from PyQt5.QtWidgets import  QWidget,QMessageBox

from gen import RestDialogUI

from model.Rest import Rest
from model.RestInRecipe import RestInRecipe

import view.styles as sty


class RestDialog(QWidget,RestDialogUI.Ui_Form ):
   
    def __init__(self,owner):
        QWidget.__init__(self,None,QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.owner=owner
        self.util=owner.util
        self.rest_key_list=self.owner.model.rest_list  
        self.current_rest=None  
        self.refresh_rest_list_widget()
        self.owner.model.subscribe_model_changed(['rest'],self.on_model_changed_rest) 
        
        self.init_dialog_and_connections()  
        self.init_styles()
        
    def add_rest(self):
        rest=self.get_rest()
        if not rest: return
        self.owner.insert_rest(self.rest_list_combo.currentIndex()+1,rest)
        self.update_rest_list()
        self.hide()
        
    def clear_edits(self):
        self.purpose_edit.clear()  
        self.temperature_edit.clear()
        self.duration_edit.clear()
        
        
    def explain_rest_selection(self): 
        message =self.tr('''
        <h2>Rest selection guidance</h2>
        <p>You can select a kind of rest in the list beside. This will
        show you some guidance about this specific kind of rest and pre-fill
        the three fields in the customize part at the bottom of the
        dialog. </p>
        
        <p>Some very basic and classical rests come with the program installation. Nevertheless, the user can
        use the Rest Dialog from the Database menu to add frequently used rests and their definition.<p> 
        
        <p>Whatever the source of the used rest, you will be still able to change anything you
        want to customize the rest as you intend. Moreover, you will
        be able to change this field values even after the rest has 
        been transfered into the recipe dialog.</p>
        
        <p>Please, consider this dialog as guidance, not as coerce.</p>
        ''' 
        )   
        self.util.alerte(message,QMessageBox.Information,self.tr('Info : Using the rest dialog?'))     
              
    
    def get_rest(self):
        purpose=self.util.check_input(self.purpose_edit,True,self.tr('purpose '),False)
        if not purpose: return
        duration = self.util.check_input(self.duration_edit,False,self.tr('duration'),False,0,200)
        if not duration: return
        temperature = self.util.check_input(self.temperature_edit,False,self.tr('temperature'),False,0,100)
        if not temperature: return
        self.clear_edits()
        return RestInRecipe(purpose, duration,temperature)
    
    def init_styles(self):
        self.purpose_edit.setStyleSheet(sty.field_styles['editable'])
        self.temperature_edit.setStyleSheet(sty.field_styles['editable'])
        self.duration_edit.setStyleSheet(sty.field_styles['editable'])
        
        self.ph_min.setStyleSheet(sty.field_styles['min_max_allowed'])
        self.ph_max.setStyleSheet(sty.field_styles['min_max_allowed'])
        self.temperature_min.setStyleSheet(sty.field_styles['min_max_allowed'])
        self.temperature_max.setStyleSheet(sty.field_styles['min_max_allowed'])
        
        self.optimal_ph_min.setStyleSheet(sty.field_styles['min_max_advised'])
        self.optimal_ph_max.setStyleSheet(sty.field_styles['min_max_advised'])
        self.optimal_temperature_min.setStyleSheet(sty.field_styles['min_max_advised'])
        self.optimal_temperature_max.setStyleSheet(sty.field_styles['min_max_advised'])
    
    def refresh_select_rest_combo(self):
        self.select_rest_combo.clear()
        self.select_rest_combo.addItem('')
        for r in self.rest_key_list:
            self.select_rest_combo.addItem(r)
        
        if self.current_rest:
            #print('RestDialogCreate : current_rest is set and equal to: '+self.current_rest)
            index = self.select_rest_combo.findData(self.current_rest)
            self.select_rest_combo.setCurrentIndex(index) 
        else:
            index = self.select_rest_combo.findData('')
            self.select_rest_combo.setCurrentIndex(index) 
            
    def refresh_rest_list_widget(self,select=None):
        
        self.rest_list_widget.clear()
        for key in self.rest_key_list:
            self.rest_list_widget.addItem(key)

        if self.current_rest:
            #print('RestDialogCreate : current_rest is set and equal to: '+self.current_rest)
            item=self.rest_list_widget.findItems(self.current_rest,QtCore.Qt.MatchExactly)
            self.rest_list_widget.setCurrentItem(item[0])             
            
    def on_model_changed_rest(self,target):
        if target == 'rest':
            self.refresh_rest_list_widget()     
        
    def selection_changed_rest(self):
        if self.rest_list_widget.currentItem():
            name=self.rest_list_widget.currentItem().text()   
        if name:     
            rest=self.owner.model.get_rest(str(name))
            for i in range(self.ph_layout.count()):
                item=self.ph_layout.itemAt(i)
                if item:
                    item.widget().setText(str(rest.phs[i]))
                    
            for i in range(self.temperature_layout.count()):
                item=self.temperature_layout.itemAt(i)
                if item:
                    item.widget().setText(str(rest.temperatures[i]))     
            self.guidance_text.setText(rest.guidance)  
            self.purpose_edit.setText(name)
            self.temperature_edit.setText(str((rest.temperatures[1]+rest.temperatures[2])/2))    
            self.duration_edit.setText(str(60))#this is the recommended duration     
        #print(name)
   
        
    def init_dialog_and_connections(self):
        self.add_button.clicked.connect(self.add_rest)
        self.rest_list_widget.currentItemChanged.connect(self.selection_changed_rest)
        self.select_guidance_help_button.clicked.connect(self.explain_rest_selection)
        
    def set_translatable_textes(self):
        self.setWindowTitle(self.tr('Dialog: choosing a rest for recipe'))
        self.select_rest_label.setText(self.tr('Select a rest type for guidance'))
        self.standard_settings_label.setText(self.tr('Standard Settings'))
        self.customize_zone_label.setText(self.tr('Customize your rest'))
        self.purpose_label.setText(self.tr('Purpose or name'))
        self.duration_label.setText(self.tr('Duration'))
        self.temperature_label.setText(self.tr('Temperature'))
        self.temperature_range_label.setText(self.tr('Temperature Range'))
        self.ph_range_label.setText(self.tr('PH Range'))
        self.insert_after_label.setText(self.tr('Insert after'))
        self.add_button.setText(self.tr('Add this rest'))  
 
    def showEvent(self, event):
        self.update_rest_list()
        self.set_translatable_textes()
        
        
        
    def update_rest_list(self):
        
        #print ('Updating rest list')
        self.rest_list_combo.clear()
        for r in self.owner.rest_list:
            #print(r.purpose + ' in rest list')
            self.rest_list_combo.addItem(r.purpose)
            