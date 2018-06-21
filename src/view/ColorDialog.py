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
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,QMessageBox,QColorDialog

from gen import ColorDialogUI


import view.constants as vcst
import view.styles as sty



class ColorDialog(QWidget,ColorDialogUI.Ui_Dialog ):
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
        self.style_key_list=self.model.style_list
        self.set_connections()
        self.set_sample_colors()
        
    color_field={
            0:'editable',
            1:'calculated',
            2: 'read_only', 
            3: 'min_max_allowed',
            4: 'min_max_advised'
            }    
        
    def get_color(self):
        num_button=self.sender().accessibleName()
        
        color=QColorDialog.getColor()
        field_name=num_button[:-2]
        print('this is field name')
        print(field_name)
        field_num=num_button[-1:]
        sty.field_colors[field_name][int(field_num)]=color.name()
        style = "background-color:"+sty.field_colors[field_name][0]+";color:"+sty.field_colors[field_name][1]+";"
        sty.field_styles[field_name]=style
        self.set_sample_colors()
        self.model.save_style(field_name,sty.field_colors[field_name])


    def set_connections(self):
        
        for i in range(self.field_layout.count()):
            l=self.field_layout.itemAt(i)
            
            button=l.itemAt(0).itemAt(1).widget()
            button.setAccessibleName(self.color_field[i]+'_0')
            button.clicked.connect(self.get_color)
            #print(button.accessibleName())
            
            button=l.itemAt(0).itemAt(3).widget()
            button.setAccessibleName(self.color_field[i]+'_1')
            button.clicked.connect(self.get_color)
            #print(button.accessibleName())
            
    def set_sample_colors(self):    
        for i in range(self.field_layout.count()):
            sample=self.field_layout.itemAt(i).itemAt(1).widget()
            style = "background-color:"+sty.field_colors[self.color_field[i]][0]+"; color:"+sty.field_colors[self.color_field[i]][1]+";"
            sample.setStyleSheet(style)
                 
        
      
        
            
                
                