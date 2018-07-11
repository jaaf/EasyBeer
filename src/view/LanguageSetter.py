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

from PyQt5 import QtCore,QtGui
from PyQt5.QtWidgets import  QDialog, QMessageBox,QApplication
from gen import LanguageSetterUI
from model.Hop import Hop
import view.styles as sty
import platform
import view.constants as vcst

from model.Unit import Unit
import os

#from PyQt4.QtGui import QStandardItemModel,QStandardItem,QItemSelectionModel

class LanguageSetter(QDialog,LanguageSetterUI.Ui_Dialog ):
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
        lang_dic={'English':'en_EN','Français':'fr_FR','日本語':'ja_JP'}
        self.init_combo()
        self.button.clicked.connect(self.button_clicked)
      
    def init_combo(self):  
        france=QtGui.QIcon('france.png')
        self.combo.addItem(QtGui.QIcon('united-kingdom.png'), "English")
        self.combo.addItem(france, "Français")
        self.combo.addItem(QtGui.QIcon(os.getcwd()+"japan.png"), "日本語")
        
        
    def read_language(self):
        return self.combo.currentText()
    
    def button_clicked(self):
        lang = self.read_language()
        if lang == 'English':
            self.model.set_language({'name':'english','code':'en_EN'})
            'memorize the language in DB'
            self.parent.set_language('en_EN')
        if lang == 'Français':
            self.model.set_language({'name':'french','code':'fr_FR'})
            self.parent.set_language('fr_FR')
           
        if lang =='日本語':
            self.model.set_language({'name':'japanese','code':'ja_JP'})
            self.parent.set_language('ja_JP')
            
            
        self.close()  
        app=QApplication.instance()
        app.exit( self.parent.EXIT_CODE_REBOOT ) 
        
            