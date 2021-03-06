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

from gen import ColorDialogUI


import view.constants as vcst
import view.styles as sty
import platform



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
        self.init_dialog_and_connections()
        self.set_translatable_texes()
        self.set_sample_colors()
        self.set_fonts()

        
    color_field={
            0:'editable',
            1:'calculated',
            2: 'read_only', 
            3: 'min_max_allowed',
            4: 'min_max_advised'
            }    
        
    def pick_color(self):
        '''
        The numbering of dialog buttons is rather particular (and given in designer)
        it is from top to bottom:
        1,5  2,7  3,8,  4,9  5,10
        every button is called pushButton_num
        '''
        'accessible name is something as read_only_1 or editable_0 please see init_dialog_and_connections below'
        num_button=self.sender().accessibleName()      
        color=QColorDialog.getColor()
        
        'the category is among editable, calculated, read_only, min_max_allowed and min_max_advised'
        field_category=num_button[:-2]#using the slicing operator
        field_num=num_button[-1:]
        
        'change the definition of colors in the styles file '
        sty.field_colors[field_category][int(field_num)]=color.name()
        'change the definition of styles in the styles file'
        style = "background-color:"+sty.field_colors[field_category][0]+";color:"+sty.field_colors[field_category][1]+";"
        sty.field_styles[field_category]=style
        
        'reuse the new definition from the styles file'
        self.set_sample_colors()
        
        cols=self.model.get_style(field_category)
        print('Color Dialog: pick color')
        print (cols)
        if (cols):
            print('Update the new style in the database')
            print(cols)
            self.model.update_style(field_category,sty.field_colors[field_category])
        else:
            print('save  the new style in the database')
            self.model.save_style(field_category,sty.field_colors[field_category])   

        cols=self.model.get_style(field_category)
        print (cols)
        
    def init_dialog_and_connections(self):
        
        for i in range(self.field_layout.count()):
            l=self.field_layout.itemAt(i)
            
            'itemAt(0) is a horizontal layout with 1 labels on the left and 2 button on the right'
            
            'for the button on first line'
            button=l.itemAt(2).itemAt(0).widget()
            button.setAccessibleName(self.color_field[i]+'_0')
            button.clicked.connect(self.pick_color)
            'for the button on second line'
            button=l.itemAt(2).itemAt(1).widget()
            button.setAccessibleName(self.color_field[i]+'_1')
            button.clicked.connect(self.pick_color)
            self.close_button.clicked.connect(self.close)
            
    def set_sample_colors(self):    
        for i in range(self.field_layout.count()):
            sample=self.field_layout.itemAt(i).itemAt(1).widget()
            style = "background-color:"+sty.field_colors[self.color_field[i]][0]+"; color:"+sty.field_colors[self.color_field[i]][1]+";"
            sample.setStyleSheet(style)
                 
    def set_translatable_texes(self):
        self.label_1.setText(self.tr('Colors for Editable fields')) 
        self.pushButton_1.setText('Change background color')
        self.pushButton_6.setText('Change text color')
        
        self.label_2.setText(self.tr('Colors for Calculated fields')) 
        self.pushButton_2.setText('Change background color')
        self.pushButton_7.setText('Change text color')
        
        self.label_3.setText(self.tr('Colors for Read Only fields')) 
        self.pushButton_3.setText('Change background color')
        self.pushButton_8.setText('Change text color')
        
        self.label_4.setText(self.tr('Colors for Min Max Allowed Values fields')) 
        self.pushButton_4.setText('Change background color')
        self.pushButton_9.setText('Change text color')
        
        self.label_5.setText(self.tr('Colors for Min Max Advised Values fields')) 
        self.pushButton_5.setText('Change background color')
        self.pushButton_10.setText('Change text color') 
         
        self.label_custom.setText(self.tr('Customize your colors'))
        self.info_edit.setText(self.tr('<h2>Warning?</h2> <p>The colors you set in this dialog will be fully applied only after you have restarted the application'))        
        
      
    def set_fonts(self):
        if self.model.in_use_fonts:
        
            self.label_1.setFont(self.model.in_use_fonts['field']) 
            self.pushButton_1.setFont(self.model.in_use_fonts['button']) 
            #self.label_6.setFont(self.model.in_use_fonts['field']) 
            self.pushButton_6.setFont(self.model.in_use_fonts['button']) 
            self.label_2.setFont(self.model.in_use_fonts['field'])
            self.pushButton_2.setFont(self.model.in_use_fonts['button']) 
            #self.label_7.setFont(self.model.in_use_fonts['field'])
            self.pushButton_7.setFont(self.model.in_use_fonts['button']) 
            self.label_3.setFont(self.model.in_use_fonts['field'])
            self.pushButton_3.setFont(self.model.in_use_fonts['button']) 
            #self.label_8.setFont(self.model.in_use_fonts['field']) 
            self.pushButton_8.setFont(self.model.in_use_fonts['button']) 
            self.label_4.setFont(self.model.in_use_fonts['field'])
            self.pushButton_4.setFont(self.model.in_use_fonts['button']) 
            #self.label_9.setFont(self.model.in_use_fonts['field'])
            self.pushButton_9.setFont(self.model.in_use_fonts['button']) 
            self.label_5.setFont(self.model.in_use_fonts['field']) 
            self.pushButton_5.setFont(self.model.in_use_fonts['button']) 
            #self.label_10.setFont(self.model.in_use_fonts['field'])
            self.pushButton_10.setFont(self.model.in_use_fonts['button']) 
            self.label_custom.setFont(self.model.in_use_fonts['field'])
            self.info_edit.setFont(self.model.in_use_fonts['field'])  
            
         
                                
            
                
                