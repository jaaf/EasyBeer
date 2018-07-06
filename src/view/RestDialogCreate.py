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
import model.constants as mcst
import view.styles as sty
import view.constants as vcst
import platform


class RestDialogCreate(QWidget,RestDialogCreateUI.Ui_Form ):
    """
       class docs
    """   
    
    def __init__(self,model,controller,util):
        QWidget.__init__(self)
        self.setupUi(self)
        self.model = model
        self.controller=controller
        self.util=util
        self.current_rest=None # the rest currently selected
        
        # register function with model for future model update announcements
        self.model.subscribe_model_changed(['rest','fontset'],self.on_model_changed_rest_create)
        
        self.add_button.hide()
        self.cancel_button.hide()
        self.delete_button.hide()
        self.edit_button.hide()
        self.update_button.hide()
        self.set_ro()
        self.init_dialog_and_connections()
        
             
        self.rest_key_list=self.model.rest_list        
        self.ensure_unremovable_rests()  
        self.refresh_rest_list_combo()  
        self.set_translatable_textes()
        #self.set_translatable_texts()  
        
    def cancel(self):
        self.clear_edits()
        self.set_ro()
        self.cancel_button.hide()
        self.add_button.hide()
        self.update_button.hide()
        self.new_button.show()
        pass    
        
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
     
    def create_unremovable_rests(self):
        self.prot_rest=Rest('Protein Rest',[4.5, 5, 6, 7],[65,66,68,70],self.tr(mcst.TEXT_REST_PROTEIN),'no')
        self.sach_rest=Rest('Saccharification Rest',[4.5, 5, 6, 7],[65,66,68,70],self.tr(mcst.TEXT_REST_SACH),'no') 
        
    def create_rest(self):
        self.set_rw()
        self.clear_edits()
        self.add_button.show() 
        self.cancel_button.show()
        self.new_button.hide()
        self.delete_button.hide()
        self.edit_button.hide()
        
    def delete_rest(self):
        name=str(self.name_combo.currentText())
        r=self.model.get_rest(name)
        if r.removable=='no':
            self.util.alerte(self.tr('You cannot delete this basic rest'))
            return
        
        self.current_rest=None
        self.model.remove_rest(name)
        
    
          
    def edit_rest(self):   
        name=str(self.name_combo.currentText())
        r=self.model.get_rest(name)
        if r.removable=='no':
            self.util.alerte(self.tr('You cannot edit this kind of basic rest'))
            return
        self.update_button.show() 
        self.cancel_button.show()
        self.edit_button.hide()
        self.delete_button.hide()
        self.new_button.hide()
        self.set_rw()
       
    def ensure_unremovable_rests(self):
        self.create_unremovable_rests()
        if not ('Protein Rest' in self.rest_key_list):
            self.model.save_rest(self.prot_rest)
        if not('Saccharification Rest' in self.rest_key_list):
            self.model.save_rest(self.sach_rest)    
            
           
        
    def name_combo_current_item_changed(self):
        unit=self.model.get_unit('temperature')
        if unit:
            unit_label=self.util.get_unit_label(unit)
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
                    item.widget().setText(str(self.util.convert_to(unit,rest.temperatures[i]))  )   
                    self.temp_unit_label.setText(unit_label)
            self.usage_guidance_edit.setHtml(rest.guidance) 
            if rest.removable=='no':
                self.usage_guidance_edit.setStyleSheet('color:green')
            else: 
                self.usage_guidance_edit.setStyleSheet('color:blue')
                self.edit_button.show()  
                self.delete_button.show()         
       
        
        
        
            
        
    def read_input(self):
        unit=self.model.get_unit('temperature')
        name=self.util.check_input(self.name_edit,True,self.tr('Name'),False)
        if not name: 
            return
        phs=[]
        for i in range(self.ph_layout.count()):
            item=self.ph_layout.itemAt(i)
            if item:
                ph=self.util.check_input(item.widget(),False,self.tr('PH value ' + str(i)), False,0,14)
                if not ph: 
                    return
                else:
                    phs.append(ph)                          
        temperatures=[]
        for i in range(self.temperature_layout.count()):
            item=self.temperature_layout.itemAt(i)
            if item:
                t=self.util.check_input(item.widget(),False,self.tr('Temperature value ' + str(i)), False,0,80,None,unit)
                if not t :return
                else: temperatures.append(t)                     
        guidance=self.usage_guidance_edit.toPlainText()                        
        return Rest(name,phs,temperatures,guidance)    
    
    
    def refresh_rest_list_combo(self):
        self.name_combo.clear()
        self.name_combo.addItem('')
        for r in self.rest_key_list:
            self.name_combo.addItem(r)
        
        
        if self.current_rest:
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
            
        'we must wait for fonts to be initialized in model'    
        if target == 'fontset':
            if (self.model.in_use_fonts):
                self.set_fonts()         
        
    def save_rest(self):
        'save or update the rest that is defined by the GUI'
        rest=self.read_input()
        self.current_rest=rest.name # in order to be able to select it back on refresh    
        self.model.save_rest(rest)
        self.set_ro()
        self.add_button.hide()
        
        
    def init_dialog_and_connections(self):
        self.add_button.clicked.connect(self.save_rest)
        self.edit_button.clicked.connect(self.edit_rest)
        self.cancel_button.clicked.connect(self.cancel)
        self.update_button.clicked.connect(self.update_rest)
        self.new_button.clicked.connect(self.create_rest)
        self.delete_button.clicked.connect(self.delete_rest)
        self.name_combo.currentIndexChanged.connect(self.name_combo_current_item_changed)
        #self.close_button.clicked.connect(self.close)  
     
     
    def set_fonts(self):
        pf=platform.system()
        self.add_button.setStyleSheet('background-color:lightgreen;')
        self.update_button.setStyleSheet('background-color:lightgreen;')
        self.cancel_button.setStyleSheet('background-color:pink:ont-family')
        self.add_button.setFont(self.model.in_use_fonts['button'])
        self.update_button.setFont(self.model.in_use_fonts['button'])
        self.cancel_button.setFont(self.model.in_use_fonts['button'])
        self.edit_button.setFont(self.model.in_use_fonts['button'])
        self.delete_button.setFont(self.model.in_use_fonts['button'])
        self.new_button.setFont(self.model.in_use_fonts['button'])
        self.main_label.setFont(self.model.in_use_fonts['title'])
        self.choose_label.setFont(self.model.in_use_fonts['title_slanted'])
        self.name_label.setFont(self.model.in_use_fonts['field'])
        self.ph_range_label.setFont(self.model.in_use_fonts['field'])
        self.temperature_label.setFont(self.model.in_use_fonts['field'])
        self.name_edit.setFont(self.model.in_use_fonts['field'])
        self.name_combo.setFont(self.model.in_use_fonts['field'])
        self.ph_max.setFont(self.model.in_use_fonts['field'])
        self.ph_min.setFont(self.model.in_use_fonts['field']) 
        self.optimal_ph_max.setFont(self.model.in_use_fonts['field'])
        self.optimal_ph_min.setFont(self.model.in_use_fonts['field'])
        self.temperature_max.setFont(self.model.in_use_fonts['field'])
        self.temperature_min.setFont(self.model.in_use_fonts['field'])
        self.optimal_temperature_max.setFont(self.model.in_use_fonts['field'])
        self.optimal_temperature_min.setFont(self.model.in_use_fonts['field']) 
        self.temp_unit_label.setFont(self.model.in_use_fonts['field'])   
        self.usage_guidance_edit.setFont(self.model.in_use_fonts['field'])       
            
            
        
           
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
        
    def set_translatable_textes(self):
        self.main_label.setText(self.tr('Rest Database'))     
        self.choose_label.setText(self.tr('Select a rest here or create a new one')) 
        self.name_label.setText(self.tr('Name'))
        self.ph_range_label.setText(self.tr('PH range'))
        self.temperature_label.setText(self.tr('Temperature range'))
        
        
        self.add_button.setText(self.tr('Add this rest'))
        self.cancel_button.setText(self.tr('Cancel'))
        self.update_button.setText(self.tr('Update this rest'))
        self.delete_button.setText(self.tr('Delete'))
        self.new_button.setText(self.tr('New'))
        self.edit_button.setText(self.tr('Edit'))
        
    def showEvent(self,e):  
        self.set_fonts()   
        
    def update_rest(self):
        'update the rest that is defined by the GUI'
        rest=self.read_input()
        self.current_rest=rest.name # in order to be able to select it back on refresh    
        self.model.update_rest(rest)
        self.set_ro()
        #self.set_read_only_style()
        self.update_button.hide()  
        self.cancel_button.hide()
                          
                
                    
     