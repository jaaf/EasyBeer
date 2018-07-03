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


#from PyQt4.QtGui import QStandardItemModel,QStandardItem,QItemSelectionModel

class UnitSetter(QDialog,UnitSetterUI.Ui_Dialog ):
    """
       class docs
    """   
    
    def __init__(self,model,util):
        QDialog.__init__(self,None,QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.init_combos()
        
        
    def init_combos(self):
        self.temperature_combo.addItem('Celsius degree')    
        self.temperature_combo.addItem('Farenheit degree')
        
        self.water_volume_combo.addItem('Liter')
        self.water_volume_combo.addItem('US Gallon')
        self.water_volume_combo.addItem('US Quart')
        self.water_volume_combo.addItem('US Pint')
        
        self.malt_mass_combo.addItem('Kilogram')
        self.malt_mass_combo.addItem('Pound')
        
        self.yeast_mass_combo.addItem('Gram')
        self.yeast_mass_combo.addItem('Ounce')
        
        