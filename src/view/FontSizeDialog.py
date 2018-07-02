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

from PyQt5 import QtCore,Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,QMessageBox,QColorDialog

from gen import FontSizeDialogUI


import view.constants as vcst
from model.FontSet import FontSet
import view.styles as sty
import platform



class FontSetDialog(QWidget,FontSizeDialogUI.Ui_Form ):
    """
       class docs
    """   
    
    def __init__(self,model,controller,util):
        QWidget.__init__(self,None,QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.model = model
        self.controller=controller
        self.util=util
        #reading a model property
        self.font_set_key_list=self.model.font_set_list
        self.init_dialog_and_connections()
       # self.set_translatable_texes()
       # self.set_sample_colors()
        #self.set_fonts()
        
    def init_dialog_and_connections(self):
        self.label.setText(self.tr('Chose a font size below and see the results above'))
        self.init_combo()
        self.combo.currentIndexChanged.connect(self.on_item_changed)
        
    def init_combo(self):
        self.combo.clear()  
        self.combo.addItem('')
        self.combo.addItem('tiny')
        self.combo.addItem('small')
        self.combo.addItem('big')
        self.combo.addItem('huge')
        
    def on_item_changed(self):
        print('item changed in FontSizeDialog')  
        category=self.combo.currentText()  
        self.model.change_active_font_set(category)
        
            
            
                