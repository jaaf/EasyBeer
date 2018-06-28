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
from PyQt5.QtWidgets import  QWidget, QMessageBox

from gen import YeastDialogUI
from model.Yeast import Yeast
import view.styles as sty



#from PyQt4.QtGui import QStandardItemModel,QStandardItem,QItemSelectionModel

class YeastDialog(QWidget,YeastDialogUI.Ui_Form ):
    """
       class docs
    """   
    
    def __init__(self,model,controller,util):
        QWidget.__init__(self,None,QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.model = model
        self.controller=controller
        self.util=util
        self.current_yeast=None # the yeast currently selected
        'register function with model for future model update announcements'
        self.model.subscribe_model_changed(['yeast'],self.on_model_has_changed_yeast)    
        self.add_button.hide()
        self.set_read_only()
        self.init_dialog_and_connections()        
        self.yeast_key_list=self.model.yeast_list             
        self.refresh_yeast_list_widget()  
        self.add_button.setStyleSheet('background-color:lightgreen')
        self.update_button.setStyleSheet('background-color:lightgreen')
        self.cancel_button.setStyleSheet('background-color:pink')

     
    def alerte_empty_name(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Name cannot be empty")
        msg.setWindowTitle("Warning Empty Name")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

 
    def cancel(self):
        'after canceling an update or a creation'  
        self.current_yeast=None
        self.selection_changed()  
        self.refresh_yeast_list_widget()   
        'as selection_changed shows them'
        self.edit_button.hide()
        self.delete_button.hide() 
        self.new_button.show()  
        
                
    def clear_edits(self):
        #whenever the user wants to new a new yeast
        self.name_edit.setText('')  
        self.maker_edit.setText('')
        self.max_allowed_temperature_edit.setText('')
        self.min_allowed_temperature_edit.setText('')
        self.max_advised_temperature_edit.setText('')
        self.min_advised_temperature_edit.setText('')
        idx =self.form_combo.findText('')
        self.form_combo.setCurrentIndex(idx)    
        idx =self.attenuation_combo.findText('')
        self.attenuation_combo.setCurrentIndex(idx)    
        idx =self.floculation_combo.findText('')
        self.floculation_combo.setCurrentIndex(idx)
        
    
    def closeEvent(self,event):
        self.close()
    
    def delete_yeast(self):
        'ask the model to delete the current yeast'
        yeastT=self.model.get_yeast(str(self.yeast_list_widget.currentItem().text()))
        self.current_yeast=None
        self.model.remove_yeast(str(yeastT.name))
        self.add_button.hide()
        self.cancel_button.hide()        
    
    def edit(self):
        self.set_editable()
        self.set_editable_style()
        self.add_button.hide()
        self.cancel_button.show()
        self.update_button.show() 
        self.edit_button.hide()
        self.delete_button.hide()
        self.new_button.hide()  
        
    def explain_attenuation(self):
        message ='''
        What we are speaking of here is apparent attenuation.
         Apparent attenuation percentage is the percentage of
         sugars that yeast consume.   Attenuation varies between
        different strains.  The fermentation conditions and 
        gravity of a particular beer will cause the attenuation 
        to vary, hence each strain of brewers yeast has a 
        characteristic attenuation range.  The range for brewers
         yeast is typically:
         Low   : 65 - 70%
         Medium: 70 - 75%
         High:   75 - 80%
         It is calculated as ([OG-FG]-1) / (OG-1)
         example : ([1.040 -1.010]-1)/(1.040 -1)=
                   (.030) /(.040) = 75%
        '''    
        self.util.alerte(message,QMessageBox.Information,self.tr('Info : What is attenuation?'))   
     
     
    def init_dialog_and_connections(self):
        #make the controls on the form active
        self.yeast_list_widget.currentItemChanged.connect(self.selection_changed) 
        self.add_button.clicked.connect(self.save_yeast)
        self.update_button.clicked.connect(self.update_yeast)
        self.cancel_button.clicked.connect(self.cancel)
        self.attenuation_help_button.clicked.connect(self.explain_attenuation)
        self.edit_button.clicked.connect(self.edit)
        self.new_button.clicked.connect(self.new)
        self.delete_button.clicked.connect(self.delete_yeast)
        self.close_button.clicked.connect(self.close)    
        
    
    def load_selected(self):
        #load the selected yeast
        #using hasattr allows the addition of new properties during development
        self.clear_edits()
        if self.yeast_list_widget.currentItem():
            yeastT=self.model.get_yeast(str(self.yeast_list_widget.currentItem().text()))
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
                idx=self.form_combo.findText(yeastT.form)  
                self.form_combo.setCurrentIndex(idx) 
            
            if hasattr(yeastT,'attenuation'):
                idx=self.attenuation_combo.findText(yeastT.attenuation)  
                self.attenuation_combo.setCurrentIndex(idx) 
                
            if hasattr(yeastT,'floculation'):
                idx=self.floculation_combo.findText(yeastT.floculation)  
                self.floculation_combo.setCurrentIndex(idx)  
                        
        self.set_read_only()  
        self.set_read_only_style() 
        
            
    def new(self):
        #the user has asked for creation of a new yeast record
        self.update_button.hide()
        self.yeast_list_widget.clear()
        self.set_editable()
        self.set_editable_style()
        self.clear_edits()
        self.cancel_button.show()
        self.add_button.show() 
        self.edit_button.hide()
        self.delete_button.hide()
        self.new_button.hide()
                
    
    def on_model_has_changed_yeast(self,target):
        if target == 'yeast':
            self.yeast_key_list=self.model.yeast_list   
            self.refresh_yeast_list_widget()
            
         
    def read_input(self):
        #read the inputs of the dialog to new a yeast object
        name=self.util.check_input(self.name_edit,True,self.tr('Name'),False)
        if not name: return
        
        maker=self.util.check_input(self.maker_edit,True,self.tr('Maker'),False)
        if not maker: return
        
        max_allowed_temperature = self.util.check_input(self.max_allowed_temperature_edit,False,self.tr('Maximum Allowed Temperature'),False,0,35)
        if not max_allowed_temperature: return
        
        min_allowed_temperature = self.util.check_input(self.min_allowed_temperature_edit,False,self.tr('Minimum Allowed Temperature'),False,0,35)
        if not min_allowed_temperature: return
        
        max_advised_temperature = self.util.check_input(self.max_advised_temperature_edit,False,self.tr('Maximum Advised Temperature'),False,0,35)
        if not max_advised_temperature: return
        
        min_advised_temperature = self.util.check_input(self.min_advised_temperature_edit,False,self.tr('Minimum Advised Temperature'),False,0,35)
        if not min_advised_temperature: return
        
        form = self.util.check_input(self.form_combo,True,self.tr('Form'),False)
        if not form: return
        
        attenuation = self.util.check_input(self.attenuation_combo,True,self.tr('Attenuation'),False)
        if not attenuation: return
        
        floculation = self.util.check_input(self.floculation_combo,True,self.tr('Floculation'),False)
        if not attenuation: return
        
        return Yeast(name,maker,max_allowed_temperature,min_allowed_temperature,max_advised_temperature,min_advised_temperature,form,attenuation,floculation)
    
  
    def refresh_yeast_list_widget(self):   
        self.edit_button.hide()          
        self.delete_button.hide()        
        self.yeast_list_widget.clear()       
        self.yeast_key_list.sort()  
        for key in self.yeast_key_list:
            self.yeast_list_widget.addItem(key)    
        if self.current_yeast:
            item=self.yeast_list_widget.findItems(self.current_yeast,QtCore.Qt.MatchExactly)
            self.yeast_list_widget.setCurrentItem(item[0]) 
        else:
            self.clear_edits()        
        self.set_read_only()   
       
     
    def save_yeast(self):
        'ask the model to save or update the yeast that is defined by the GUI'
        'then set all inputs readonly'
        yeastT=self.read_input()
        self.current_yeast=yeastT.name # in order to be able to select it back on refresh
        self.model.save_yeast(yeastT)
        self.set_read_only()
        self.set_read_only_style()
        self.add_button.hide()
         
    def selection_changed(self):
        self.add_button.hide()
        self.update_button.hide()
        self.cancel_button.hide()
        self.load_selected()
        self.edit_button.show()
        self.delete_button.show()
        self.new_button.show()
     
    def set_editable(self):
        self.name_edit.setReadOnly(False)
        self.maker_edit.setReadOnly(False)
        self.max_allowed_temperature_edit.setReadOnly(False)
        self.min_allowed_temperature_edit.setReadOnly(False)
        self.max_advised_temperature_edit.setReadOnly(False)
        self.min_advised_temperature_edit.setReadOnly(False)
        self.form_combo.setEnabled(True)
        self.attenuation_combo.setEnabled(True)
        self.floculation_combo.setEnabled(True)
        self.set_editable_style()
                
            
    def set_editable_style(self):
        self.name_edit.setStyleSheet(sty.field_styles['editable']) 
        self.maker_edit.setStyleSheet(sty.field_styles['editable'])
        self.max_allowed_temperature_edit.setStyleSheet(sty.field_styles['editable'])
        self.min_allowed_temperature_edit.setStyleSheet(sty.field_styles['editable'])
        self.max_advised_temperature_edit.setStyleSheet(sty.field_styles['editable'])
        self.min_advised_temperature_edit.setStyleSheet(sty.field_styles['editable']) 
        self.form_combo.setStyleSheet(sty.field_styles['editable'])
        self.attenuation_combo.setStyleSheet(sty.field_styles['editable'])
        self.floculation_combo.setStyleSheet(sty.field_styles['editable'])

    def set_read_only(self):
        self.name_edit.setReadOnly(True)
        self.maker_edit.setReadOnly(True)
        self.max_allowed_temperature_edit.setReadOnly(True)
        self.min_allowed_temperature_edit.setReadOnly(True)
        self.max_advised_temperature_edit.setReadOnly(True)
        self.min_advised_temperature_edit.setReadOnly(True)
        self.form_combo.setEnabled(False)
        self.attenuation_combo.setEnabled(False)
        self.floculation_combo.setEnabled(False)
        self.set_read_only_style()  
              

    def set_read_only_style(self):
        self.name_edit.setStyleSheet(sty.field_styles['read_only']) 
        self.maker_edit.setStyleSheet(sty.field_styles['read_only']) 
        self.max_allowed_temperature_edit.setStyleSheet(sty.field_styles['read_only'])
        self.min_allowed_temperature_edit.setStyleSheet(sty.field_styles['read_only'])
        self.max_advised_temperature_edit.setStyleSheet(sty.field_styles['read_only'])
        self.min_advised_temperature_edit.setStyleSheet(sty.field_styles['read_only'])
        self.form_combo.setStyleSheet(sty.field_styles['read_only'])
        self.attenuation_combo.setStyleSheet(sty.field_styles['read_only'])
        self.floculation_combo.setStyleSheet(sty.field_styles['read_only'])
    
        
     
    def showEvent(self,ev):
        #must wait for the dialog to be created in order to do this stuff
        self.set_translatable_textes()
        self.yeast_attenuation_list=['',self.tr('Low'),self.tr('Medium'),self.tr('High')]
        self.yeast_form_list=['',self.tr('Dry'),self.tr('Liquid')]
        for f in self.yeast_form_list:
            self.form_combo.addItem(f)
        for a in self.yeast_attenuation_list:
            self.attenuation_combo.addItem(a)   
        for f in self.yeast_attenuation_list:#list is common to attenuation and floculation
            self.floculation_combo.addItem(f) 
        
            
        
    def update_yeast(self):
        'ask the model to save or update the yeast that is defined by the GUI'
        'then set all inputs readonly'
        yeastT=self.read_input()
        self.current_yeast=yeastT.name # in order to be able to select it back on refresh
        self.model.update_yeast(yeastT)
        self.set_read_only()
        self.set_read_only_style()
        self.add_button.hide()    
        
        
    
              
        
    
    def set_translatable_textes(self):
        #this is called once the dialog has been fully created (showEvent)
        self.setWindowTitle(self.tr('Yeast Database Edition'))
        self.yeast_list_label.setText(self.tr('Yeast List'))
        self.detail_label.setText(self.tr('Selected Yeast Details'))
        self.add_button.setText(self.tr('Ajouter cette levure'))
        self.name_label.setText(self.tr('Name'))
        self.maker_label.setText(self.tr('Maker'))
        self.max_allowed_temperature_label.setText(self.tr('Maximum Allowed Temperature'))
        self.min_allowed_temperature_label.setText(self.tr('Minimum Allowed Temperature'))
        self.max_advised_temperature_label.setText(self.tr('Maximum Advised Temperature'))
        self.min_advised_temperature_label.setText(self.tr('Minimum Advised Temperature'))
        self.form_label.setText(self.tr('Form'))
        self.attenuation_label.setText(self.tr('Attenuation'))
        self.floculation_label.setText(self.tr('Floculation'))
        self.close_button.setText(self.tr('Close'))
        self.edit_button.setText(self.tr('Edit'))
        self.delete_button.setText(self.tr('Delete'))
        self.new_button.setText(self.tr('New'))
        