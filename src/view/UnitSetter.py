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
from PyQt5.QtWidgets import  QDialog, QMessageBox
from gen import UnitSetterUI
from model.Hop import Hop
import view.styles as sty
import platform
import view.constants as vcst
from model.Unit import Unit

#from PyQt4.QtGui import QStandardItemModel,QStandardItem,QItemSelectionModel

class UnitSetter(QDialog,UnitSetterUI.Ui_Dialog ):
    """
       class docs
    """   
    
    def __init__(self,model,parent=None):
        QDialog.__init__(self,None,QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        #self.unit_list=self.model.unit_list
        self.parent=parent
        self.model=model
        #self.util=util
        self.init_combos()
        self.set_connections()
        self.model.subscribe_model_changed(['unit'],self.on_model_changed)
        self.info_edit.setHtml('''
        <h2>Set your units here</h2>
        <p>After you have chosen your units here using the various combo boxes,
        use the Apply button to save your choices, or use the Cancel button to keep the
        international unit system i.e Celsius degree, kilogram, gram, and liter</p>
        <p>This dialog will not be shown again, but if you want to change your unit system afterwards,
        you will have to use the Preferences menu to ask for a new setup at next startup</p> 
        
        ''')
        
        
    def apply_default_values(self):
        self.model.update_unit(Unit('temperature','Celsius'))
        self.model.update_unit(Unit('delta_temperature','Celsius'))
        self.model.update_unit(Unit('water_volume', 'Liter'))
        self.model.update_unit(Unit('malt_mass','Kilogram'))
        self.model.update_unit(Unit('yeast_mass','Gram'))  
        self.model.update_unit(Unit('hop_rate','Gram per liter'))
        self.model.update_unit(Unit('hop_mass','Gram'))
        
        self.close()
        
    def apply_values_from_GUI(self):
        units=self.read_inputs()
        for u in units:
            self.model.update_unit(u) 
        self.parent.set_unit_labels()
        self.close()       
        
        
        
        
    def init_combos(self):
            
        self.temperature_combo.addItem('Celsius')    
        self.temperature_combo.addItem('Farenheit')
        
        
        
        self.water_volume_combo.addItem('Liter')
        self.water_volume_combo.addItem('Gallon')
        self.water_volume_combo.addItem('Quart')
        self.water_volume_combo.addItem('Pint')
        
        self.malt_mass_combo.addItem('Kilogram')
        self.malt_mass_combo.addItem('Pound')
        
        self.yeast_mass_combo.addItem('Gram')
        self.yeast_mass_combo.addItem('Ounce')
        
        self.hop_rate_combo.addItem('Gram per liter')
        self.hop_rate_combo.addItem('Gram per gallon')
        self.hop_rate_combo.addItem('Ounce per gallon')
        
        self.hop_mass_combo.addItem('Gram')
        self.hop_mass_combo.addItem('Ounce')
        
        
        
        
    def on_model_changed(self,target):
        return

        
    def read_inputs(self):
        u=[]
        temperature=self.temperature_combo.currentText() 
        u.append(Unit('temperature',temperature))
        u.append(Unit('delta_temperature',temperature))
        water_volume=self.water_volume_combo.currentText()
        u.append(Unit('water_volume',water_volume))
        malt_mass=self.malt_mass_combo.currentText()
        u.append(Unit('malt_mass',malt_mass))
        yeast_mass=self.yeast_mass_combo.currentText()
        u.append(Unit('yeast_mass',yeast_mass))
        hop_rate=self.hop_rate_combo.currentText()
        u.append(Unit('hop_rate',hop_rate))
        hop_mass=self.hop_mass_combo.currentText()
        u.append(Unit('hop_mass',hop_mass))
        u.append(Unit('yeast_rate','Billion/°P/'+water_volume))
        return u
        
    def set_connections(self):
        self.apply_button.clicked.connect(self.apply_values_from_GUI)  
        self.cancel_button.clicked.connect(self.apply_default_values)  
        
        
        
           
        
        