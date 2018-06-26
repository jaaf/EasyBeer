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


from PyQt5.QtWidgets import  QWidget

from gen import RestDialogCreateUI

from model.Rest import Rest
import view.styles as sty


class RestDialogCreate(QWidget,RestDialogCreateUI.Ui_Form ):
    """
       class docs
    """   
    
    def __init__(self,model,controller,util):
        QWidget.__init__(self)
        self.setupUi(self)
        print ('RestDialog: creating a MaltDialog object')
        self.model = model
        self.controller=controller
        self.util=util
        self.current_rest=None # the rest currently selected
        
        # register function with model for future model update announcements
        self.model.subscribe_model_changed(['rest'],self.on_model_changed_rest_create)
        
        self.add_button.hide()
        self.set_ro()
        self.init_dialog_and_connections()
             
        self.rest_key_list=self.model.rest_list        
          
        self.refresh_rest_list_combo()  
        #self.set_translatable_texts()  
        
    def clear_edits(self):
        self.refresh_rest_list_combo()
        self.name_edit.setText('')
        for i in range(self.ph_layout.count()):
            item=self.ph_layout.itemAt(i)
            if item:
                item.widget().setText('')
        for i in range(self.temperature_layout.count()):
            item=self.temperature_layout.itemAt(i)
            if item:
                item.widget().setText('')
        self.usage_guidance_edit.setText('')        
            
        
    def create_rest(self):
        self.set_rw()
        self.clear_edits()
        self.add_button.show() 
        
    def delete_rest(self):
        name=str(self.name_combo.currentText())
        self.current_rest=None
        self.model.remove_rest(name)
        
    
          
    def edit_rest(self):   
        self.add_button.show() 
        self.set_rw()
       
        
    def name_combo_current_item_changed(self):
        name=str(self.name_combo.currentText())
        if name:
            rest=self.model.get_rest(name)
            self.name_edit.setText(rest.name)
            for i in range(self.ph_layout.count()):
                item=self.ph_layout.itemAt(i)
                if item:
                    item.widget().setText(str(rest.phs[i]))
                    
            for i in range(self.temperature_layout.count()):
                item=self.temperature_layout.itemAt(i)
                if item:
                    item.widget().setText(str(rest.temperatures[i]))     
            self.usage_guidance_edit.setPlainText(rest.guidance)           
        print(name)
        
        
        
            
        
    def read_input(self):
        name=self.util.check_input(self.name_edit,True,self.tr('Name'),False)
        if not name: return
        phs=[]
        for i in range(self.ph_layout.count()):
            item=self.ph_layout.itemAt(i)
            if item:
                ph=self.util.check_input(item.widget(),False,self.tr('PH value ' + str(i)), False,0,14)
                if not ph: return
                else:
                    phs.append(ph)
                    
                    
        temperatures=[]
        for i in range(self.temperature_layout.count()):
            item=self.temperature_layout.itemAt(i)
            if item:
                t=self.util.check_input(item.widget(),False,self.tr('Temperature value ' + str(i)), False,0,80)
                if not t :return
                else:
                    temperatures.append(t)        
                    
        guidance=self.usage_guidance_edit.toPlainText()                        
                    
        
        
        return Rest(name,phs,temperatures,guidance)    
    
    def refresh_rest_list_combo(self):
        self.name_combo.clear()
        self.name_combo.addItem('')
        for r in self.rest_key_list:
            self.name_combo.addItem(r)
        
        
        if self.current_rest:
            #print('RestDialogCreate : current_rest is set and equal to: '+self.current_rest)
            index = self.name_combo.findData(self.current_rest)
            self.name_combo.setCurrentIndex(index) 
        else:
            index = self.name_combo.findData('')
            self.name_combo.setCurrentIndex(index)    
             
     
    def on_model_changed_rest_create(self,target):
        '''
        This function is called by the model when it changes
        due to the fact that it is subscribed as callback
        on initialization
        '''
        if target == 'rest':
            self.rest_key_list=self.model.rest_list 
            self.refresh_rest_list_combo()
            self.clear_edits()       
        
    def save_rest(self):
        'save or update the rest that is defined by the GUI'
        rest=self.read_input()
        self.current_rest=rest.name # in order to be able to select it back on refresh
        for i in range(len(rest.phs)):
            print('ph '+str(i)+' : '+str(rest.phs[i]))
        for i in range(len(rest.temperatures)):
            print('temp '+str(i)+' : '+str(rest.temperatures[i]))    
        self.model.save_rest(rest)
        self.set_ro()
        #self.set_read_only_style()
        self.add_button.hide()
        
        
    def init_dialog_and_connections(self):
        self.add_button.clicked.connect(self.save_rest)
        self.edit_button.clicked.connect(self.edit_rest)
        self.new_button.clicked.connect(self.create_rest)
        self.delete_button.clicked.connect(self.delete_rest)
        self.name_combo.currentIndexChanged.connect(self.name_combo_current_item_changed)
        #self.close_button.clicked.connect(self.close)  
        
    def set_ro(self):
        #self.name_combo.setEnabled(False)
        self.name_edit.setReadOnly(True)
        self.name_edit.setStyleSheet(sty.field_styles['read_only'])
        for i in range (self.ph_layout.count()):
            item=self.ph_layout.itemAt(i)
            if item:
                item.widget().setReadOnly(True)
                item.widget().setStyleSheet(sty.field_styles['read_only'])
                
        for i in range (self.temperature_layout.count()):
            item=self.temperature_layout.itemAt(i)
            if item:
                item.widget().setReadOnly(True)
                item.widget().setStyleSheet(sty.field_styles['read_only'])  
                
        self.usage_guidance_edit.setReadOnly(True)
        self.usage_guidance_edit.setStyleSheet(sty.field_styles['read_only'])    
        
    def set_rw(self):
        self.name_combo.setEnabled(True)
        self.name_edit.setReadOnly(False)
        self.name_edit.setStyleSheet(sty.field_styles['editable'])
        for i in range (self.ph_layout.count()):
            item=self.ph_layout.itemAt(i)
            if item:
                item.widget().setReadOnly(False)
                item.widget().setStyleSheet(sty.field_styles['editable'])
                
        for i in range (self.temperature_layout.count()):
            item=self.temperature_layout.itemAt(i)
            if item:
                item.widget().setReadOnly(False)
                item.widget().setStyleSheet(sty.field_styles['editable'])  
                
        self.usage_guidance_edit.setReadOnly(False)
        self.usage_guidance_edit.setStyleSheet(sty.field_styles['editable'])                      
                
                    
     