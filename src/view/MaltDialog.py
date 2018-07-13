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
from PyQt5.QtWidgets import QWidget,QMessageBox
from gen import MaltDialogUI
from model.Malt import Malt
import view.constants as vcst
import view.styles as sty

class MaltDialog(QWidget,MaltDialogUI.Ui_MaltDialog ):
    """
       class docs
    """   
    def __init__(self,model,controller,util):
        QWidget.__init__(self,None,QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.model = model
        self.controller=controller
        self.util=util
        self.current_malt=None # the malt currently selected
        self.model.subscribe_model_changed(['malt','fontset'],self.on_model_changed_malt) 
        self.add_button.hide()
        self.update_button.hide()
        self.cancel_button.hide()
        self.set_read_only()
        self.init_dialog_and_connections()         
        self.malt_key_list=self.model.malt_list             
        self.refresh_malt_list_widget()  
          
        
    def cancel(self):
        'after canceling an update or a creation' 
        'to prevent reselect after cancel'
        self.current_malt=None 
        self.selection_changed()  
        self.refresh_malt_list_widget()
        'because selection_changed show them'
        self.edit_button.hide()
        self.delete_button.hide()
        self.new_button.show()    
  
    def changeEvent(self, event):
        print('changeEvent triggered')
        'the following lines are no longer required as the application restarts after a language change'
        #if event.type() == QtCore.QEvent.LanguageChange:
            #self.retranslateUi(self)
            
                    
    def clear_edits(self):
        self.name_edit.setText('')  
        self.maker_edit.setText('')
        self.max_yield_edit.setText('')
        self.color_edit.setText('')    
        self.kolbach_max.setText('')
        self.kolbach_min.setText('')
        
        
    def closeEvent(self,event):
        self.close()   
              
        
    def delete_malt(self):
        maltT=self.model.get_malt(self.malt_list_widget.currentItem().text())
        self.current_malt=None
        if self.model.is_used(maltT.name):
            self.util.alerte(self.tr('Malt')+maltT.name+self.tr('is already used by a recipe. You cannot delete it'),
                             QMessageBox.Critical,
                             self.tr('Malt Dialog : Malt Deletion Denied'))
            return
        self.model.remove_malt(maltT.name)
  
        
    def edit(self):
        self.add_button.hide()
        self.cancel_button.show()
        self.update_button.show()
        self.set_editable()
        self.set_editable_style()
        self.edit_button.hide()
        self.delete_button.hide()
        self.new_button.hide()
        
    def set_fonts(self):
        self.add_button.setStyleSheet('background-color:lightgreen;')
        self.update_button.setStyleSheet('background-color:lightgreen;')
        self.cancel_button.setStyleSheet('background-color:pink')
     
        self.add_button.setFont(self.model.in_use_fonts['button'])
        self.update_button.setFont(self.model.in_use_fonts['button'])
        self.cancel_button.setFont(self.model.in_use_fonts['button'])
        self.edit_button.setFont(self.model.in_use_fonts['button'])
        self.delete_button.setFont(self.model.in_use_fonts['button'])
        self.new_button.setFont(self.model.in_use_fonts['button'])
        self.close_button.setFont(self.model.in_use_fonts['button'])
        self.malt_list_label.setFont(self.model.in_use_fonts['title_slanted'])
        self.detail_label.setFont(self.model.in_use_fonts['title_slanted'])
        self.name_label.setFont(self.model.in_use_fonts['field'])
        self.name_edit.setFont(self.model.in_use_fonts['field'])
        
        self.maker_label.setFont(self.model.in_use_fonts['field'])
        self.maker_edit.setFont(self.model.in_use_fonts['field'])
        self.max_yield_label.setFont(self.model.in_use_fonts['field'])
        self.max_yield_edit.setFont(self.model.in_use_fonts['field'])
        self.color_label.setFont(self.model.in_use_fonts['field'])
        self.kolbach_index_label.setFont(self.model.in_use_fonts['field'])
        self.kolbach_min.setFont(self.model.in_use_fonts['field'])
        self.kolbach_max.setFont(self.model.in_use_fonts['field'])
        self.kolbach_max_label.setFont(self.model.in_use_fonts['field'])
        self.kolbach_min_label.setFont(self.model.in_use_fonts['field'])
        self.malt_list_widget.setFont(self.model.in_use_fonts['field'])
        self.color_edit.setFont(self.model.in_use_fonts['field'] )
                               
        
    def init_dialog_and_connections(self):
        self.malt_list_widget.currentItemChanged.connect(self.selection_changed) 
        self.add_button.clicked.connect(self.save_malt)
        self.update_button.clicked.connect(self.update_malt)
        self.edit_button.clicked.connect(self.edit)
        
        self.new_button.clicked.connect(self.new)
        self.delete_button.clicked.connect(self.delete_malt)
        self.close_button.clicked.connect(self.close)  
        self.cancel_button.clicked.connect(self.cancel)    
      
    
    def load_selected(self):
        self.clear_edits()
        if self.malt_list_widget.currentItem():
            maltT=self.model.get_malt(str(self.malt_list_widget.currentItem().text()))
            if hasattr(maltT,'name'):
                self.name_edit.setText(maltT.name)
            if hasattr(maltT,'maker'):
                self.maker_edit.setText(maltT.maker)
            if hasattr(maltT,'max_yield'):
                self.max_yield_edit.setText(str(maltT.max_yield))
            if hasattr(maltT,'color')  :  
                self.color_edit.setText(str(maltT.color))
            if hasattr(maltT,'kolbach_min'):
                self.kolbach_min.setText(str(maltT.kolbach_min))
            if hasattr(maltT,'kolbach_max'):
                self.kolbach_max.setText(str(maltT.kolbach_max))
        self.set_read_only()
        self.set_read_only_style()
    
    def new(self):
        self.update_button.hide()
        self.malt_list_widget.clear()
        self.clear_edits()
        self.set_editable()
        self.set_editable_style()
        self.add_button.show()
        self.cancel_button.show()
        self.edit_button.hide()
        self.delete_button.hide()
        self.new_button.hide()
            
        
    def on_model_changed_malt(self,target):
        '''
        This function is called by the model when it changes
        due to the fact that it is subscribed as callback
        on initialization
        '''
        if target == 'malt':
            self.malt_key_list=self.model.malt_list 
            self.refresh_malt_list_widget()  
            
        'we must wait for fonts to be initialized in model'    
        if target == 'fontset':
            if (self.model.in_use_fonts):
                self.set_fonts()    
            
     
    def read_input(self):
        name=self.util.check_input(self.name_edit,True,self.tr('Name'),False)
        if not name: return
        maker=self.util.check_input(self.maker_edit,True,self.tr('Maker'),False)
        if not maker: return
        max_yield=self.util.check_input(self.max_yield_edit,False,self.tr('Maximum Yield'),False,0,100)
        if not max_yield: return
        color= self.util.check_input(self.color_edit,False,self.tr('Color'),False,0,100)
        if not color: return
        kolbach_min=self.util.check_input(self.kolbach_min,False,self.tr('Kolbach Index Min'),True,0,100)
        kolbach_max=self.util.check_input(self.kolbach_max,False,self.tr('Kolbach Index Max'),True,0,100)
        return Malt(str(name),maker,max_yield,color,kolbach_min,kolbach_max)   
        
        
    def refresh_malt_list_widget(self): 
        self.edit_button.hide()          
        self.delete_button.hide()
        self.malt_list_widget.clear()       
        self.malt_key_list.sort()  
        for key in self.malt_key_list:
            self.malt_list_widget.addItem(key)         
        if self.current_malt:
            item=self.malt_list_widget.findItems(self.current_malt,QtCore.Qt.MatchExactly)
            self.malt_list_widget.setCurrentItem(item[0])         
        self.set_read_only()    
        
    def save_malt(self):
        'save the malt that is defined by the GUI into the database'
        maltT=self.read_input()
        if not maltT: return
        self.current_malt=maltT.name # in order to be able to select it back on refresh
        self.model.save_malt(maltT)
        self.set_read_only()
        self.set_read_only_style()
        self.add_button.hide()
        self.cancel_button.hide()
        
        
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
        self.color_edit.setReadOnly(False)
        self.max_yield_edit.setReadOnly(False)  
        self.kolbach_min.setReadOnly(False)
        self.kolbach_max.setReadOnly(False)
        self.set_editable_style()        
    
            
    def set_editable_style(self):
        self.name_edit.setStyleSheet(sty.field_styles['editable']) 
        self.maker_edit.setStyleSheet(sty.field_styles['editable'])
        self.max_yield_edit.setStyleSheet(sty.field_styles['editable']) 
        self.color_edit.setStyleSheet(sty.field_styles['editable']) 
        self.kolbach_min.setStyleSheet(vcst.OPTIONAL_EDITABLE_STYLE)
        self.kolbach_max.setStyleSheet(vcst.OPTIONAL_EDITABLE_STYLE)
        

    def set_read_only_style(self):
        self.name_edit.setStyleSheet(sty.field_styles['read_only']) 
        self.maker_edit.setStyleSheet(sty.field_styles['read_only'])
        self.max_yield_edit.setStyleSheet(sty.field_styles['read_only']) 
        self.color_edit.setStyleSheet(sty.field_styles['read_only'])
        self.kolbach_min.setStyleSheet(sty.field_styles['read_only'])
        self.kolbach_max.setStyleSheet(sty.field_styles['read_only'])
                       
            
    def set_read_only(self):
        self.name_edit.setReadOnly(True)
        self.maker_edit.setReadOnly(True)
        self.color_edit.setReadOnly(True)
        self.kolbach_min.setReadOnly(True)
        self.kolbach_max.setReadOnly(True)
        self.max_yield_edit.setReadOnly(True)
        self.set_read_only_style()
        
                
    def showEvent(self,e):  
        self.set_fonts()
        
     
    def update_malt(self):
        'update the malt that is defined by the GUI into the database'
        maltT=self.read_input()
        if not maltT: return
        self.current_malt=maltT.name # in order to be able to select it back on refresh
        self.model.update_malt(maltT)
        self.set_read_only()
        self.set_read_only_style()
        self.update_button.hide()
        self.cancel_button.hide()    

