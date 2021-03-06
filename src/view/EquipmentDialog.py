# -*- coding: utf-8 -*-­

#MaMousse
#Copyright (C) 2017 José FOURNIER

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

from gen import EquipmentDialogUI

from model.Equipment import Equipment

import view.styles as sty
import view.constants as vcst
import platform

class EquipmentDialog(QWidget,EquipmentDialogUI.Ui_Form ):
   
    def __init__(self,model,controller,util):
        QWidget.__init__(self)
        self.setupUi(self)
        self.model = model
        self.controller=controller
        self.util=util
        self.current_equipment=None
        
        self.add_button.hide()
        self.update_button.hide()
        self.cancel_button.hide()
        self.set_ro()

        #get the list of malts from db and load into the malt_list widget
        self.equipment_key_list=self.model.equipment_list
           
        for key in self.equipment_key_list:
            self.equipment_list_widget.addItem(key)
        self.model.subscribe_model_changed(['equipment','fontset'],self.on_model_changed_equipment)
        self.init_dialog_and_connections()
    
        
    
    def add_equipment(self):
        equipment=self.read_input()
        #read imput has been avorted due to non documented value
        if not equipment: return
        if not self.name_edit.text(): 
            self.alerte(self.tr('Short name cannot be empty'))
            return
        
        self.model.add_equipment(equipment)
        self.current_equipment=equipment.name
        
              
        self.refresh_equipment_list_widget()
        item=self.equipment_list_widget.findItems(equipment.name,QtCore.Qt.MatchExactly)
        self.equipment_list_widget.setCurrentItem(item[0])     
        self.set_ro()
        self.unset_color()
        self.add_button.hide()
        self.cancel_button.hide()
        
    def update_equipment(self):
        'save or update the malt that is defined by the GUI'
        
        equipment=self.read_input()
        if not equipment: return
        self.current_equipment=equipment.name # in order to be able to select it back on refresh
        self.model.update_equipment(equipment)
        self.set_ro()
        self.unset_color()
        self.update_button.hide()
        self.cancel_button.hide()    
        
    def alerte(self,texte):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(texte)
        msg.setWindowTitle(self.tr("Warning Text"))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()    
        
        
    def all_in_one_type_radiobutton_toggled(self):
        if self.all_in_one_type_radiobutton.isChecked():
            self.mash_tun_size_label.hide()
            self.mash_tun_size_unit_label.hide()
            self.mash_tun_size_edit.hide()
            
            self.mash_tun_heat_losses_unit_label.hide()
            self.mash_tun_heat_losses_label.hide()
            self.mash_tun_heat_losses_edit.hide()
            
            self.mash_tun_dead_space_label.hide()
            self.mash_tun_dead_space_unit_label.hide()
            self.mash_tun_dead_space_edit.hide()
              
            self.mash_tun_groupbox.hide()
            self.set_fonts()
            
    def basic_type_radiobutton_toggled(self):
        if self.basic_type_radiobutton.isChecked():
            self.mash_tun_groupbox.show()
            self.mash_tun_size_label.show()
            self.mash_tun_size_unit_label.show()
            self.mash_tun_size_edit.show()
            
            self.mash_tun_heat_losses_unit_label.show()
            self.mash_tun_heat_losses_label.show()
            self.mash_tun_heat_losses_edit.show()
                       
            self.mash_tun_dead_space_label.show()
            self.mash_tun_dead_space_unit_label.show()
            self.mash_tun_dead_space_edit.show()
            
            #clean the value not to forgot entering them anew
            self.mash_tun_size_edit.setText('')
            self.mash_tun_dead_space_edit.setText('')
            self.mash_tun_heat_losses_edit.setText('')    
            self.set_fonts()
                                                                     
    def cancel(self):
        'after canceling an update or a creation'  
        self.selection_changed()  
        self.refresh_equipment_list_widget()
        'because selection_changed show them'
        self.edit_button.hide()
        self.delete_button.hide()
        self.new_button.show() 
        
                        
    def clear_edits(self):
        self.name_edit.setText('') 
        self.basic_type_radiobutton.setChecked(True)
        self.mash_tun_size_edit.setText('')
        self.mash_tun_dead_space_edit.setText('')
        self.mash_tun_heat_losses_edit.setText('')
        self.brewing_efficiency_edit.setText('')
        self.boiler_size_edit.setText('')
        self.boiler_dead_space_edit.setText('')
        self.boiler_evaporation_rate_edit.setText('')
        self.fermentor_size_edit.setText('')
        self.fermentor_dead_space_edit.setText('')
      
      
    def closeEvent(self,event):
        self.close()
        
    def delete_equipment(self):
        equipment=self.model.get_equipment(self.equipment_list_widget.currentItem().text())
        self.current_equipment=None#avoid selection after update
        self.model.remove_equipment(equipment.name)
        self.refresh_equipment_list_widget()         
        
    def edit_equipment(self):
        self.add_button.hide()
        self.cancel_button.show()
        self.update_button.show()
        self.unset_ro()
        self.set_color()
        self.edit_button.hide()
        self.delete_button.hide()
        self.new_button.hide()   
        
    def on_model_changed_equipment(self,target):
        '''
        This function is called by the model when it changes
        due to the fact that it is subscribed as callback
        on initialization
        '''
        if target == 'equipment':
            self.equipment_key_list=self.model.equipment_list 
            self.refresh_equipment_list_widget() 
            self.set_ro()
            self.unset_color() 
                
        'we must wait for fonts to be initialized in model'    
        if target == 'fontset':
            if (self.model.in_use_fonts):
                self.set_fonts()    
                    
    def explain_type(self):
        txt=self.tr('''
        A basic type equipment, is an equipment with a mash tun separate from the boiler.
        In an all in one equipment the mash tun is the same as the boiler. It means, that 
        it is the grain, and not the wort, that is removed from the tun after the mash.
        Examples, of all in one equipment are GrainFather, Robobrew, etc.
        Dead space in a tun is the part that is below the tap and cannot be drained out. 
        ''')
        msg = QMessageBox()   
        msg.setIcon(QMessageBox.Warning)
        msg.setText(txt)
        msg.setWindowTitle(self.tr("Warning Bad Input: "))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    
    
    def init_dialog_and_connections(self):
        self.add_button.clicked.connect(self.add_equipment)
        self.type_ask_button.clicked.connect(self.explain_type)
        self.edit_button.clicked.connect(self.edit_equipment)
        self.new_button.clicked.connect(self.new_equipment)
        self.delete_button.clicked.connect(self.delete_equipment)
        self.close_button.clicked.connect(self.close)
        self.basic_type_radiobutton.toggled.connect(self.basic_type_radiobutton_toggled)
        self.all_in_one_type_radiobutton.toggled.connect(self.all_in_one_type_radiobutton_toggled) 
        self.equipment_list_widget.currentItemChanged.connect(self.selection_changed) 
        self.cancel_button.clicked.connect(self.cancel)  
        self.update_button.clicked.connect(self.update_equipment)        

    def load_selected(self):
        v_unit=self.model.get_unit('water_volume')
        if not v_unit:
            return
        t_unit=self.model.get_unit('temperature')
        delta_t_unit=self.model.get_unit('delta_temperature')
        if self.equipment_list_widget.currentItem():
            equipment=self.model.get_equipment(str(self.equipment_list_widget.currentItem().text()))           
            self.clear_edits()
            self.set_ro()      
            self.name_edit.setText(equipment.name) 
            if hasattr(equipment, 'brewing_efficiency'):
                self.brewing_efficiency_edit.setText(str(equipment.brewing_efficiency))
            if hasattr(equipment,'type'):    
                if equipment.type ==0:
                    self.basic_type_radiobutton.setChecked(True)
                    self.basic_type_radiobutton_toggled()
                elif equipment.type==1:
                    self.all_in_one_type_radiobutton.setChecked(True) 
                    self.all_in_one_type_radiobutton_toggled() 
            if hasattr(equipment,'mash_tun_size') and equipment.mash_tun_size:
                self.mash_tun_size_edit.setText(str(self.util.convert_to(v_unit,equipment.mash_tun_size)))    
            if hasattr(equipment,'mash_tun_dead_space') and equipment.mash_tun_dead_space:
                self.mash_tun_dead_space_edit.setText(str(self.util.convert_to(v_unit,equipment.mash_tun_dead_space))) 
            if hasattr(equipment,'mash_tun_heat_losses') and equipment.mash_tun_heat_losses:
                'as heat losses are always calculates per hour, the ratio is the same as the ratio between °C and °F'
                self.mash_tun_heat_losses_edit.setText(str(self.util.convert_to(delta_t_unit,equipment.mash_tun_heat_losses)) )  
            if hasattr(equipment,'boiler_size'):                
                self.boiler_size_edit.setText(str(self.util.convert_to(v_unit,equipment.boiler_size)))
            if hasattr(equipment,'boiler_dead_space'):    
                self.boiler_dead_space_edit.setText(str(self.util.convert_to(v_unit,equipment.boiler_dead_space)))
            if hasattr(equipment,'boiler_evaporation_rate'):
                'as evaporation  is always calculated per hour, the ratio is the same as the ratio between °C and °F'
                self.boiler_evaporation_rate_edit.setText(str(self.util.convert_to(v_unit,equipment.boiler_evaporation_rate)))    
            if hasattr(equipment,'fermentor_size'):    
                self.fermentor_size_edit.setText(str(self.util.convert_to(v_unit,equipment.fermentor_size)))
            if hasattr(equipment,'fermentor_dead_space'):
                self.fermentor_dead_space_edit.setText(str(self.util.convert_to(v_unit,equipment.fermentor_dead_space)))
            self.set_ro()
        else:#there is no selection
            self.clear_edits()    
            
                       
    def new_equipment(self):
        self.update_button.hide()
        self.unset_ro()
        self.clear_edits() 
        self.equipment_list_widget.clear() 
        self.cancel_button.show()
        self.add_button.show()
        self.edit_button.hide()
        self.delete_button.hide()
        self.new_button.hide()      
      
            
    def read_input(self):
        typ=None
        mash_tun_size=None
        mash_tun_dead_space=None 
        mash_tun_heat_losses=None  
        v_unit=self.model.get_unit('water_volume')
        t_unit=self.model.get_unit('temperature')
        delta_t_unit=self.model.get_unit('delta_temperature')
    
        name = self.util.check_input(self.name_edit,True, self.tr('Name'),False)
        if not name: return
        brewing_efficiency = self.util.check_input(self.brewing_efficiency_edit,False,self.tr('Brewing Efficiency'),False,0,100)
        if not brewing_efficiency: return
        boiler_size = self.util.check_input(self.boiler_size_edit,False, self.tr('Boiler Size'),False,0,vcst.MAX_MASH_TUN_SIZE,None,v_unit)
        if not boiler_size: return
        boiler_dead_space = self.util.check_input(self.boiler_dead_space_edit,False, self.tr('Boiler Dead Space'),False,0,vcst.MAX_MASH_TUN_SIZE,None,v_unit)
        if not boiler_dead_space: return  
        'as evaporation  is always calculated per hour, the ratio is the same as the ratio between °C and °F'
        boiler_evaporation_rate = self.util.check_input(self.boiler_evaporation_rate_edit,False,self.tr('Boiler Evaporation Rate'),False,0,20,None,v_unit)
        if not boiler_evaporation_rate: return
        fermentor_size = self.util.check_input(self.fermentor_size_edit,False, self.tr('Fermentor Size'),False,0,vcst.MAX_MASH_TUN_SIZE,None,v_unit)
        if not fermentor_size: return 
        fermentor_dead_space = self.util.check_input(self.fermentor_dead_space_edit,False, self.tr('Boiler Size'),False,0,vcst.MAX_MASH_TUN_SIZE,None,v_unit)
        if not fermentor_dead_space: return
        
        if self.basic_type_radiobutton.isChecked():
            typ=0
        elif self.all_in_one_type_radiobutton.isChecked():
            typ=1 
        else:
            typ=0   
        try:               
            if typ==0:
                mash_tun_size = self.util.check_input(self.mash_tun_size_edit,False,self.tr('Mash Tun Size'),False,0,vcst.MAX_MASH_TUN_SIZE,None,v_unit)
                if not mash_tun_size: return
                mash_tun_dead_space = self.util.check_input(self.mash_tun_dead_space_edit,\
                    False, self.tr('Mash Tun Dead Space'), False,0,vcst.MAX_MASH_TUN_SIZE/10,None,v_unit)
                if not mash_tun_dead_space: return
                'as heat losses are always calculates per hour, the ratio is the same as the ratio between °C and °F'
                mash_tun_heat_losses = self.util.check_input(self.mash_tun_heat_losses_edit,\
                    False,self.tr('Mash Tun Heat Losses'),False,0,vcst.MAX_MASH_TUN_HEAT_LOSSES,None,delta_t_unit)
                if not mash_tun_heat_losses: return
                
            elif typ==1:
                mash_tun_size=None
                mash_tun_dead_space=None 
                mash_tun_heat_losses=None     
                 
           
            equipment=Equipment(name,brewing_efficiency,boiler_size,boiler_dead_space, boiler_evaporation_rate,\
                                fermentor_size,fermentor_dead_space,typ,mash_tun_size,mash_tun_dead_space,mash_tun_heat_losses)
            
            self.add_button.hide()
                
            return (equipment)  
        except ValueError:
            self.alerte(self.tr('Could not read inputs. Please check all input values are correct'))  
    
        
    def refresh_equipment_list_widget(self):
        self.edit_button.hide()          
        self.delete_button.hide()
        self.equipment_list_widget.clear()
        for key in self.equipment_key_list:
            self.equipment_list_widget.addItem(key)

        if self.current_equipment:
            item=self.equipment_list_widget.findItems(self.current_equipment,QtCore.Qt.MatchExactly)
            self.equipment_list_widget.setCurrentItem(item[0]) 
                   
            
    def selection_changed(self):
        self.add_button.hide()
        self.update_button.hide()
        self.cancel_button.hide()
        self.load_selected()
        self.edit_button.show()
        self.delete_button.show()
            
    def set_color(self):
        self.name_edit.setStyleSheet(sty.field_styles['editable']) 
        self.brewing_efficiency_edit.setStyleSheet(sty.field_styles['editable']) 
        self.mash_tun_size_edit.setStyleSheet(sty.field_styles['editable'])
        self.mash_tun_dead_space_edit.setStyleSheet(sty.field_styles['editable'])
        self.mash_tun_heat_losses_edit.setStyleSheet(sty.field_styles['editable'])
        self.boiler_size_edit.setStyleSheet(sty.field_styles['editable']) 
        self.boiler_dead_space_edit.setStyleSheet(sty.field_styles['editable'])
        self.boiler_evaporation_rate_edit.setStyleSheet(sty.field_styles['editable'])
        self.fermentor_size_edit.setStyleSheet(sty.field_styles['editable']) 
        self.fermentor_dead_space_edit.setStyleSheet(sty.field_styles['editable']) 
        

        
    def set_fonts(self):
        self.add_button.setStyleSheet('background-color:lightgreen;')
        self.update_button.setStyleSheet('background-color:lightgreen;')
        self.cancel_button.setStyleSheet('background-color:pink;')  
       
        self.add_button.setFont(self.model.in_use_fonts['button'])
        self.update_button.setFont(self.model.in_use_fonts['button'])
        self.cancel_button.setFont(self.model.in_use_fonts['button'])
        self.edit_button.setFont(self.model.in_use_fonts['button'])
        self.delete_button.setFont(self.model.in_use_fonts['button'])
        self.new_button.setFont(self.model.in_use_fonts['button'])
        self.close_button.setFont(self.model.in_use_fonts['button'])
        self.equipment_list_label.setFont(self.model.in_use_fonts['title_slanted'])
        self.equipment_properties_label.setFont(self.model.in_use_fonts['title_slanted'])
        self.type_guidance_label.setFont(self.model.in_use_fonts['title_slanted'])
        self.basic_type_radiobutton.setFont(self.model.in_use_fonts['field'])
        self.all_in_one_type_radiobutton.setFont(self.model.in_use_fonts['field'])
        self.brewing_efficiency_label.setFont(self.model.in_use_fonts['field'])
        self.brewing_efficiency_edit.setFont(self.model.in_use_fonts['field'])
        self.brewing_efficiency_unit_label.setFont(self.model.in_use_fonts['field'])
        self.mash_tun_size_label.setFont(self.model.in_use_fonts['field'])
        self.mash_tun_size_unit_label.setFont(self.model.in_use_fonts['field'])
        self.mash_tun_size_edit.setFont(self.model.in_use_fonts['field'])
        self.mash_tun_dead_space_label.setFont(self.model.in_use_fonts['field'])
        self.mash_tun_dead_space_unit_label.setFont(self.model.in_use_fonts['field'])
        self.mash_tun_dead_space_edit.setFont(self.model.in_use_fonts['field'])
        self.mash_tun_heat_losses_label.setFont(self.model.in_use_fonts['field'])
        self.mash_tun_heat_losses_unit_label.setFont(self.model.in_use_fonts['field'])
        self.mash_tun_heat_losses_edit.setFont(self.model.in_use_fonts['field'])
        self.boiler_size_label.setFont(self.model.in_use_fonts['field'])
        self.boiler_size_unit_label.setFont(self.model.in_use_fonts['field'])
        self.boiler_size_edit.setFont(self.model.in_use_fonts['field'])
        self.boiler_dead_space_label.setFont(self.model.in_use_fonts['field'])
        self.boiler_dead_space_unit_label.setFont(self.model.in_use_fonts['field'])
        self.boiler_dead_space_edit.setFont(self.model.in_use_fonts['field'])
        self.boiler_evaporation_rate_edit.setFont(self.model.in_use_fonts['field'])
        self.boiler_evaporation_rate_label.setFont(self.model.in_use_fonts['field'])
        self.boiler_evaporation_rate_unit_label.setFont(self.model.in_use_fonts['field'])
        self.fermentor_size_label.setFont(self.model.in_use_fonts['field'])
        self.fermentor_size_unit_label.setFont(self.model.in_use_fonts['field'])
        self.fermentor_size_edit.setFont(self.model.in_use_fonts['field'])
        self.fermentor_dead_space_label.setFont(self.model.in_use_fonts['field'])
        self.fermentor_dead_space_unit_label.setFont(self.model.in_use_fonts['field'])
        self.fermentor_dead_space_edit.setFont(self.model.in_use_fonts['field'])
        self.name_label.setFont(self.model.in_use_fonts['field'])
        self.mash_tun_groupbox.setFont(self.model.in_use_fonts['title_slanted'])
        self.boiler_groupbox.setFont(self.model.in_use_fonts['title_slanted'])
        self.fermentor_groupbox.setFont(self.model.in_use_fonts['title_slanted'])
        self.general_groupbox.setFont(self.model.in_use_fonts['title_slanted'])
        self.equipment_list_widget.setFont(self.model.in_use_fonts['field'])
            
        
    def set_ro(self):
        self.basic_type_radiobutton.setEnabled(False)
        self.all_in_one_type_radiobutton.setEnabled(False)
        self.name_edit.setReadOnly(True)
        self.brewing_efficiency_edit.setReadOnly(True)
        self.mash_tun_size_edit.setReadOnly(True)
        self.mash_tun_dead_space_edit.setReadOnly(True)
        self.mash_tun_heat_losses_edit.setReadOnly(True) 
        self.boiler_size_edit.setReadOnly(True)
        self.boiler_dead_space_edit.setReadOnly(True)
        self.boiler_evaporation_rate_edit.setReadOnly(True)
        self.fermentor_size_edit.setReadOnly(True)
        self.fermentor_dead_space_edit.setReadOnly(True)
        self.unset_color()
        
        
    def showEvent(self,ev):
        #self.set_labels()    
        self.set_fonts()
        #self.set_unit_labels()
        
        
    def unset_color(self):
        self.name_edit.setStyleSheet(sty.field_styles['read_only'])
        self.brewing_efficiency_edit.setStyleSheet(sty.field_styles['read_only']) 
        self.mash_tun_size_edit.setStyleSheet(sty.field_styles['read_only'])
        self.mash_tun_dead_space_edit.setStyleSheet(sty.field_styles['read_only'])
        self.mash_tun_heat_losses_edit.setStyleSheet(sty.field_styles['read_only'])
        self.boiler_size_edit.setStyleSheet(sty.field_styles['read_only']) 
        self.boiler_dead_space_edit.setStyleSheet(sty.field_styles['read_only'])
        self.boiler_evaporation_rate_edit.setStyleSheet(sty.field_styles['read_only'])
        self.fermentor_size_edit.setStyleSheet(sty.field_styles['read_only']) 
        self.fermentor_dead_space_edit.setStyleSheet(sty.field_styles['read_only']) 
                   
        
    def unset_ro(self):
        self.basic_type_radiobutton.setEnabled(True)
        self.all_in_one_type_radiobutton.setEnabled(True)
        self.name_edit.setReadOnly(False)
        self.brewing_efficiency_edit.setReadOnly(False) 
        self.mash_tun_size_edit.setReadOnly(False)
        self.mash_tun_dead_space_edit.setReadOnly(False)
        self.mash_tun_heat_losses_edit.setReadOnly(False) 
        self.boiler_size_edit.setReadOnly(False) 
        self.boiler_dead_space_edit.setReadOnly(False)
        self.boiler_evaporation_rate_edit.setReadOnly(False)
        self.fermentor_size_edit.setReadOnly(False)
        self.fermentor_dead_space_edit.setReadOnly(False)
        self.set_color()
                 