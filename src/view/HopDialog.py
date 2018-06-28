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
from gen import HopDialogUI
from model.Hop import Hop
import view.styles as sty


#from PyQt4.QtGui import QStandardItemModel,QStandardItem,QItemSelectionModel

class HopDialog(QWidget,HopDialogUI.Ui_Form ):
    """
       class docs
    """   
    
    def __init__(self,model,controller,util):
        QWidget.__init__(self,None,QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        #print('HopDialog : creating a HopDialog object')
        self.model = model
        self.controller=controller
        self.util=util
        self.current_hop=None # the hop currently selected
        ' register function with model for future model update announcements'
        self.model.subscribe_model_changed(['hop'],self.on_model_changed_hop) 
        self.add_button.hide()
        self.update_button.hide()
        self.cancel_button.hide()
        self.set_read_only()
        self.init_dialog_and_connections()         
        self.hop_key_list=self.model.hop_list             
        self.refresh_hop_list_widget()     
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
        self.current_hop=None
        self.selection_changed()  
        self.refresh_hop_list_widget()   
        'as selection_changed shows them'
        self.edit_button.hide()
        self.delete_button.hide()
        self.new_button.show()
        
                
    def clear_edits(self):
        self.name_edit.setText('')  
        self.alpha_acid_edit.setText('')
        idx =self.form_list.findText('')
        self.form_list.setCurrentIndex(idx)
        
        
    def closeEvent(self,event):
        self.close()        
    
    
    def delete_hop(self):
        hopT=self.model.get_hop(self.hop_list_widget.currentItem().text())
        self.current_hop=None
        self.model.remove_hop(hopT.name)
        
    
        
    def edit(self):
        self.set_editable()
        self.set_editable_style()
        self.update_button.show() 
        self.cancel_button.show()
        self.edit_button.hide()
        self.delete_button.hide()
        self.new_button.hide()
        
        
    def init_dialog_and_connections(self):
        self.hop_list_widget.currentItemChanged.connect(self.selection_changed) 
        self.add_button.clicked.connect(self.save_hop)
        self.update_button.clicked.connect(self.update_hop)
        self.cancel_button.clicked.connect(self.cancel)
        self.edit_button.clicked.connect(self.edit)
        self.new_button.clicked.connect(self.new)
        self.delete_button.clicked.connect(self.delete_hop)
        self.close_button.clicked.connect(self.close)
    
    
    def load_selected(self):
        self.clear_edits()
        if self.hop_list_widget.currentItem():
            hopT=self.model.get_hop(str(self.hop_list_widget.currentItem().text()))
            if hasattr(hopT,'name'):
                self.name_edit.setText(hopT.name)
            if hasattr(hopT,'alpha_acid'):    
                self.alpha_acid_edit.setText(str(hopT.alpha_acid))
            if hasattr(hopT,'form'):    
                idx=self.form_list.findText(hopT.form)
                self.form_list.setCurrentIndex(idx)
        self.set_read_only()  
        self.set_read_only_style()  
     
     
    def new(self):
        self.update_button.hide()
        self.hop_list_widget.clear()
        self.set_editable()
        self.set_editable_style()
        self.clear_edits()
        self.add_button.show() 
        self.cancel_button.show()
        self.edit_button.hide()
        self.delete_button.hide()
        self.new_button.hide() 
          
        
    def on_model_changed_hop(self,target):
        '''
        This function is called by the model when it changes
        due to the fact that it is subscribed as callback
        on initialization
        '''
        if target == 'hop':
            self.hop_key_list=self.model.hop_list 
            self.refresh_hop_list_widget()   
            
    def read_input(self):
        name=self.util.check_input(self.name_edit,True,self.tr('Name'),False)
        if not name: return
        alpha_acid = self.util.check_input(self.alpha_acid_edit,False,self.tr('Alpha Acids'),False,0,100)
        if not alpha_acid: return
        form=self.util.check_input(self.form_list,True,self.tr('Form'),False)
        if not form: return
        return Hop(name,alpha_acid,form)          
           
        
    def refresh_hop_list_widget(self): 
        self.edit_button.hide() 
        self.delete_button.hide()         
        self.hop_list_widget.clear()       
        self.hop_key_list.sort()  
        for key in self.hop_key_list:
            self.hop_list_widget.addItem(key)        
        if self.current_hop:
            item=self.hop_list_widget.findItems(self.current_hop,QtCore.Qt.MatchExactly)
            self.hop_list_widget.setCurrentItem(item[0]) 
        else:
            self.clear_edits()          
        self.set_read_only()      
     
    
    def save_hop(self):
        'add the hop that is defined by the GUI'
        hopT=self.read_input()
        if not hopT: return
        self.current_hop=hopT.name # in order to be able to select it back on refresh
        self.model.save_hop(hopT)
        self.set_read_only()
        self.set_read_only_style()
        self.add_button.hide()
        
         
    def set_editable(self):
        self.name_edit.setReadOnly(False)
        self.alpha_acid_edit.setReadOnly(False)
        self.form_list.setEditable(False)
        self.form_list.setEnabled(True)
        self.set_editable_style()
                
            
    def set_editable_style(self):
        self.name_edit.setStyleSheet(sty.field_styles['editable']) 
        self.alpha_acid_edit.setStyleSheet(sty.field_styles['editable']) 
        self.form_list.setStyleSheet(sty.field_styles['editable'])
        

    def set_read_only_style(self):
        self.name_edit.setStyleSheet(sty.field_styles['read_only']) 
        self.alpha_acid_edit.setStyleSheet(sty.field_styles['read_only']) 
        self.form_list.setStyleSheet(sty.field_styles['read_only'])
          
           
    def set_read_only(self):
        self.name_edit.setReadOnly(True)
        self.alpha_acid_edit.setReadOnly(True)
        self.form_list.setEditable(False)
        self.form_list.setEnabled(False)
        self.set_read_only_style()
        

    def selection_changed(self):
        print('HopDialog : selection changed')
        self.add_button.hide()
        self.update_button.hide()
        self.cancel_button.hide()
        self.load_selected()
        self.edit_button.show()
        self.delete_button.show()
        self.new_button.show()
        
    def set_translatable_textes(self):
        self.setWindowTitle(self.tr('Hop Database Edition'))
        self.list_label.setText(self.tr('Hop List'))
        self.detail_label.setText(self.tr('Selected Hop Details'))
        self.add_button.setText(self.tr('Add this hop'))
        self.cancel_button.setText(self.tr('Cancel'))
        self.update_button.setText(self.tr('Update this hop'))
        self.name_label.setText(self.tr('Name'))
        self.alpha_acid_label.setText(self.tr('Alpha Acids'))
        self.form_label.setText(self.tr('Form'))
        self.close_button.setText(self.tr('Close'))
        self.edit_button.setText(self.tr('Edit'))
        self.delete_button.setText(self.tr('Delete'))
        self.new_button.setText(self.tr('New'))
        
        
    def showEvent(self,ev):
        self.set_translatable_textes()
        self.hop_form_list=['',self.tr('Pellets'),self.tr('Leaves'),self.tr('Cones')]    
        for f in self.hop_form_list:
            self.form_list.addItem(f)    
        
        
    def update_hop(self):
        print('updating hop')
        hopT=self.read_input()
        if not hopT:return
        self.current_hop=hopT.name # in order to be able to select it back on refresh
        self.model.update_hop(hopT)
        self.set_read_only()
        self.set_read_only_style()
        self.update_button.hide() 
        self.cancel_button.hide()   
        self.selection_changed()  
        