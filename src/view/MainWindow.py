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
from PyQt5 import Qt,QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow,QHBoxLayout,QLabel,QLineEdit,QMessageBox,QFrame,QVBoxLayout,QPushButton
from model.Model import Model
from controller.Controller import Controller
from gen import MainWindowUI
from view.MaltDialog import MaltDialog 
from view.RestDialogCreate import RestDialogCreate
from view.HopDialog import HopDialog
from view.YeastDialog import YeastDialog
from view.RecipeDialog import RecipeDialog 
from view.EquipmentDialog import EquipmentDialog
from view.ColorDialog import ColorDialog
from view.FontSizeDialog import FontSetDialog
from view.HelpWindow import HelpWindow
from view.UnitSetter import UnitSetter
from view.LanguageSetter import LanguageSetter
from view.Feedback import Feedback
from view.Utils import Utils
import view.constants as vcst
import view.styles as sty
from view.CustomProgressBar import CustomProgressBar
from doc.Documentation import Documentation
from view.FolderChooser import FolderChooser
from view.ImportExportDb import ImportExportDb
from model.FontSet import FontSet
from PyQt5.QtGui import QFont

     
import sys
import time
import datetime
import os
import webbrowser
import platform

from model.Session import Session
from model.MaltInSession import MaltInSession
from model.HopInSession import HopInSession
from model.RestInSession import RestInSession
from model.YeastInSession import YeastInSession

from model.Calculator import Calculator

import math
from PyQt5.Qt import QSpacerItem, QEvent
from PyQt5.QtWidgets import QFileDialog


class MainWindow(QMainWindow,MainWindowUI.Ui_MainWindow):
    '''
    classdocs
    '''
    EXIT_CODE_REBOOT = -12345678
    def __init__(self, translator,parent=None):
        super(MainWindow,self).__init__(parent)
        self.setupUi(self)
        
        self.translator=translator
        
        'THIS IS FOR CX FREEZE ONLY'
        self.frozen='not'
        if getattr(sys, 'frozen', False):
        # frozen
            dir_ = os.path.dirname(sys.executable)
            self.frozen='yes'
            self.bundle_dir=dir_
            self.model=Model(self.bundle_dir)
            self.trad_path=os.path.join(self.bundle_dir,'translate')
        else:
        # unfrozen
            dir_ = os.path.dirname(os.path.realpath(__file__))
            'l’import export is reserved to the frozen application (bundled)'
            self.actionImport_Export_Databases.setVisible(False)
            self.model = Model()
            'the path to the .qm translated files'
            (filepath,filename)=os.path.split(__file__)
            self.trad_path=os.path.join(filepath,'..','translate')
            
           
            
            
        '''    
        'THIS IS FOR PYINSTALLER ONLY'
        'Folder structure is quite different when running in a bundle'
        'Please see pyinstaller’s documentation'
        self.frozen = 'not' 
        if getattr(sys, 'frozen', False):
            self.frozen = 'yes'
            self.bundle_dir = sys._MEIPASS
            self.model = Model(self.bundle_dir)
            'the path to the translated .qm files'
            self.trad_path=os.path.join(self.bundle_dir ,'translate')
   
        else: 
            'l’import export is reserved to the frozen application (bundled)'
            self.actionImport_Export_Databases.setVisible(False)
            self.model = Model()
            'the path to the .qm translated files'
            (filepath,filename)=os.path.split(__file__)
            self.trad_path=os.path.join(filepath,'..','translate')
        '''
        
        self.controller = Controller(self.model)
        self.unitSetter=UnitSetter(self.model,self)
        self.language_setter=LanguageSetter(self.model,self)
        if not self.model.language:
            self.language_setter.setModal(True)
            self.language_setter.show()  
        else: self.set_language(self.model.language[1]) 
        #colors must be set before all dialogs
        'due to the translation into util.init_hop_usage_dic , util should be created after setting the language'
        self.util=Utils(self.model)
        self.util.init_hop_usage_dic()
        self.style_key_list=self.model.style_list
        self.set_active_colors() 
        self.maltDialog = MaltDialog(self.model,self.controller,self.util)
        self.hopDialog = HopDialog(self.model,self.controller,self.util)
        self.restDialogCreate = RestDialogCreate(self.model,self.controller,self.util)
        self.yeastDialog = YeastDialog(self.model,self.controller,self.util)
        self.recipeDialog = RecipeDialog(self.model,self.controller,self.util)
        self.colorDialog = ColorDialog(self.model,self.controller,self.util)
        self.equipmentDialog = EquipmentDialog(self.model,self.controller,self.util)
        self.fontSizeDialog=FontSetDialog(self.model,self.controller,self.util)
        
        self.feedback=Feedback(self.model,self.util)
        'if running in a bundle may be the user wants to save or restore their databases'
        if self.frozen=='yes':
            self.importExportDbDialog=ImportExportDb(self.model,self.controller,self.util,self.bundle_dir)
            
        self.helpWindow=HelpWindow()
        self.malt_key_list=self.model.malt_list 
        self.hop_key_list=self.model.hop_list
        self.recipe_key_list=self.model.recipe_list
        self.equipment_key_list=self.model.equipment_list
        self.session_key_list = self.model.session_list
        self.init_equipment_combo()
        self.init_recipe_combo()
        self.set_tooltips()
        self.set_subscriptions()
        'set the way various controls respond'
        self.set_connections()
        self.targeted_original_gravity =None
        self.brewing_efficiency=None   
        self.init_session_combo()
        self.new_session()
        self.init_font_set_db()
        self.view_session_button.setEnabled(False)
        
        
        
        
       
  
    def add_hop_view(self,hop,usage=None,duration=None,hop_rate=None):
        hopT=hop
        hl=QHBoxLayout()
        
        label_name=QLabel()
        label_name.setAccessibleName('name')
        label_name.setMinimumSize(200,30)
        label_name.setText(hopT.name)
        hl.addWidget(label_name)
        
        label_desc=QLabel()
        label_desc.setAccessibleName('desc')
        label_desc.setMinimumSize(200,30)
        info= ' – '+hopT.form + ' – ' +str(hopT.alpha_acid)+ ' % AA'
        label_desc.setText(info) 
        hl.addWidget(label_desc)

        label_usage=QLabel()
        label_usage.setAccessibleName('usage')       
        label_usage.setText(usage)
        label_usage.setFixedWidth(100)
        hl.addWidget(label_usage)
       
        label_duration=QLabel()
        label_duration.setAccessibleName('duration')
        label_duration.setMaximumSize(40,30)
        if duration:
            label_duration.setText(str(duration))
        hl.addWidget(label_duration)    
   
        #other usage do not need time
        time_label=QLabel()
        time_label.setAccessibleName('time_unit')
        if usage:
            usage_key=self.util.get_usage_key(usage)
           
            if usage_key == vcst.HOP_BOILING_HOPPING:
                time_label.setText('min')
                hl.addWidget(time_label)#4for unit
        else:
            time_label.setText('')
            hl.addWidget(time_label)#4for unit   
           
        label_advised_amount=QLabel(self.tr('Advised by recipe'))
        label_advised_amount.setAccessibleName('advised_label')
        label_advised_amount.setAlignment(Qt.Qt.AlignRight)
        hl.addWidget(label_advised_amount)
                       
        edit_advised_amount=QLineEdit()
        edit_advised_amount.setAccessibleName('advised_amount')#the amount indicated in the recipe
        edit_advised_amount.setStyleSheet(sty.field_styles['calculated'])
        edit_advised_amount.setReadOnly(True) 
        edit_advised_amount.setMaximumSize(50,30)
       
        ha_unit=self.model.get_unit('hop_mass')
        if ha_unit: ha_unit_label=self.util.get_unit_label(ha_unit)
        hl.addWidget(edit_advised_amount)
        advised_amount_unit_label=QLabel()
        advised_amount_unit_label.setAccessibleName('advised_unit')
        advised_amount_unit_label.setText(ha_unit_label)
        hl.addWidget(advised_amount_unit_label)
        
        'the amount the user decides to use'
        label_amount=QLabel(self.tr('Adopted'))
        label_amount.setAccessibleName('amount_label')
        label_amount.setAlignment(Qt.Qt.AlignRight)
        hl.addWidget(label_amount)
        edit_amount=QLineEdit()
        edit_amount.setAccessibleName('amount')
        edit_amount.setStyleSheet(sty.field_styles['editable'])
        edit_amount.setMaximumSize(50,30)
    
        if hop_rate:
            hr_unit=self.model.get_unit('hop_rate')
            hidden_hop_rate=QLineEdit()
            hidden_hop_rate.setText(str(self.util.convert_to(hr_unit,hop_rate)))
            hidden_hop_rate.setVisible(False)
            hidden_hop_rate.setAccessibleName('hidden_hop_rate')
            hl.addWidget(hidden_hop_rate)
            
        'recalculate IBU whenever the user changes the amount'           
        edit_amount.editingFinished.connect(self.calculate_IBU)
        hl.addWidget(edit_amount)
        
        
        amount_unit_label=QLabel()
        amount_unit_label.setText(ha_unit_label)
        amount_unit_label.setAccessibleName('amount_unit_label')
        hl.addWidget(amount_unit_label)#6 for weight unit
        
        label_calculated_IBU=QLabel()
        label_calculated_IBU.setAccessibleName('calculated_IBU')
        hl.addWidget(label_calculated_IBU)    
        
        label_calculated_IBU_unit=QLabel('IBU')
        label_calculated_IBU_unit.setAccessibleName('calculated_IBU_unit')
        
        hl.addWidget(label_calculated_IBU_unit)  #8 
        
        label_hidden_alpha=QLabel()
        label_hidden_alpha.setAccessibleName('hidden_alpha')
        label_hidden_alpha.setText(str(hopT.alpha_acid))
        hl.addWidget(label_hidden_alpha)
        label_hidden_alpha.hide()
        
        'SETTING THE FONTS'
        label_name.setFont(self.model.in_use_fonts['field'])
        label_desc.setFont(self.model.in_use_fonts['field'])
        label_usage.setFont(self.model.in_use_fonts['field'])
        label_duration.setFont(self.model.in_use_fonts['field'])
        time_label.setFont(self.model.in_use_fonts['field'])
        advised_amount_unit_label.setFont(self.model.in_use_fonts['field'])
        label_advised_amount.setFont(self.model.in_use_fonts['field'])
        edit_advised_amount.setFont(self.model.in_use_fonts['field'])
        label_amount.setFont(self.model.in_use_fonts['field'])
        edit_amount.setFont(self.model.in_use_fonts['field'])
        amount_unit_label.setFont(self.model.in_use_fonts['field'])
        label_calculated_IBU.setFont(self.model.in_use_fonts['field'])
        label_calculated_IBU_unit.setFont(self.model.in_use_fonts['field'])

        self.hop_layout.addLayout(hl)
        
                
    def add_malt_view(self,malt_type=None,percent=None,):
        """ Add a MaltInMash in a reserved layout displaying its MaltType name and percentage
        as well as a delete push button
        When displaying an existing recipe, the malt_type is passed in parameters, while when
        added manually by the user, it is read from the GUI
        
        """      
        maltT=malt_type
        hl=QHBoxLayout()#create an horizontal layout to host widgets for one malt line
        
        edit_name=QLineEdit()
        edit_name.setAccessibleName('name')
        edit_name.setReadOnly(True)
        
        hl.addWidget(edit_name)
        edit_name.setText(maltT.name)
        
        edit_percentage=QLineEdit()
        edit_percentage.setAccessibleName('percentage')
        edit_percentage.setMaximumSize(60,30)
        edit_percentage.setStyleSheet(sty.field_styles['read_only'])
        edit_percentage.setReadOnly(True)
        if percent:
            edit_percentage.setText(str(percent))
        hl.addWidget(edit_percentage)    
        
        label_percentage_unit=QLabel()
        label_percentage_unit.setText('%')
        label_percentage_unit.setAccessibleName('percentage_unit')
        label_percentage_unit.setMaximumSize(30,30)
        #label_percentage_unit.setStyleSheet("font-size: 14px;")
        hl.addWidget(label_percentage_unit)
        
        edit_calculated_mass=QLineEdit()
        edit_calculated_mass.setAccessibleName('calculated_mass')
        edit_calculated_mass.setMaximumSize(60,30)
        edit_calculated_mass.setStyleSheet(sty.field_styles['calculated'])
        edit_calculated_mass.setReadOnly(True)  
        hl.addWidget(edit_calculated_mass)
        
        m_unit=self.model.get_unit('malt_mass')
        if m_unit: m_unit_label=self.util.get_unit_label(m_unit)
        label_mass_unit=QLabel()
        label_mass_unit.setText('kg')
        label_mass_unit.setAccessibleName('calculated_mass_unit')
        #label_mass_unit.setStyleSheet("font-size: 14px;")
        label_mass_unit.setMaximumSize(40,30)
        label_mass_unit.setText(m_unit_label)
        hl.addWidget(label_mass_unit)
        
        edit_name.setFont(self.model.in_use_fonts['field'])
        edit_percentage.setFont(self.model.in_use_fonts['field'])
        label_percentage_unit.setFont(self.model.in_use_fonts['field'])
        edit_calculated_mass.setFont(self.model.in_use_fonts['field'])
        label_mass_unit.setFont(self.model.in_use_fonts['field'])
              
        self.malt_layout.addLayout(hl)
        
    def add_yeast_view(self,yeast_type,rate=None,amount=None,creation_mode=True):  
        self.util.clearLayout(self.yeast_layout)
        yeastT=yeast_type
        hl=QHBoxLayout()#create an horizontal layout to host widgets for the yeast
        
        maker_edit=QLineEdit()
        maker_edit.setAccessibleName('maker')
        maker_edit.setMinimumSize(100,30)
        maker_edit.setMaximumSize(100,30)
        maker_edit.setStyleSheet(sty.field_styles['read_only'])
        maker_edit.setReadOnly(True)
        maker_edit.setText(yeastT.maker)
        hl.addWidget(maker_edit)
        
        name_edit=QLineEdit()
        name_edit.setAccessibleName('name')
        name_edit.setMinimumSize(200,30)
        name_edit.setMaximumSize(200,30)
        name_edit.setStyleSheet(sty.field_styles['read_only'])
        name_edit.setReadOnly(True)
        name_edit.setText(yeastT.name)
        hl.addWidget(name_edit)
        
        form_edit=QLineEdit()
        form_edit.setAccessibleName('form')
        form_edit.setMinimumSize(70,30)
        form_edit.setMaximumSize(70,30)
        form_edit.setStyleSheet(sty.field_styles['read_only'])
        form_edit.setReadOnly(True)
        form_edit.setText(yeastT.form)
        hl.addWidget(form_edit)
        hl.addStretch()
        
        vl1=QVBoxLayout()
        t_unit=self.model.get_unit('temperature')
        temp_label=QLabel(self.tr('Temperature range in '+self.util.get_unit_label(t_unit)),alignment=4)
        temp_label.setAccessibleName('temperature_label ')
        vl1.addWidget(temp_label)
        hl1=QHBoxLayout()
        min_allowed_temperature_edit=QLineEdit()
        min_allowed_temperature_edit.setAccessibleName('min_allowed_temperature')
        min_allowed_temperature_edit.setMinimumSize(50,30)
        min_allowed_temperature_edit.setMaximumSize(50,30)
        min_allowed_temperature_edit.setStyleSheet(sty.field_styles['min_max_allowed'])
        min_allowed_temperature_edit.setReadOnly(True)
        t=self.util.convert_to(t_unit,yeastT.min_allowed_temperature)
        min_allowed_temperature_edit.setText(str(t))
        hl1.addWidget(min_allowed_temperature_edit)
        
        min_advised_temperature_edit=QLineEdit()
        min_advised_temperature_edit.setAccessibleName('min_advised_temperature')
        min_advised_temperature_edit.setMinimumSize(50,30)
        min_advised_temperature_edit.setMaximumSize(50,30)
        min_advised_temperature_edit.setStyleSheet(sty.field_styles['min_max_advised'])
        min_advised_temperature_edit.setReadOnly(True)
        t=self.util.convert_to(t_unit,yeastT.min_advised_temperature)
        min_advised_temperature_edit.setText(str(t))
        hl1.addWidget(min_advised_temperature_edit)
        
        max_advised_temperature_edit=QLineEdit()
        max_advised_temperature_edit.setAccessibleName('max_advised_temperature')
        max_advised_temperature_edit.setMinimumSize(50,30)
        max_advised_temperature_edit.setMaximumSize(50,30)
        max_advised_temperature_edit.setStyleSheet(sty.field_styles['min_max_advised'])
        max_advised_temperature_edit.setReadOnly(True)
        t=self.util.convert_to(t_unit,yeastT.max_advised_temperature)
        max_advised_temperature_edit.setText(str(t))
        hl1.addWidget(max_advised_temperature_edit)
        
        max_allowed_temperature_edit=QLineEdit()
        max_allowed_temperature_edit.setAccessibleName('max_allowed_temperature')
        max_allowed_temperature_edit.setMinimumSize(50,30)
        max_allowed_temperature_edit.setMaximumSize(50,30)
        max_allowed_temperature_edit.setStyleSheet(sty.field_styles['min_max_allowed'])
        max_allowed_temperature_edit.setReadOnly(True)
        t=self.util.convert_to(t_unit,yeastT.max_allowed_temperature)
        max_allowed_temperature_edit.setText(str(t))
        hl1.addWidget(max_allowed_temperature_edit)
        vl1.addLayout(hl1)
        vl1.addStretch()
        hl.addLayout(vl1)
        hl.addStretch()
        
        vl2=QVBoxLayout()
        
        yr_unit=self.model.get_unit('yeast_rate')
        yr_unit_label=self.util.get_unit_label(yr_unit)
        ya_unit=self.model.get_unit('yeast_mass')
        ya_unit_label=self.util.get_unit_label(ya_unit)
        
        
        if creation_mode:
            hl21=QHBoxLayout()
            hl22=QHBoxLayout()
            hl23=QHBoxLayout()
            pitch_label=QLabel('',alignment=4)
            pitch_label.setText(self.tr('Recommended Pitching rate'))
            pitch_label.setAccessibleName('recommended_pitching_label')
            hl21.addWidget(pitch_label)
 
            'in this mode, only the rate is given, amount has to be calculated'
            calculate_amount_button=QPushButton(self.tr('Calculate'))
            calculate_amount_button.setAccessibleName('calculate_button')
            calculate_amount_button.setMaximumSize(120, 30)
            calculate_amount_button.clicked.connect(self.calculate_yeast_amount)
            hl21.addWidget(calculate_amount_button)
            vl2.addLayout(hl21)
            
            rate_edit=QLineEdit()
            rate_edit.setAccessibleName('rate')
            rate_edit.setMaximumSize(60,30)
            'in session creation mode, rate is given by the recipe: see load_recipe'
            if rate: rate_edit.setText(self.util.convert_to(yr_unit,rate))
            rate_edit.setStyleSheet(sty.field_styles['read_only'])
            rate_unit=QLabel()   
            rate_unit.setAccessibleName('rate_unit')
            rate_unit.setText(yr_unit_label)
            hl22.addWidget(rate_edit)
            hl22.addWidget(rate_unit) 
            
            'amount is calculated from rate when button clicked '
            y_unit=self.model.get_unit('yeast_mass')
            calculated_amount_edit=QLineEdit()
            calculated_amount_edit.setAccessibleName('calculated_amount')
            calculated_amount_edit.setStyleSheet(sty.field_styles['calculated'])
            calculated_amount_edit.setReadOnly(True)
            calculated_amount_edit.setMaximumSize(60,30)
            hl22.addWidget(calculated_amount_edit)
            calculated_amount_unit=QLabel()
            calculated_amount_unit.setAccessibleName('calculated_amount_unit')
            calculated_amount_unit.setText(self.util.get_unit_label(y_unit))
            calculated_amount_unit.setMaximumSize(30,30)
            hl22.addWidget(calculated_amount_unit) 
            vl2.addLayout(hl22)
            
            
            hline=QFrame()
            hline.setFrameShape(QFrame.HLine)
            hline.setFrameShadow(QFrame.Sunken)
            vl2.addWidget(hline)
            adopted_pitch_label=QLabel('',alignment=4)
            adopted_pitch_label.setAccessibleName('adopted_pitching_label')
            adopted_pitch_label.setText(self.tr('Adopted Pitching rate'))
            vl2.addWidget(adopted_pitch_label)
            'adopted_rate will be calculated after editing the adopted amount. See calculate_adopted_pitching_rate()'
            adopted_rate_edit=QLineEdit()
            adopted_rate_edit.setAccessibleName('adopted_pitching_rate')
            adopted_rate_edit.setMaximumSize(60,30)
            adopted_rate_edit.setStyleSheet(sty.field_styles['calculated'])
            adopted_rate_edit.setReadOnly(True)
            hl23.addWidget(adopted_rate_edit)
            adopted_rate_unit=QLabel()
            adopted_rate_unit.setText(yr_unit_label)
            adopted_rate_unit.setAccessibleName('calculated_rate_unit')
            hl23.addWidget(adopted_rate_unit)
            
            adopted_amount_edit=QLineEdit()
            adopted_amount_edit.setAccessibleName('adopted_amount')
            adopted_amount_edit.setStyleSheet(sty.field_styles['read_only'])
            adopted_amount_edit.setReadOnly(True)
            adopted_amount_edit.editingFinished.connect(self.calculate_adopted_pitching_rate)
            adopted_amount_edit.setMaximumSize(60,30)
            hl23.addWidget(adopted_amount_edit)
            adopted_amount_unit=QLabel()
            adopted_amount_unit.setAccessibleName('adopted_amount_unit')
            adopted_amount_unit.setText(self.util.get_unit_label(y_unit))
            adopted_amount_unit.setMaximumSize(30,30)
      
            hl23.addWidget(adopted_amount_unit) 
        
            vl2.addLayout(hl23)
            
            'pitch_label does not exist in other modes for example load session'
            pitch_label.setFont(self.model.in_use_fonts['field'])
            calculate_amount_button.setFont(self.model.in_use_fonts['button'])
            rate_edit.setFont(self.model.in_use_fonts['field'])
            rate_unit.setFont(self.model.in_use_fonts['field'])
            calculated_amount_edit.setFont(self.model.in_use_fonts['field'])
            calculated_amount_unit.setFont(self.model.in_use_fonts['field'])
            rate_unit.setFont(self.model.in_use_fonts['field'])
            adopted_rate_unit.setFont(self.model.in_use_fonts['field'])
            
              
        else:
            'Here we display a session from database.It includes rate and amount in yeast_in_session object'
            hl23=QHBoxLayout()
            adopted_pitch_label=QLabel(self.tr('Adopted Pitching rate'),alignment=4)
            adopted_pitch_label.setAccessibleName('adopted_pitching_label')
            vl2.addWidget(adopted_pitch_label)
            adopted_rate_edit=QLineEdit()
            #calculated_rate_edit.setAccessibleName('calculated_pitching_rate')
            adopted_rate_edit.setMaximumSize(60,30)
            adopted_rate_edit.setStyleSheet(sty.field_styles['read_only'])
            adopted_rate_edit.setReadOnly(True)
            adopted_rate_edit.setText(self.util.convert_to(yr_unit,rate))
            #calculated_rate_edit.setText(self.util.convert_from(yr_unit, )
            hl23.addWidget(adopted_rate_edit)
            adopted_rate_unit=QLabel()
            adopted_rate_unit.setText(yr_unit_label)
            hl23.addWidget(adopted_rate_unit)
            adopted_amount_edit=QLineEdit()
            adopted_amount_edit.setAccessibleName('adopted_amount')
            adopted_amount_edit.setStyleSheet(sty.field_styles['read_only'])
            adopted_amount_edit.setReadOnly(True)
            adopted_amount_edit.setText(self.util.convert_to(ya_unit,amount))
            adopted_amount_edit.setMaximumSize(60,30)
            hl23.addWidget(adopted_amount_edit)
            adopted_amount_unit=QLabel()
            adopted_amount_unit.setText(ya_unit_label)
            adopted_amount_unit.setMaximumSize(30,30)
            hl23.addWidget(adopted_amount_unit)
            vl2.addLayout(hl23)  
            adopted_rate_unit.setFont(self.model.in_use_fonts['field'])
            adopted_rate_edit.setFont(self.model.in_use_fonts['field'])
            adopted_pitch_label.setFont(self.model.in_use_fonts['field'])

        hl.addLayout(vl2)
        hl.addStretch()
        maker_edit.setFont(self.model.in_use_fonts['field'])
        name_edit.setFont(self.model.in_use_fonts['field'])
        form_edit.setFont(self.model.in_use_fonts['field'])
        temp_label.setFont(self.model.in_use_fonts['field'])
        min_advised_temperature_edit.setFont(self.model.in_use_fonts['field'])
        max_advised_temperature_edit.setFont(self.model.in_use_fonts['field'])
        min_allowed_temperature_edit.setFont(self.model.in_use_fonts['field'])
        max_allowed_temperature_edit.setFont(self.model.in_use_fonts['field'])
        adopted_amount_edit.setFont(self.model.in_use_fonts['field'])
        adopted_amount_unit.setFont(self.model.in_use_fonts['field'])
        self.yeast_layout.addLayout(hl)   
     
        
    def batch_volume_changed(self): 
        self.clean_results()
        #self.set_aroma_amounts() 
        
        
    def calculate_adopted_pitching_rate(self):
        'used to calculate the pitching rate in creation mode. In display session, mode it is already included into YeasInSesson object'
        v_unit=self.model.get_unit('water_volume')
        y_unit=self.model.get_unit('yeast_mass')
        yr_unit=self.model.get_unit('yeast_rate')
        yr_unit_label=self.util.get_unit_label(yr_unit)
        batch_volume = self.util.check_input(self.batch_volume_edit, False, self.tr('Batch volume'), False, 1, vcst.MAX_VOLUME,None,v_unit) 
        if not batch_volume:#alert is given in check_input
            return
        original_gravity=self.util.check_input(self.targeted_original_gravity_value,False,self.tr('Targeted Original Gravity'),False,1.000,vcst.MAX_OG)
        if not original_gravity:#alert is given in check_input
            return
        widgt=self.util.get_by_name_recursive(self.yeast_layout,'adopted_amount')
        a = self.util.check_input(widgt,False,self.tr('Adopted yeast Amount'),False, 0,vcst.MAX_VOLUME*vcst.MAX_PITCHING_RATE,None,y_unit)
        if not a: return
        advised_rate= self.recipe.yeast_in_recipe.pitching_rate
        billions=a *100/11
        platos=(original_gravity -1)*1000/4
        pitching_rate=  billions / batch_volume / platos
        adopted_p_rate_edit=self.util.get_by_name_recursive(self.yeast_layout,'adopted_pitching_rate')
        adopted_p_rate_edit.setText(self.util.convert_to(yr_unit,pitching_rate))
        self.update_pitching_bar(advised_rate,pitching_rate)      
        
    def calculate_hop_amounts(self): 
        'calculate hop amounts based on hop rate (g/l) and final boiling volume'  
        'this function is called whenever the user click the "Reset to Recipe values" in the hop area of the MainWindow' 
        'It sets values both in the advised and the adopted fields'
        v_unit=self.model.get_unit('water_volume')
        'batch_size always in liter hence the conversion from display unit'
        batch_size=self.util.check_input(self.batch_volume_edit,False,self.tr('Batch Volume'),False, 0,vcst.MAX_VOLUME,None,v_unit)
        if not batch_size:
            return
        print('batch size is '+str(batch_size))
        if not self.equipment:
            warning_text='Warning : Hop Amount Calculation'
            self.util.alerte(self.tr('Please select an equipment'),QMessageBox.Warning, warning_text)
            return
        'end_boiling_volume also in liters'
        end_boiling_volume=batch_size+self.equipment.boiler_dead_space
        for i in range(self.hop_layout.count()):
            hr_unit=self.model.get_unit('hop_rate')
            ha_unit=self.model.get_unit('hop_mass')
            hl=self.hop_layout.itemAt(i).layout()
            w_amount= self.util.get_by_name(hl,'amount')
            #w_advised_amount=self.util.get_by_name(hl,'advised_amount')
            w_hidden_rate=self.util.get_by_name(hl, 'hidden_hop_rate')
            'rate always in g/liters'
            rate=self.util.check_input(w_hidden_rate, False, self.tr(' Hop rate '+str(i)), False, 0, vcst.MAX_HOP_RATE, True,hr_unit)
            print('rate is '+str(rate))
            if not rate:
                return
            w_advised=self.util.get_by_name(hl,'advised_amount')
            print('end boil volume = '+str(end_boiling_volume))
            advised_value=self.util.convert_to(ha_unit, rate*end_boiling_volume)
            #advised_value_formated='{0:.2f}'.format(advised_value)
            #display_value='{0:.2f}'.format(advised_value)
            w_advised.setText(advised_value)
            w_amount.setText(advised_value)
            #w_advised_amount.setText(str(advised_value))
            self.calculate_IBU(w_amount)
        

 
    def calculate_IBU(self,s=None):
        '''
        this function is called after hop amounts have been calculated or on editing finished for one specific hop adopted amount 
        and calculate the IBU contribution for all hops or the selected hop
        '''
        usage=None
        warning_text=self.tr('Warning : IBU Calculation')
        if not self.equipment: 
            self.util.alerte(self.tr('You need to select an equipment prior to IBU calculation.'),
                             QMessageBox.Warning,warning_text)
            self.batch_volume_edit.setText('')
            return
        duration=0
        line=None
        widg=None
        if s:
            send=s
        else:     
            send=self.sender()
            
        for i in range(self.hop_layout.count()):
            hl=self.hop_layout.itemAt(i).layout()
            w_amount= self.util.get_by_name(hl,'amount')
            w_advised_amount=self.util.get_by_name(hl,'advised_amount')
            w_hidden_rate=self.util.get_by_name(hl, 'hidden_hop_rate')
            w_usage=self.util.get_by_name(hl, 'usage')
            text=w_usage.text()
            usage=self.util.get_usage_key(text)
            if (w_amount==send):
                line=hl
                widg=w_amount
                break
            
        if not widg:
            return #normally not possible
        'In the hop_usage_dic, usage is the key not the val'
        if not(usage==vcst.HOP_BOILING_HOPPING or usage==vcst.HOP_FIRST_WORT_HOPPING):
            'no calculation in other usage cases'
            return 
        v_unit=self.model.get_unit('water_volume')
        'get the batch volume in liters'
        batch_volume = self.util.check_input(self.batch_volume_edit, False, self.tr('Batch volume'), False, 1,vcst.MAX_VOLUME,None,v_unit) 
        if not batch_volume:
            widg.setText('') 
            return 
        boiling_time=self.recipe.boiling_time
        if not boiling_time: 
            widg.setText('')
            return  
        #flag calculated determines the default style for the widget
        ha_unit=self.model.get_unit('hop_mass')
        'get the mass in g whatever the display unit'
        mass=self.util.check_input(widg, False, self.tr('Hop amount'), False, 0, vcst.MAX_VOLUME*vcst.MAX_HOP_RATE,None,ha_unit)
        if not(isinstance(mass,float)):#if not mass: 
            widg.setText('')
            return
        w_alpha=self.util.get_by_name(line,'hidden_alpha')
        alpha = float(w_alpha.text()) 
        w_usage=self.util.get_by_name(line,'usage')
        if w_usage.text()==self.util.hop_usage_dic[vcst.HOP_FIRST_WORT_HOPPING]:
            duration =60*1.1 #according to Palmer, 110% of 60 mn boiling with the same quantities
        else:
            w_duration=self.util.get_by_name(line,'duration')
            duration = float(w_duration.text())  
            if duration > boiling_time:
                w_duration.setStyleSheet(vcst.WARNING_STYLE)
                self.util.alerte('The hop duration is more than the boiling time thus it has been limited to the boiling time',
                            QMessageBox.Warning,warning_text)  
                duration = boiling_time
          
      
        calculator=Calculator(self.model,self.recipe,self.equipment,batch_volume,boiling_time)
        final_volume=batch_volume+self.equipment.boiler_dead_space
        ibu=calculator.get_IBU(duration,self.recipe.targeted_original_gravity, mass,alpha,final_volume)
        val='{0:.2f}'.format(ibu)
        w_ibu=self.util.get_by_name(line,'calculated_IBU')   
        w_ibu.setText(val)
        self.update_ibu_bar(self.recipe.targeted_bitterness)      
        return ibu       

     
    
    def calculate_IBU_later(self,duration,batch_volume,gravity,amount,alpha,final_volume):
        '''this function uses the values saved with session but not values of actual recipe and equipment as'
        as these later may have changed since '''
        f_t= (1 - math.exp(-0.04 * duration))   / 4.15
        f_G=1.65 * (0.000125 **(gravity-1))
        return (10 / final_volume) * amount * f_G * f_t * alpha  
        
        
    def calculate_malt_amounts(self):
        'calculate malt amounts based on percentages and gravity target'
        'This function is called after a recipe, an equipment, a batch size and a grain temperature have been defined'
        'whenever the user click the calculate button in the malt area of the main window'
        v_unit=self.model.get_unit('water_volume')
        t_unit=self.model.get_unit('temperature')
        self.set_input_style()
        warning_text=self.tr('Warning : Malt Amount Calculation')
        
        if not self.recipe:
            self.util.alerte(self.tr('Please select a recipe'),QMessageBox.Warning, warning_text)
            return
        if not self.equipment:
            self.util.alerte(self.tr('Please select an equipment'),QMessageBox.Warning, warning_text)
        self.batch_volume = self.util.check_input(self.batch_volume_edit, False, self.tr('Batch volume'), False, 1, vcst.MAX_VOLUME,None,v_unit) 
        if not self.batch_volume: return 
        self.grain_temperature = self.util.check_input(self.grain_temperature_edit, False, 'Grain temperature', False, 0,vcst.MAX_GRAIN_TEMPERATURE,None,t_unit) 
        if not self.grain_temperature: return
        
        first_rest=self.rest_layout.itemAt(0)
        if first_rest:
            self.first_rest_temperature = float(first_rest.itemAt(3).widget().text())                                                    
        else:
            self.util.alerte('There should be at least one rest. Please select a recipe or check the recipe you have selected',
                             QMessageBox.Warning,warning_text)    
 
        calculator=Calculator(self.model,self.recipe,self.equipment,self.batch_volume,self.boiling_time)
        total_mass=calculator.get_malt_mass()
        
        unit=self.model.get_unit('malt_mass')
        for i in range(len(self.malts)):
            w_percentage=self.util.get_by_name(self.malt_layout.itemAt(i).layout(),'percentage')
            amount=total_mass*float(w_percentage.text())/100
            w_calculated_mass=self.util.get_by_name(self.malt_layout.itemAt(i).layout(),'calculated_mass')
            w_calculated_mass.setText(str(self.util.convert_to(unit, float(math.ceil(amount*100)/100))))

        if self.equipment.type == 1: self.mash_water_volume = calculator.get_mash_water_volume(1)
        if self.equipment.type == 0: self.mash_water_volume  = calculator.get_mash_water_volume(0)
        #val='{0:.2f}'.format(self.mash_water_volume)
        vol=self.util.convert_to(v_unit, self.mash_water_volume)
        self.mash_water_volume_edit.setText(str(vol))
        strike_temperature = calculator.get_strike_temperature(self.mash_water_volume, total_mass, \
                            self.first_rest_temperature, self.grain_temperature)
        val='{0:.1f}'.format(strike_temperature)
        self.strike_temperature_edit.setText(val)
        self.sparge_water_volume = calculator.get_sparge_water_volume(self.mash_water_volume)
        #val ='{0:.2f}'.format(self.sparge_water_volume)
        self.mash_sparge_water_volume_edit.setText(str(self.util.convert_to(v_unit, self.sparge_water_volume)))    
    def calculate_yeast_amount(self):
        v_unit=self.model.get_unit('water_volume')
        y_unit=self.model.get_unit('yeast_mass')
        batch_volume = self.util.check_input(self.batch_volume_edit, False, self.tr('Batch volume'), False, 1, vcst.MAX_VOLUME,None,v_unit) 
        if not batch_volume:#alert is given in check_input
            return
        original_gravity=self.util.check_input(self.targeted_original_gravity_value,False,self.tr('Targeted Original Gravity'),False,1.000,vcst.MAX_OG )
        if not original_gravity:#alert is given in check_input
            return
        pitching_rate = self.recipe.yeast_in_recipe.pitching_rate
        billions=pitching_rate * batch_volume * 1000 * (original_gravity -1)/4
        amount=billions/100*11
        w_amount=self.util.get_by_name_recursive(self.yeast_layout,'calculated_amount')
        w_amount.setText(self.util.convert_to(y_unit,amount))
        w_adopted_amount=self.util.get_by_name_recursive(self.yeast_layout,'adopted_amount')
        w_adopted_amount.setText(self.util.convert_to(y_unit,amount))
        adopted_yeast_amount_edit=self.util.get_by_name_recursive(self.yeast_layout, 'adopted_amount')
        if adopted_yeast_amount_edit: 
            adopted_yeast_amount_edit.setReadOnly(False)
            adopted_yeast_amount_edit.setStyleSheet(sty.field_styles['editable'])
            adopted_yeast_amount_edit.editingFinished.connect(self.calculate_adopted_pitching_rate)
        self.calculate_adopted_pitching_rate()
        
        
       
        
    def changeEvent(self, event):
        print('changeEvent triggered'+str(event.type()))
        if event.type() == QtCore.QEvent.LanguageChange:
            self.retranslateUi(self)
            #self.set_translatable_textes()
            
 
 
    def clear_inputs(self):
        'clear the various inputs after deletion of a session '
        self.targeted_original_gravity_value.setText('')
        self.targeted_bitterness_value.setText('') 
        self.boiling_time_value.setText('')
        self.batch_volume_edit.setText('')
        self.grain_temperature_edit.setText('') 
        self.mash_water_volume_edit.setText('')
        self.mash_sparge_water_volume_edit.setText('')
        self.strike_temperature_edit.setText('')
        self.zero_ibu_bar()
        self.zero_pitching_bar()           
        
    def clear_layouts(self):
        self.util.clearLayout(self.malt_layout)
        self.util.clearLayout(self.hop_layout)
        self.util.clearLayout(self.yeast_layout)
        self.util.clearLayout(self.rest_layout)
        
  
                
    def clean_results(self):     
        for i in range(self.malt_layout.count()):
            calculated_mass_edit=self.util.get_by_name_recursive(self.malt_layout.itemAt(i).layout(),'calculated_mass')
            if calculated_mass_edit: calculated_mass_edit.setText('')  
        self.strike_temperature_edit.setText('')
        self.mash_water_volume_edit.setText('')
        self.mash_sparge_water_volume_edit.setText('')  
        for i in range(self.hop_layout.count()):
            hidden_hop_rate=self.util.get_by_name_recursive(self.hop_layout.itemAt(i).layout(), 'hidden_hop_rate')
            if hidden_hop_rate: 
                hop_amount_edit=self.util.get_by_name_recursive(self.hop_layout.itemAt(i).layout(),'amount')
                if hop_amount_edit:
                    hop_amount_edit.setText('')
                    hop_amount_edit.setStyleSheet(sty.field_styles['calculated'])
                    
 
    def closeEvent(self,ev):
        self.recipeDialog.close()
        self.equipmentDialog.close()
        self.maltDialog.close()
        self.yeastDialog.close()
        self.hopDialog.close()
        self.restDialogCreate.close()
        self.feedback.close()
     
    
        
    def edit_session(self):
        if self.session_combo.currentText():
            self.set_feedback_editable()
    
    
    def explain_current_brewing_session(self):
        message=self.tr('''
    <h2>Brewing session dialog explanation</h2>
        
    <p>This part of the dialog allows you to set up a brewing session in order to register it afterward. 
    A brewing session is the implementation of a recipe on a given equipment with a specific batch volume.</p>
    
    <p>Filling a brewing session aims at 2 goals:
    <ol>
      <li>To calculate the various amount (hops, yeast, malts, water for mash, water for sparging, etc.) in order to implement a given recipe on a given equipment</li>
      <li>To keep a trace of your work in order to retrieve it later on</li>
    
    </ol>
        
    <p>You have to click the <strong>new button</strong> in order to make the dialog writable.<p>
        
    <p>Don't forget that before filling the form for a brewing session, you must a least \
    have one recipe and one equipment declared in your database. Use the menu Database \
    on the top of this window to create a recipe and an equipment.</p>
        
    <p>In this dialog, your have just to select a recipe and an equipment and \
    fill the writable fields. (See the Preferences in the menu to identify which fields\
    are writable or not and to change the background colors at will).</p>
        
    <p>Some fields for which filling is not always obvious are fitted with a question\
    mark button where additional guidance is useful. </p>

    <p>Once the brewing session has been saved, it is no longer possible to modify it and the user\
    is ready to associate a feedback to it in the bottom part of the dialog.</p>
    
    <p>The feedback can be modified and amended at any time.</p>
    
        
        '''
        )     
        self.util.alerte(message,QMessageBox.Information,self.tr('Info : Using the Current Brewing Session Dialog?'))   
                                 
                                                     
    def explain_ibu_bar(self):
        message =self.tr('''
        <h2>IBU bar explanation </h2>
        <p>IBU stands for International Bitterness Unit</p>
        <p>Before using the hop dialog the user has to select 
        a recipe, an equipment and define the batch volume.</p>
        
        <p>In the hop dialog, when the users enters a quantity of
        hop in the adopted field, the total bitterness is calculated anew.</p>
        
        <p>The Hop Bitterness Bar starts from 0 to twice the recipe
        targeted bitterness. Thus the recipe targeted
        bitterness is just in the middle of the bar and is 
        represented by a small black rectangle.</p>
        
        <p>Nevertheless, the user can decide to modify the amount of 
        hop  at any time. Then, the bitterness is 
         recalculated and the bar updated.
        The bar is displayed with a green background only if
        the actual bitterness stays in the range +-10%. </p>
        
        <p>Only Boil hopping and First wort hopping contribute to the bitterness.
        First Wort Hopping is hopping during the lautering and sparging of the 
        wort. Its contribution, according to John Palmer is roughly 110% of 
        a 60 min boil of the same amount.</p>
        ''' 
        ) 
        self.util.alerte(message,QMessageBox.Information,self.tr('Info : Using the Hop dialog?'))    
        
   
                
    def explain_yeast_bar(self): 
        message =self.tr('''
        <h2>Yeast Dialog explanation</h2>
        
        <p>Before using the yeast dialog the user has to select 
        a recipe, an equipment and define the batch volume.</p>
        
        <p>In the yeast dialog, when the users presses the calculate
        button, the recommended pitching rate is used along with
        the batch size to calculate the amount of yeast to use.</p>
        
        <p>The Yeast Pitching Bar starts from 0 to twice the recipe
        recommended pitching rate. Thus the recommended recipe 
        pitching rate is just in the middle of the bar and is 
        represented by a small black rectangle.</p>
        
        <p>Nevertheless, the user can decide to modify the amount of 
        yeast in the lower part of the yeast dialog. Then, the 
        actual pitching rate is recalculated and the bar updated.
        The bar is displayed with a green background only if
        the actual pitching rate stays in the range +-10%.</p> 
        ''' 
        )   
        self.util.alerte(message,QMessageBox.Information,self.tr('Info : Using the yeast dialog?')) 
                    
    def get_hop_amounts(self):
        'return a list of user defined hop amounts' 
        l=[]
        for i in range (self.hop_layout.count()):
            item = self.hop_layout.itemAt(i)
            if item:
                val_edit=self.util.get_by_name(item.layout(), 'amount')
                val=self.util.check_input(val_edit, False, self.tr('Hop amount at line'+str(i)+' is not readable. Please check your \
                input'), False, 0, vcst.MAX_VOLUME*vcst.MAX_HOP_RATE)
                l.append(val)
        return l   
    
    def hide_session_designation(self):
        widgets=self.util.get_included_widgets(self.current_session_intro_layout)
        for w in widgets:
            w.hide()   
  
                 
    def init_equipment_combo(self):
        self.equipment_combo.clear()  
        self.equipment_combo.addItem('')
        for key in self.equipment_key_list:
            eq = self.model.get_equipment(key)
            self.equipment_combo.addItem(eq.name)
       
        self.equipment_combo.currentIndexChanged.connect(self.load_equipment)
        self.equipment_combo.setEnabled(True)
        self.load_equipment()
        self.equipment_combo.setStyleSheet(vcst.MAIN_COMBO_SELECTION_STYLE)
        
    def init_font_set_db(self):
        pf=platform.system()  
        
        font_set=self.model.get_active_font_set()
        if font_set:
            self.active_font_set=font_set
        else:
            self.active_font_set=FontSet('tiny','active')
            self.model.save_font_set(FontSet('small','inactive'))
            self.model.save_font_set(FontSet('big','inactive'))
            self.model.save_font_set(FontSet('huge','inactive'))
            #self.model.save_font_set(FontSet('tiny','active'))
        
        self.model.set_in_use_fonts()    
            
       
             
                
                
            
        
    def init_recipe_combo(self):
        self.recipe_combo.clear()
        self.recipe_combo.addItem('')
        for key in self.recipe_key_list:
            rec=self.model.get_recipe(key)
            self.recipe_combo.addItem(rec.name)
        self.recipe_combo.currentIndexChanged.connect(self.load_recipe)
        self.recipe_combo.setEnabled(True)
        self.load_recipe()
        self.recipe_combo.setStyleSheet(vcst.MAIN_COMBO_SELECTION_STYLE)
        
    def init_session_combo(self): 
        
        self.session_key_list = self.model.session_list
        self.session_combo.clear()
        self.session_combo.addItem('')
        for key in self.session_key_list:
            session=self.model.get_session(key)
            self.session_combo.addItem(session.name)
        self.session_combo.currentIndexChanged.connect(self.load_session)
        
        self.session_combo.setStyleSheet(vcst.MAIN_COMBO_SELECTION_STYLE)
            
        
    def load_equipment(self):
        self.clean_results()
        if self.equipment_combo.currentText():
            self.equipment=self.model.get_equipment(self.equipment_combo.currentText())
            self.brewing_efficiency_value.setText(str(self.equipment.brewing_efficiency))
            self.brewing_efficiency=self.equipment.brewing_efficiency
        else:
            self.equipment=None
        
            
    def load_recipe(self):# connection established in init_recipe_combo
        self.clean_results()
        self.zero_ibu_bar()
        if self.recipe_combo.currentText():
            self.recipe=self.model.get_recipe(self.recipe_combo.currentText())
            
            #MALTS
            self.util.clearLayout(self.malt_layout)  
            self.malts=self.recipe.malts_in_mash
            for m in self.malts:
                malt=self.model.get_malt(m.malt)
                self.add_malt_view(malt, m.percentage) 
            
            self.rests=self.recipe.mash_rests    
            self.update_rest_view(self.recipe.mash_rests)
                  
            val='{0:.3f}'.format(self.recipe.targeted_original_gravity)
            self.targeted_original_gravity_value.setText(val)
            self.targeted_original_gravity=self.recipe.targeted_original_gravity
            self.boiling_time=self.recipe.boiling_time
            self.boiling_time_value.setText(str(self.boiling_time))
            
            #HOPS
            self.util.clearLayout(self.hop_layout)
            self.hops=self.recipe.hops_in_recipe
            for hir in self.hops:
                hop=self.model.get_hop(hir.hop)
                use=self.util.hop_usage_dic[hir.usage]
                self.add_hop_view(hop,use,hir.duration,hir.hop_rate)
            self.targeted_bitterness_value.setText(str(self.recipe.targeted_bitterness))  
            #self.calculate_hop_amounts()
            
            #YEAST
            self.util.clearLayout(self.yeast_layout)
            yeast=self.model.get_yeast(self.recipe.yeast_in_recipe.yeast)
            self.add_yeast_view(yeast,self.recipe.yeast_in_recipe.pitching_rate)
            if hasattr(self.recipe,'fermentation_explanation'):
                self.fermentation_explain_edit.setPlainText(self.recipe.fermentation_explanation)
                    
        else:
            self.recipe=None
            self.util.clearLayout(self.malt_layout)  
            self.targeted_original_gravity_value.setText('-.---')   
            self.targeted_bitterness_value.setText('--') 
            self.boiling_time_value.setText('---')          
   
    def load_session(self):
       
        
        if self.session_combo.currentText():
            self.current_session=self.session_combo.currentText()
            #to prevent GUI refresh on recipe or equipment change in DB
            self.view_session_button.setEnabled(True)
            v_unit=self.model.get_unit('water_volume')
            t_unit=self.model.get_unit('temperature')
            ma_unit=self.model.get_unit('malt_mass')
            h_unit=self.model.get_unit('hop_mass')
            self.mode_session='view'
            session=self.model.get_session(str(self.session_combo.currentText())) 
            self.util.create_session_sheet(session)
            self.set_ro_session()
            self.designation_edit.setText(session.name)
            self.show_session_designation()
            self.add_button.hide()
            
            self.targeted_original_gravity_value.setText(str(session.targeted_original_gravity))
            self.targeted_bitterness_value.setText(str(session.targeted_bitterness))
            self.boiling_time_value.setText(str(session.boiling_time))
            self.brewing_efficiency_value.setText(str(session.brewing_efficiency))
            
            #in order to avoid loading of a recipe that could have changed
            try:
                self.recipe_combo.currentIndexChanged.disconnect()
            except:
                pass    
            
            index = self.recipe_combo.findText(session.recipe, QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.recipe_combo.setCurrentIndex(index)
                
            #in order to avoid loading of an equipment that could have changed
            try:
                self.equipment_combo.currentIndexChanged.disconnect()
            except:
                pass    
            
            index = self.equipment_combo.findText(session.equipment, QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.equipment_combo.setCurrentIndex(index)
            self.batch_volume_edit.setText(str(self.util.convert_to(v_unit, session.batch_volume)))
            self.grain_temperature_edit.setText(str(self.util.convert_to(t_unit,session.grain_temperature)))
            

            malts=session.malts_in_session
            self.util.clearLayout(self.malt_layout)
            for i in range(len(malts)):
                m=self.model.get_malt(malts[i].name)
                self.add_malt_view(m,malts[i].percentage)
                item=self.malt_layout.itemAt(i)
                if item:
                    amount_w=self.util.get_by_name(item.layout(), 'calculated_mass')
                    if amount_w: 
                        amount_w.setText(str(self.util.convert_to(ma_unit,malts[i].amount)))
                        amount_w.setReadOnly(False)
                        amount_w.setStyleSheet(sty.field_styles['read_only']) 
                        
            self.mash_water_volume_edit.setText(str(self.util.convert_to(v_unit, session.mash_water_volume))  )    
            self.strike_temperature_edit.setText(str(self.util.convert_to(t_unit, session.strike_temperature)) )   
            self.mash_sparge_water_volume_edit.setText(str(self.util.convert_to(v_unit,session.mash_sparge_water_volume)))
                        
            rests=session.rests_in_session 
            self.util.clearLayout(self.rest_layout)
            for i in range(len(rests)):
                self.update_rest_view(rests)   
                
            hops=session.hops_in_session
            ibus=[]
            self.hop_calculate_button.hide()
            self.util.clearLayout(self.hop_layout)
            for i in range(len(hops)):
                his=hops[i]
                h=self.model.get_hop(his.name)
                #self.save_hop(h,his.usage,his.duration) 
                self.add_hop_view(h,his.usage,his.duration) 
                ibu=self.calculate_IBU_later(his.duration,session.batch_volume,
                                             session.targeted_original_gravity,his.amount,h.alpha_acid,session.batch_volume)
                ibus.append(ibu)
                  
                item=self.hop_layout.itemAt(i)
                if item:
                    amount_w=self.util.get_by_name(item.layout(), 'amount')   
                    if amount_w:
                        amount_w.setText(str(self.util.convert_to(h_unit,his.amount)))
                        amount_w.setReadOnly(True)
                        amount_w.setStyleSheet(sty.field_styles['read_only'])
                        try:
                            amount_w.editingFinished.disconnect()
                        except:
                            pass  
                        
             
            'YEAST'     
            yis=session.yeast_in_session
            self.util.clearLayout(self.yeast_layout)
            yeast=self.model.get_yeast(yis.name)
            if yeast: 
                self.add_yeast_view(yeast,yis.recommended_pitching_rate,yis.amount,False)
          
            for i in range(len(hops)):
                item=self.hop_layout.itemAt(i)
                if item:
                    calculated_ibu_w=self.util.get_by_name(item.layout(), 'calculated_IBU')
                    val='{0:.1f}'.format(ibus[i])
                    if calculated_ibu_w: calculated_ibu_w.setText(val)
                 
            self.update_ibu_bar(session.targeted_bitterness)
           
            self.edit_feedback_button.setEnabled(True)
            
        else: self.view_session_button.setEnabled(False)   
        
        
    def new_session(self):
        'the hop_calculate_button can be hidden when displaying a past session'
        self.hop_calculate_button.show()
        self.init_session_combo()#to make the previous selection disappear
        #self.hide_session_feedback()
        '''
        widgets=self.util.get_included_widgets(self.feedback_groupbox_layout)
        for w in widgets:
            w.hide()        
        '''    
        self.hide_session_designation() 
        self.set_editable_session()
        self.mode_session='create'
    
    def on_model_changed_main(self,target):    
        
        
        if (self.mode_session=='create' and target == 'recipe'):
        
            'update view after a recipe list change in model'
            self.recipe_key_list=self.model.recipe_list
            if self.recipe_combo.currentText():
                mem_selected=self.recipe_combo.currentText()
                self.init_recipe_combo()
                self.clean_results()
                index = self.recipe_combo.findText(mem_selected, QtCore.Qt.MatchFixedString)
                if index >= 0:
                    self.recipe_combo.setCurrentIndex(index)
            self.batch_volume_edit.setText('') 
            
        if (self.mode_session == 'create' and target == 'equipment'):
            'update vcst after a malt list change in model'
            self.equipment_key_list=self.model.equipment_list
            if self.equipment_combo.currentText():
                mem_selected=self.equipment_combo.currentText()
                self.init_equipment_combo()
                self.clean_results()
                index = self.equipment_combo.findText(mem_selected, QtCore.Qt.MatchFixedString)
                if index >= 0:
                    self.equipment_combo.setCurrentIndex(index) 
        if target == 'style':
            self.set_active_colors()
            self.maltDialog = MaltDialog(self.model,self.controller,self.util)    
        if target == 'fontset':
            if (self.model.in_use_fonts):
                self.set_fonts()  
    
    def open_session_sheet(self):
        if(os.path.isfile('session_sheet.html')):
            webbrowser.open('session_sheet.html')
                        
                    
    def remove_session(self):
        session=self.session_combo.currentText()
        if session: self.model.remove_session(session)
        self.init_session_combo()
        self.set_disable_session()
        self.clear_layouts()
        self.clear_inputs()
        #self.hide_session_feedback()
                
        
    def save_session(self):
        v_unit=self.model.get_unit('water_volume')
        t_unit=self.model.get_unit('temperature')
        m_unit=self.model.get_unit('malt_mass')
        h_unit=self.model.get_unit('hop_mass')
        recipe=self.recipe_combo.currentText()
        if not recipe: 
            self.util.alerte(self.tr('You have not chosen a recipe. Please chose one'))
            return
        equipment=self.equipment_combo.currentText() 
        if not equipment:
            self.util.alerte(self.tr('You have not chosen an equipment. Please chose one'))  
            return
        
        format= "%a %b %d %H:%M %Y"
        today=datetime.datetime.today()
        formated_date=today.strftime(format)
        designation= formated_date+' — '+recipe+ ' – '+equipment
        
        batch_volume=self.util.check_input(self.batch_volume_edit, False, self.tr('Batch Volume'),False, 0, vcst.MAX_VOLUME,None,v_unit) 
        if not batch_volume: return#alert message is included in check_input
        
        grain_temperature=self.util.check_input(self.grain_temperature_edit, False,self.tr('Grain Temperature'), False, 0,vcst.MAX_GRAIN_TEMPERATURE,None,t_unit)
        if not grain_temperature: return
        
        #all the following values are not entered by user
        targeted_original_gravity=float(self.targeted_original_gravity_value.text())
        targeted_bitterness=float(self.targeted_bitterness_value.text())
        boiling_time=float(self.boiling_time_value.text())
        brewing_efficiency = float(self.brewing_efficiency_value.text())
        
        'SAVE MALT VALUES'
        malts_in_session=[]
        for i in range (self.malt_layout.count()):
            item=self.malt_layout.itemAt(i)
            if item:
                name_w=self.util.get_by_name(item.layout(), 'name')
                if name_w: name=name_w.text()
                percentage_w=self.util.get_by_name(item.layout(), 'percentage')
                if percentage_w: percentage=float(percentage_w.text())
                amount_w=self.util.get_by_name(item.layout(), 'calculated_mass')
                if amount_w:
                    amount=self.util.check_input(amount_w, False, self.tr('Malt Amount '+str(i)), False, 0, vcst.MAX_VOLUME*vcst.MAX_MALT_RATE, True,m_unit)
                    if not amount:return
                mis=MaltInSession(name,percentage,amount)
                malts_in_session.append(mis)
        
        'SAVE REST DEFINITION'
        rests_in_session=[]
        for i in range (self.rest_layout.count()):
            item = self.rest_layout.itemAt(i)
            if item:
                purpose_w=self.util.get_by_name(item.layout(), 'purpose')
                if purpose_w: purpose=purpose_w.text()
                duration_w=self.util.get_by_name(item.layout(), 'duration')
                if duration_w: duration=float(duration_w.text())
                temperature_w=self.util.get_by_name(item.layout(), 'temperature')
                if temperature_w: temperature=self.util.convert_from(t_unit, float(temperature_w.text()))
                ris=RestInSession(purpose,duration,temperature)
                rests_in_session.append(ris)
        
        'SAVE HOP VALUES'        
        hops_in_session=[]  
        for i in range (self.hop_layout.count()):
            item = self.hop_layout.itemAt(i)
            if item:
                name_w=self.util.get_by_name(item.layout(), 'name')
                if name_w: name=name_w.text()
                usage_w=self.util.get_by_name(item.layout(), 'usage')
                if usage_w: 
                    usage=self.util.get_usage_key(usage_w.text())
                duration_w=self.util.get_by_name(item.layout(), 'duration')
                
                'Only boiling case has duration'
                if duration_w and usage== vcst.HOP_BOILING_HOPPING: 
                    duration=self.util.check_input(duration_w,False, self.tr('Hop duration '+str(i)), False, 0, vcst.MAX_BOILING_TIME)
                    if not duration: return
                    
                amount_w=self.util.get_by_name(item.layout(), 'amount')
                if amount_w:
                    amount=self.util.check_input(amount_w, False, self.tr('Hop Amount '+str(i)),False, 0, vcst.MAX_VOLUME*vcst.MAX_HOP_RATE,None,h_unit)
                    if not amount: return
                his=HopInSession(name,usage,duration,amount)
                hops_in_session.append(his)
                      
        'SAVE YEAST VALUES'   
        ya_unit=self.model.get_unit('yeast_mass')
        ya_unit_label=self.util.get_unit_label(ya_unit)
        yr_unit=self.model.get_unit('yeast_rate')
        yr_unit_label=self.util.get_unit_label(yr_unit)
        yeast_name_w=self.util.get_by_name_recursive(self.yeast_layout, 'name')
        if yeast_name_w: yeast_name=yeast_name_w.text()
        rate_edit=self.util.get_by_name_recursive(self.yeast_layout, 'adopted_pitching_rate')
        if rate_edit: 
    
            rate=self.util.check_input(rate_edit, False,self.tr('Adopted Pitching Rate'), False,0,2,None,yr_unit)#float(rate_edit.text())
        
        adopted_yeast_amount_edit=self.util.get_by_name_recursive(self.yeast_layout,'adopted_amount')
        if not adopted_yeast_amount_edit: 
            self.util.alerte(self.tr('Could not find the adopted yeast amount. This should never happen. Please file a bug'))
            return
        else:
            adopted_yeast_amount=self.util.check_input(adopted_yeast_amount_edit, False, self.tr('Adopted Yeast Amount. \
             Please use the calculate button and if you want change the value '), False,0,vcst.MAX_VOLUME*vcst.MAX_PITCHING_RATE,None,ya_unit)
            if not isinstance(adopted_yeast_amount,float):
                return
            yeast_in_session=YeastInSession(yeast_name,adopted_yeast_amount,rate)
        
        'all what will reside in db is in liter'    
        mash_water_volume=self.util.check_input(self.mash_water_volume_edit,False, self.tr('Mash Water Volume'),False,0,vcst.MAX_VOLUME,None,v_unit)    
        if not mash_water_volume: return
        strike_temperature=self.util.check_input(self.strike_temperature_edit, False, self.tr('Strike Température'), False,0,100,None,t_unit)
        if not strike_temperature: return
        mash_sparge_water_volume=self.util.check_input(self.mash_sparge_water_volume_edit, False, self.tr('Sparge Water Volume'), False, 0,vcst.MAX_VOLUME,None,v_unit)
        equipment_object=self.model.get_equipment(equipment)   
        if equipment: boiler_dead_space=equipment_object.boiler_dead_space
        ts=time.time()
        print('recipe before save ')
        print(recipe)
        
        session=Session(designation,ts,recipe,equipment,batch_volume,grain_temperature,
                        targeted_original_gravity,targeted_bitterness,boiling_time,brewing_efficiency,
                        malts_in_session,rests_in_session,hops_in_session,yeast_in_session,
                        mash_water_volume,strike_temperature,mash_sparge_water_volume,boiler_dead_space)
        
        self.model.save_session(session)
        self.init_session_combo()
        index = self.session_combo.findText(designation, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.session_combo.setCurrentIndex(index)
        #self.util.create_session_sheet(session)
        
            
            
    def save_session_feedback(self):
        
        designation=self.designation_edit.text()
        session=self.model.get_session(designation)
        if not session: 
            return
        feedback_water_treatment_text=self.feedback_water_treatment_textedit.toPlainText()
        session.feedback_water_treatment_text=feedback_water_treatment_text
        feedback_mash_ph=self.util.check_input(self.feedback_mash_PH_edit_2, False, self.tr('Feedback Mash PH'), True, 3, 7)
        session.feedback_mash_ph=feedback_mash_ph
        feedback_preboil_volume=self.util.check_input(self.feedback_preboil_volume_edit_2, False, self.tr('Feedback Preboil Volume'), True, 0, vcst.MAX_VOLUME)
        session.feedback_preboil_volume=feedback_preboil_volume
        feedback_original_gravity=self.util.check_input(self.feedback_original_gravity_edit_2, False, self.tr('Feedback Original Gravity'), True, 1, vcst.MAX_OG)
        session.feedback_original_gravity=feedback_original_gravity
        feedback_fermentor_volume=self.util.check_input(self.feedback_fermentor_volume_edit, False, self.tr('Feedback Fermentor Volume'), True, 0, vcst.MAX_VOLUME)
        session.feedback_fermentor_volume=feedback_fermentor_volume
        self.model.save_session(session)
        self.show_session_feedback()
     
     
    def select_combo_by_text(self,combo,text):    
        index = combo.findText(text, QtCore.Qt.MatchFixedString)
        if index >= 0:
            combo.setCurrentIndex(index) 
            
    def set_active_colors(self):
        'This function is called at init time of mainwindow and also on model changed'
        self.active_colors={}
        'if style in db then use it, otherwise use default'
        for key in vcst.FIELD_DEFAULT_COLORS:
            if key in self.style_key_list:
                self.active_colors[key]=self.model.get_style(key)
            else:
                self.active_colors[key]=vcst.FIELD_DEFAULT_COLORS[key]            
                
        sty.field_styles['editable']="background-color:"+self.active_colors['editable'][0]+\
        ";color:"+self.active_colors['editable'][1]+";" 
        sty.field_colors['editable']=[self.active_colors['editable'][0],self.active_colors['editable'][1]]
        
        sty.field_styles['calculated']="background-color:"+self.active_colors['calculated'][0]+\
        ";color:"+self.active_colors['calculated'][1]+";"
        sty.field_colors['calculated']=[self.active_colors['calculated'][0],self.active_colors['calculated'][1]]
        
        sty.field_styles['read_only']="background-color:"+self.active_colors['read_only'][0]+\
        ";color:"+self.active_colors['read_only'][1]+";" 
        sty.field_colors['read_only']=[self.active_colors['read_only'][0],self.active_colors['read_only'][1]]
        
        sty.field_styles['min_max_allowed']="background-color:"+self.active_colors['min_max_allowed'][0]+\
        ";color:"+self.active_colors['min_max_allowed'][1]+";"
        sty.field_colors['min_max_allowed']=[self.active_colors['min_max_allowed'][0],self.active_colors['min_max_allowed'][1]]
        
        sty.field_styles['min_max_advised']="background-color:"+self.active_colors['min_max_advised'][0]+\
        ";color:"+self.active_colors['min_max_advised'][1]+";"    
        sty.field_colors['min_max_advised']=[self.active_colors['min_max_advised'][0],self.active_colors['min_max_advised'][1]]   
     
                  
    def set_calculated_style(self):
        
        self.mash_water_volume_edit.setStyleSheet(sty.field_styles['calculated'])
        self.mash_water_volume_edit.setReadOnly(True)
        self.strike_temperature_edit.setStyleSheet(sty.field_styles['calculated'])
        self.strike_temperature_edit.setReadOnly(True)
        self.mash_sparge_water_volume_edit.setStyleSheet(sty.field_styles['calculated'])
        self.mash_sparge_water_volume_edit.setReadOnly(True)
        
        
    def set_connections(self):
        self.actionEdit_Malt_Database.triggered.connect(self.show_malt_dialog)
        self.actionEdit_Hop_Database.triggered.connect(self.show_hop_dialog)
        self.actionEdit_Rest_Database.triggered.connect(self.show_rest_dialog_create)
        self.actionEdit_Yeast_Database.triggered.connect(self.show_yeast_dialog)
        self.actionCustomize_colors.triggered.connect(self.show_color_dialog)
        self.actionCustomize_Font_Size.triggered.connect(self.show_font_size_dialog)
        
        
        self.actionSet_Units_at_Next_Startup.triggered.connect(self.set_units_at_startup)
        self.actionChange_language.triggered.connect(self.request_change_language)
        self.actionImport_Export_Databases.triggered.connect(self.show_import_export_dialog)
        self.actionEdit_Recipe_Database.triggered.connect(self.show_recipe_dialog)
        self.actionEdit_Equipment_Database.triggered.connect(self.show_equipment_dialog)
        self.actionView_Help.triggered.connect(self.show_help)
        
        

        self.view_session_button.clicked.connect(self.open_session_sheet)
        self.calculate_button.clicked.connect(self.calculate_malt_amounts)
        self.hop_calculate_button.clicked.connect(self.calculate_hop_amounts)
        self.batch_volume_edit.editingFinished.connect(self.batch_volume_changed)    
        self.bar_button.clicked.connect(self.explain_ibu_bar)
        self.main_help_button.clicked.connect(self.explain_current_brewing_session)
        self.pitching_bar_button.clicked.connect(self.explain_yeast_bar)
        self.add_button.clicked.connect(self.save_session)
        self.new_button.clicked.connect(self.new_session)
        self.delete_button.clicked.connect(self.remove_session)  
        self.edit_feedback_button.clicked.connect(self.show_feedback) 
        #self.edit_button.clicked.connect(self.edit_session)  
        #self.feedback_save_button.clicked.connect(self.save_session_feedback)   
        self.batch_volume_edit.editingFinished.connect(self.calculate_hop_amounts)    
     
    def set_disable_session(self):
            self.hide_session_designation()
            self.batch_volume_edit.setStyleSheet(sty.field_styles['read_only'])
            self.batch_volume_edit.setEnabled(False)
            self.grain_temperature_edit.setEnabled(False)
            self.grain_temperature_edit.setStyleSheet(sty.field_styles['read_only'])
            self.recipe_combo.setEnabled(False)
            self.equipment_combo.setEnabled(False)
            self.calculate_button.setEnabled(False)
            self.hop_calculate_button.setEnabled(False)   
        
        
    def set_editable_session(self):
        'reset the form for session creation'
       
        
        self.batch_volume_edit.setText('')
        self.batch_volume_edit.setReadOnly(False)
        self.batch_volume_edit.setStyleSheet(sty.field_styles['editable'])
        self.batch_volume_edit.setEnabled(True)
        
        self.grain_temperature_edit.setReadOnly(False) 
        self.grain_temperature_edit.setStyleSheet(sty.field_styles['editable'])
        self.grain_temperature_edit.setEnabled(True)
        self.grain_temperature_edit.setText('')
        
        self.calculate_button.setEnabled(True)
        self.hop_calculate_button.setEnabled(True)
        
        self.targeted_original_gravity_value.setText('-.---')
        self.targeted_bitterness_value.setText('--')
        self.boiling_time_value.setText('--')
        self.brewing_efficiency_value.setText('--')
        
        self.init_recipe_combo()
        self.init_equipment_combo()
        
        self.mash_water_volume_edit.setText('')
        self.mash_water_volume_edit.setReadOnly(True)
        self.mash_water_volume_edit.setStyleSheet(sty.field_styles['calculated'])
        
        self.strike_temperature_edit.setText('')
        self.strike_temperature_edit.setReadOnly(True)
        self.strike_temperature_edit.setStyleSheet(sty.field_styles['calculated'])
        
        self.mash_sparge_water_volume_edit.setText('')
        self.mash_sparge_water_volume_edit.setReadOnly(True)
        self.mash_sparge_water_volume_edit.setStyleSheet(sty.field_styles['calculated'])
        
        self.util.clearLayout(self.malt_layout)
        self.calculate_button.show()
        self.util.clearLayout(self.rest_layout)
        self.util.clearLayout(self.hop_layout)
        self.util.clearLayout(self.yeast_layout)
        
        self.add_button.show()
        self.add_button.setEnabled(True)
        
     
    
            
            
            
    
            
     
        
    def set_feedback_editable(self):
        self.feedback_water_treatment_textedit.setStyleSheet(sty.field_styles['editable'])   
        self.feedback_water_treatment_textedit.setEnabled(True) 
        self.feedback_mash_PH_edit_2.setStyleSheet(sty.field_styles['editable']) 
        self.feedback_mash_PH_edit_2.setEnabled(True)
        self.feedback_preboil_volume_edit_2.setStyleSheet(sty.field_styles['editable']) 
        self.feedback_preboil_volume_edit_2.setEnabled(True)
        self.feedback_original_gravity_edit_2.setStyleSheet(sty.field_styles['editable']) 
        self.feedback_original_gravity_edit_2.setEnabled(True)
        self.feedback_fermentor_volume_edit.setStyleSheet(sty.field_styles['editable'])  
        self.feedback_fermentor_volume_edit.setEnabled(True)
        self.feedback_save_button.show()
        self.edit_button.hide()   
        
        
    def set_fonts(self):
        self.menubar.setFont(self.model.in_use_fonts['field'])
        self.menuHelp.setFont(self.model.in_use_fonts['field'])
        self.menuSettings.setFont(self.model.in_use_fonts['field'])
        self.menuFile.setFont(self.model.in_use_fonts['field'])
        self.menuDatabase.setFont(self.model.in_use_fonts['field'])
        self.menuImport_Export.setFont(self.model.in_use_fonts['field'])
        #self.menuChoose_Language.setFont(self.model.in_use_fonts['field'])
        self.batch_volume_edit.setFont(self.model.in_use_fonts['field'])
        self.grain_temperature_edit.setFont(self.model.in_use_fonts['field'])
        self.mash_water_volume_edit.setFont(self.model.in_use_fonts['field'])
        self.strike_temperature_edit.setFont(self.model.in_use_fonts['field'])
        self.mash_sparge_water_volume_edit.setFont(self.model.in_use_fonts['field'])
        self.recipe_combo.setFont(self.model.in_use_fonts['field'])
        self.equipment_combo.setFont(self.model.in_use_fonts['field'])
        
        self.delete_button.setFont(self.model.in_use_fonts['button'])
        self.view_session_button.setFont(self.model.in_use_fonts['button'])
        self.new_button.setFont(self.model.in_use_fonts['button'])
        self.designation_label.setFont(self.model.in_use_fonts['field'])
        
        self.current_brewing_session_label.setFont(self.model.in_use_fonts['very_big_title']) 
        self.choose_session_label.setFont(self.model.in_use_fonts['title_slanted'])
        self.new_session_label.setFont(self.model.in_use_fonts['title_slanted'])
        
        self.batch_volume_label.setFont(self.model.in_use_fonts['field'])  
        self.batch_volume_unit_label.setFont(self.model.in_use_fonts['field'])
        self.grain_temperature_label.setFont(self.model.in_use_fonts['field'])
        self.grain_temperature_unit_label.setFont(self.model.in_use_fonts['field'])  
        self.add_button.setFont(self.model.in_use_fonts['button'])
        
        self.recipe_label.setFont(self.model.in_use_fonts['field'])
        self.equipment_label.setFont(self.model.in_use_fonts['field'])
        
        self.boiling_time_label.setFont(self.model.in_use_fonts['field'])
        self.boiling_time_value.setFont(self.model.in_use_fonts['field'])
        self.boiling_time_unit_label.setFont(self.model.in_use_fonts['field'])
        self.recipe_label.setFont(self.model.in_use_fonts['field'])
        self.targeted_original_gravity_label.setFont(self.model.in_use_fonts['field'])
        self.targeted_original_gravity_value.setFont(self.model.in_use_fonts['field'])
        self.targeted_bitterness_label.setFont(self.model.in_use_fonts['field'])
        self.targeted_bitterness_value.setFont(self.model.in_use_fonts['field'])
        self.targeted_bitterness_unit_label.setFont(self.model.in_use_fonts['field'])
        self.brewing_efficiency_label.setFont(self.model.in_use_fonts['field'])
        self.brewing_efficiency_value.setFont(self.model.in_use_fonts['field'])
        
        self.mash_label.setFont(self.model.in_use_fonts['big_title'])
        self.malt_label.setFont(self.model.in_use_fonts['button'])
        self.calculate_button.setFont(self.model.in_use_fonts['button'])
        
        self.mash_rest_label.setFont(self.model.in_use_fonts['title'])
        self.mash_water_volume_label.setFont(self.model.in_use_fonts['field'])
        self.mash_water_volume_unit_label.setFont(self.model.in_use_fonts['field'])
        
        self.strike_temperature_label.setFont(self.model.in_use_fonts['field'])
        self.strike_temperature_unit_label.setFont(self.model.in_use_fonts['field'])
        
        self.mash_sparge_water_volume_label.setFont(self.model.in_use_fonts['field'])
        self.mash_sparge_water_volume_unit_label.setFont(self.model.in_use_fonts['field'])
        
        self.boil_label.setFont(self.model.in_use_fonts['big_title'])
        self.hop_label.setFont(self.model.in_use_fonts['title'])
        self.ibu_bar_label.setFont(self.model.in_use_fonts['field'])
        self.hop_calculate_button.setFont(self.model.in_use_fonts['button'])
        
        self.adjunct_label.setFont(self.model.in_use_fonts['title'])
        
        self.pitching_label.setFont(self.model.in_use_fonts['big_title'])
        self.yeast_label.setFont(self.model.in_use_fonts['title'])
        self.pitching_rate_bar_label.setFont(self.model.in_use_fonts['field'])
        
        '''
        self.feedback_label.setFont(self.model.in_use_fonts['very_big_title'])
        self.feedback_water_treatment_label.setFont(self.model.in_use_fonts['big_title'])
        self.feedback_observed_data_label.setFont(self.model.in_use_fonts['big_title'])
        self.feedback_mash_PH_label_2.setFont(self.model.in_use_fonts['field'])
        self.feedback_preboil_volume_label_2.setFont(self.model.in_use_fonts['field'])
        self.feedback_preboil_volume_unit_label_2.setFont(self.model.in_use_fonts['field'])
        self.feedback_original_gravity_label_2.setFont(self.model.in_use_fonts['field'])
        self.feedback_fermentor_volume_label_2.setFont(self.model.in_use_fonts['field'])
        self.feedback_fermentor_volume_unit_label_2.setFont(self.model.in_use_fonts['field']) 
        self.feedback_save_button.setFont(self.model.in_use_fonts['button'])
        '''
            
        self.set_malt_fonts() 
        self.set_hop_fonts()
        self.set_yeast_fonts()
        self.set_rest_fonts()
     
    def set_hop_fonts(self):
        for i in range (self.hop_layout.count()):
            item = self.hop_layout.itemAt(i)
            if item:
                name_w=self.util.get_by_name(item.layout(), 'name')
                if name_w: name_w.setFont(self.model.in_use_fonts['field'])
                
                desc_w=self.util.get_by_name(item.layout(), 'desc')
                if desc_w: desc_w.setFont(self.model.in_use_fonts['field'])
                
                usage_w=self.util.get_by_name(item.layout(), 'usage')
                if usage_w: usage_w.setFont(self.model.in_use_fonts['field'])
                
                duration_w=self.util.get_by_name(item.layout(), 'duration')
                if duration_w: duration_w.setFont(self.model.in_use_fonts['field'])
                
                time_unit_w=self.util.get_by_name(item.layout(), 'time_unit')
                if time_unit_w: time_unit_w.setFont(self.model.in_use_fonts['field'])
                
                advised_label_w=self.util.get_by_name(item.layout(), 'advised_label')
                if advised_label_w: advised_label_w.setFont(self.model.in_use_fonts['field'])
                
                advised_amount_w=self.util.get_by_name(item.layout(), 'advised_amount')
                if advised_amount_w: advised_amount_w.setFont(self.model.in_use_fonts['field'])
                
                advised_unit_w=self.util.get_by_name(item.layout(), 'advised_unit')
                if advised_unit_w: advised_unit_w.setFont(self.model.in_use_fonts['field'])
                
                amount_label_w=self.util.get_by_name(item.layout(), 'amount_label')
                if amount_label_w: amount_label_w.setFont(self.model.in_use_fonts['field'])
                
                amount_unit_label_w=self.util.get_by_name(item.layout(), 'amount_unit_label')
                amount_unit_label_w.setFont(self.model.in_use_fonts['field'])
               
                    
                amount_w=self.util.get_by_name(item.layout(), 'amount')
                if amount_w: amount_w.setFont(self.model.in_use_fonts['field'])
                
                calculated_IBU_w=self.util.get_by_name(item.layout(), 'calculated_IBU')
                calculated_IBU_w.setFont(self.model.in_use_fonts['field'])
                
                calculated_IBU_unit_w=self.util.get_by_name(item.layout(), 'calculated_IBU_unit')
                calculated_IBU_unit_w.setFont(self.model.in_use_fonts['field'])
        
        
         
    def set_input_style(self):
        self.batch_volume_edit.setStyleSheet(sty.field_styles['editable'])
        self.grain_temperature_edit.setStyleSheet(sty.field_styles['editable'])  
            
        
    def set_malt_fonts(self):
        for i in range (self.malt_layout.count()):
            item=self.malt_layout.itemAt(i)
            if item:
                name_w=self.util.get_by_name(item.layout(), 'name')
                if name_w: name_w.setFont(self.model.in_use_fonts['field'])
                percentage_w=self.util.get_by_name(item.layout(), 'percentage')
                if percentage_w: percentage_w.setFont(self.model.in_use_fonts['field'])
                percentage_unit_w=self.util.get_by_name(item.layout(),'percentage_unit')
                if percentage_unit_w: percentage_unit_w.setFont(self.model.in_use_fonts['field'])
                amount_w=self.util.get_by_name(item.layout(), 'calculated_mass')
                if amount_w:amount_w.setFont(self.model.in_use_fonts['field'])
                amount_unit_w=self.util.get_by_name(item.layout(),'calculated_mass_unit')
                if amount_unit_w:amount_unit_w.setFont(self.model.in_use_fonts['field'])        
        
   
         
    def request_change_language(self):
        self.model.drop_languages()
        mb=QMessageBox()
        mb.setIcon(QMessageBox.Warning)
        mb.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        mb.setText(self.tr('You made a request to change the language!'))
        mb.setInformativeText(self.tr('Do you really want to change it? If no, just use the Ignore button. \
        Otherwise use the Ok button and the application will restart instantly.'))
        mb.setStandardButtons(QMessageBox.Ok|QMessageBox.Ignore)
        ret =mb.exec_()
        
        if ret==QMessageBox.Ok:
            app=QApplication.instance()
            app.exit( MainWindow.EXIT_CODE_REBOOT )
       
   
        
    def set_language(self,code):
        print('language in set_language is '+code)
        app=QApplication.instance()
        app.removeTranslator(self.translator)
        self.translator.load(os.path.join(self.trad_path,code))
        '''reinstall of translator triggers an changeEvent that should be used in each widget that 
        needs translation. See changeEvent function in each widget'''
        app.installTranslator(self.translator)
            
        
    def set_rest_fonts(self):
        for i in range(self.rest_layout.count()):
            item=self.rest_layout.itemAt(i)
            if item:
                duration_w=self.util.get_by_name(item.layout(),'duration')
                duration_w.setFont(self.model.in_use_fonts['field'])
                duration_unit_w=self.util.get_by_name(item.layout(), 'duration_unit')
                duration_unit_w.setFont(self.model.in_use_fonts['field'])
                temperature_w=self.util.get_by_name(item.layout(), 'temperature')
                temperature_w.setFont(self.model.in_use_fonts['field'])
                temperature_unit_w=self.util.get_by_name(item.layout(), 'temperature_unit')
                temperature_unit_w.setFont(self.model.in_use_fonts['field'])
        
    def  set_ro_session(self):
        'set readonly at upper level i.e. the session level'
        self.designation_edit.setReadOnly(True)
        self.designation_edit.setStyleSheet(sty.field_styles['read_only'])
        self.add_button.hide()
        self.recipe_combo.setEnabled(False)
        self.equipment_combo.setEnabled(False)
        self.calculate_button.hide()
        self.batch_volume_edit.setReadOnly(True)
        self.batch_volume_edit.setStyleSheet(sty.field_styles['read_only'])  
        try:
            self.batch_volume_edit.editingFinished.disconnect()
        except:
            pass    
        self.grain_temperature_edit.setReadOnly(True)
        self.targeted_original_gravity_value.setStyleSheet(sty.field_styles['read_only'])
        self.grain_temperature_edit.setStyleSheet(sty.field_styles['read_only']) 
        self.mash_water_volume_edit.setReadOnly(True)
        self.mash_water_volume_edit.setStyleSheet(sty.field_styles['read_only'])
        self.strike_temperature_edit.setReadOnly(True)
        self.strike_temperature_edit.setStyleSheet(sty.field_styles['read_only'])
        self.mash_sparge_water_volume_edit.setReadOnly(True)
        self.mash_sparge_water_volume_edit.setStyleSheet(sty.field_styles['read_only'])
        
        for i in range (self.hop_layout.count()):
            item=self.hop_layout.itemAt(i)
            if item:
                hidden_hop_rate=self.util.get_by_name_recursive(item.layout(), 'hidden_hop_rate')
                hop_amount_edit=self.util.get_by_name_recursive(item.layout(), 'amount')
                if hidden_hop_rate:
                    hop_amount_edit.setReadOnly(True)
                    hop_amount_edit.setStyleSheet(sty.field_styles['calculated'])
                    try:
                        hop_amount_edit.editingFinished.disconnect()
                    except:
                        pass    
                else:
                    hop_amount_edit.setReadOnly(True)
                    hop_amount_edit.setStyleSheet(sty.field_styles['read_only']) 
                    try:
                        hop_amount_edit.editingFinished.disconnect()
                    except:
                        pass    
        for i in range(self.rest_layout.count()):
            item= self.rest_layout.itemAt(i)
            if item:
                temperature_edit=self.util.get_by_name_recursive(item.layout(), 'temperature')
                if temperature_edit:
                    temperature_edit.setReadOnly(True)
                    temperature_edit.setStyleSheet(sty.field_styles['read_only'])
        adopted_yeast_amount_edit=self.util.get_by_name_recursive(self.yeast_layout, 'adopted_amount')
        if adopted_yeast_amount_edit: 
            adopted_yeast_amount_edit.setReadOnly(True)
            adopted_yeast_amount_edit.setStyleSheet(sty.field_styles['read_only'])
            try:
                adopted_yeast_amount_edit.editingFinished.disconnect()
            except:
                pass  
        try:
            yeast_calculate_button=  self.util.get_by_name_recursive(self.yeast_layout, 'calculate_button')
            if yeast_calculate_button: 
                yeast_calculate_button.clicked.disconnect()    
        except:
            pass   
        self.fermentation_explain_edit.setStyleSheet(sty.field_styles['read_only'])     
             
    def set_subscriptions(self):
        self.model.subscribe_model_changed(['malt','hop','yeast','recipe','equipment','session','style','fontset'],self.on_model_changed_main)
        
           
    def set_tooltips (self):
        return
        if self.equipment:
            text='Brewing efficiency: '+str(self.equipment.brewing_efficiency) +\
             '\nBoiler size: '+str(self.equipment.boiler_size)+\
             '\nBoiler dead space: '+str(self.equipment.boiler_dead_space)+\
             '\nFermentor size: '+str(self.equipment.fermentor_size)+\
             '\nFermentor dead space: '+str(self.equipment.fermentor_dead_space)
            self.equipment_combo.setToolTip(text)
            
   
       
    def set_units(self,units):
        for u in units:
            self.model.update_unit(u.name,u.unit)
           
    def set_units_at_startup(self):
        self.model.drop_units()   
        #self.util.alerte(self.tr('Your request for changing the unit system has been taken into account. Please restart the application and you will be invited to enter your new units.'), QMessageBox.Warning, 'Request for changing units') 
        mb=QMessageBox()
        mb.setIcon(QMessageBox.Warning)
        mb.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        mb.setText(self.tr('You made a request to change units!'))
        mb.setInformativeText(self.tr('Do you really want to change them? If no, just use the Ignore button. \
        Otherwise use the Ok button and the application will restart instantly.'))
        mb.setStandardButtons(QMessageBox.Ok|QMessageBox.Ignore)
        
        ret =mb.exec_()
        
        if ret==QMessageBox.Ok:
            app=QApplication.instance()
            app.exit( MainWindow.EXIT_CODE_REBOOT )
        
        
        
    def set_unit_labels(self):
        t_unit=self.model.get_unit('temperature')
        if t_unit  : t_unit_label=self.util.get_unit_label(t_unit) 
        v_unit=self.model.get_unit('water_volume')
        if v_unit: v_unit_label=self.util.get_unit_label(v_unit)
        self.mash_water_volume_unit_label.setText(v_unit_label)   
        self.mash_sparge_water_volume_unit_label.setText(v_unit_label) 
        self.strike_temperature_unit_label.setText(t_unit_label)
        self.grain_temperature_unit_label.setText(t_unit_label)  
        self.batch_volume_unit_label.setText(v_unit_label)
        
            
    def set_yeast_fonts(self):
        for i in range (self.yeast_layout.count()):
            item = self.yeast_layout.itemAt(i)
            if item:
                
                maker_w=self.util.get_by_name(item.layout(), 'maker')
                if maker_w: maker_w.setFont(self.model.in_use_fonts['field']) 
                
                name_w=self.util.get_by_name(item.layout(), 'name')
                if name_w: name_w.setFont(self.model.in_use_fonts['field'])
                
                desc_w=self.util.get_by_name(item.layout(), 'desc')
                if desc_w: desc_w.setFont(self.model.in_use_fonts['field'])
                
                form_w=self.util.get_by_name(item.layout(), 'form')
                if form_w: form_w.setFont(self.model.in_use_fonts['field'])
                
                temperature_label_w=self.util.get_by_name_recursive(item.layout(), 'temperature_label')
                if temperature_label_w: temperature_label_w.setFont(self.model.in_use_fonts['field'])
                
                max_allowed_temperature_w=self.util.get_by_name_recursive(item.layout(), 'max_allowed_temperature')
                if max_allowed_temperature_w: max_allowed_temperature_w.setFont(self.model.in_use_fonts['field'])
                
                min_allowed_temperature_w=self.util.get_by_name_recursive(item.layout(), 'min_allowed_temperature')
                if min_allowed_temperature_w: min_allowed_temperature_w.setFont(self.model.in_use_fonts['field'])
                
                max_advised_temperature_w=self.util.get_by_name_recursive(item.layout(), 'max_advised_temperature')
                if max_advised_temperature_w: max_advised_temperature_w.setFont(self.model.in_use_fonts['field'])
                
                min_advised_temperature_w=self.util.get_by_name_recursive(item.layout(), 'min_advised_temperature')
                if min_advised_temperature_w: min_advised_temperature_w.setFont(self.model.in_use_fonts['field'])
                
                max_recommended_temperature_w=self.util.get_by_name_recursive(item.layout(), 'max_recommended_temperature')
                if max_recommended_temperature_w: max_recommended_temperature_w.setFont(self.model.in_use_fonts['field'])
                
                min_recommended_temperature_w=self.util.get_by_name_recursive(item.layout(), 'min_recommended_temperature')
                if min_recommended_temperature_w: min_recommended_temperature_w.setFont(self.model.in_use_fonts['field'])
                
                recommended_pitching_label_w=self.util.get_by_name_recursive(item.layout(), 'recommended_pitching_label')
                if recommended_pitching_label_w: recommended_pitching_label_w.setFont(self.model.in_use_fonts['field'])
                
                calculate_button_w=self.util.get_by_name_recursive(item.layout(), 'calculate_button')
                if calculate_button_w: calculate_button_w.setFont(self.model.in_use_fonts['field'])
                
                rate_w=self.util.get_by_name_recursive(item.layout(), 'rate')
                if rate_w: rate_w.setFont(self.model.in_use_fonts['field'])
                
                rate_unit_w=self.util.get_by_name_recursive(item.layout(), 'rate_unit')
                if rate_unit_w: rate_unit_w.setFont(self.model.in_use_fonts['field'])
                
                calculated_amount_w=self.util.get_by_name_recursive(item.layout(), 'calculated')
                if calculated_amount_w: calculated_amount_w.setFont(self.model.in_use_fonts['field'])
                
                calculated_amount_unit_w=self.util.get_by_name_recursive(item.layout(), 'calculated_amount_unit')
                if calculated_amount_unit_w: calculated_amount_unit_w.setFont(self.model.in_use_fonts['field'])
                
                adopted_pitch_label_w=self.util.get_by_name_recursive(item.layout(), 'adopted_pitching_label')
                if adopted_pitch_label_w: adopted_pitch_label_w.setFont(self.model.in_use_fonts['field'])
               
                    
                calculated_pitch_rate_w=self.util.get_by_name_recursive(item.layout(), 'calculated_pitching_rate')
                if calculated_pitch_rate_w: calculated_pitch_rate_w.setFont(self.model.in_use_fonts['field'])
                
                calculated_rate_unit_w=self.util.get_by_name_recursive(item.layout(), 'calculated_rate_unit')
                if calculated_rate_unit_w: calculated_rate_unit_w.setFont(self.model.in_use_fonts['field'])
                
              
                
                adopted_pitching_label_w=self.util.get_by_name_recursive(item.layout(), 'adopted_pitching_label')
                if adopted_pitching_label_w : adopted_pitching_label_w.setFont(self.model.in_use_fonts['field'])
                
                adopted_amount_w=self.util.get_by_name_recursive(item.layout(), 'adopted_amount')
                if adopted_amount_w: adopted_amount_w.setFont(self.model.in_use_fonts['field'])
                
                adopted_amount_unit_w=self.util.get_by_name_recursive(item.layout(), 'adopted_amount_unit')
                if adopted_amount_unit_w : adopted_amount_unit_w.setFont(self.model.in_use_fonts['field'])
        
            
    def show_color_dialog(self):
        self.colorDialog.show()   
    
    
    def show_feedback(self):
        self.feedback.set_session_name(self.current_session)
        self.feedback.show()    
        
        
    def show_font_size_dialog(self):
        self.fontSizeDialog.show()     
        
    def show_help(self):
        self.helpWindow.show()
        #self.helpWindow.text_edit.setHtml(Documentation.text)
            
           
    def show_malt_dialog(self):
        self.maltDialog.show()  
        
    def show_rest_dialog_create(self):
        self.restDialogCreate.show()    
        
    def show_session_designation(self):
        widgets=self.util.get_included_widgets(self.current_session_intro_layout)
        for w in widgets:
            w.setEnabled(False)
            w.show()          
        
    def show_session_feedback(self):
        widgets=self.util.get_included_widgets(self.feedback_groupbox_layout)
        for w in widgets:
            w.show() 
        self.feedback_save_button.hide()    
        self.edit_button.show()   
            
        self.feedback_water_treatment_textedit.setStyleSheet(sty.field_styles['read_only'])   
        self.feedback_water_treatment_textedit.setEnabled(False) 
        self.feedback_mash_PH_edit_2.setStyleSheet(sty.field_styles['read_only']) 
        self.feedback_mash_PH_edit_2.setEnabled(False)
        self.feedback_preboil_volume_edit_2.setStyleSheet(sty.field_styles['read_only']) 
        self.feedback_preboil_volume_edit_2.setEnabled(False)
        self.feedback_original_gravity_edit_2.setStyleSheet(sty.field_styles['read_only']) 
        self.feedback_original_gravity_edit_2.setEnabled(False)
        self.feedback_fermentor_volume_edit.setStyleSheet(sty.field_styles['read_only'])  
        self.feedback_fermentor_volume_edit.setEnabled(False)
        
                
    def show_yeast_dialog(self):
        self.yeastDialog.show()
        
    
    def show_equipment_dialog(self):
        self.equipmentDialog.show()  
        
    def showEvent(self,ev):
        print('showEvent in mainWindow')
        #self.set_translatable_textes()
        
        self.set_fonts()
        mypb=CustomProgressBar()
        mypb.setAccessibleName('ibu')
        mypb.setRange(0,200)
        mypb.setFormat('▮')
        mypb.setMaximumSize(400,18)
        self.hops_header_layout.insertWidget(5,mypb)#insert était 3

        pitching_pb=CustomProgressBar()
        pitching_pb.setAccessibleName('pitching')
        pitching_pb.setRange(0,200)
        pitching_pb.setFormat('▮')
        pitching_pb.setMaximumSize(400,18)
        self.yeast_header_layout.insertWidget(3,pitching_pb)
        date=datetime.datetime.now()
        self.set_disable_session()
        #self.hide_session_feedback()
        '''
        widgets=self.util.get_included_widgets(self.feedback_groupbox_layout)
        for w in widgets:
            w.hide()
         '''   
        self.hide_session_designation() 
        self.set_fonts()
        'if the user as asked for setting units, all units have been removed from db'
        if not self.model.get_unit('temperature'):
            self.unitSetter.setModal(True)
            'default units will be applied if dialog cancelled, or new units if apply button clicked'
            self.unitSetter.show()#will call set_unit_labels() once units set in model
        else: self.set_unit_labels() 
        '''
        if not self.model.language:
            self.language_setter.setModal(True)
            self.language_setter.show()  
        else: self.set_language(self.model.language[1])     
         '''
        
    def  show_folder_chooser(self):
        
        #if getattr( sys, 'frozen', False ) :
        # running in a bundle
        return #not used at the moment
                
    def show_import_export_dialog(self):
        'bundle_dir is preset during initialization of this main window'      
        self.importExportDbDialog.show()
          
    def show_hop_dialog(self):
        self.hopDialog.show() 
        
    
    def show_recipe_dialog(self):
        self.recipeDialog.show()     
        
      
    def update_ibu_bar(self,target):
        total_ibu=0
        for i in range(self.hop_layout.count()):
            hl=self.hop_layout.itemAt(i)
            w_ibu = self.util.get_by_name(hl,'calculated_IBU')
            try:
                if float(w_ibu.text()):
                    total_ibu = total_ibu+float(w_ibu.text())
            except:
                pass
        #get the progress bar 
        mypb = self.util.get_by_name(self.hops_header_layout,'ibu')
        mypb.setRange(0,target *2)
        if total_ibu<=target*2:
            mypb.setValue(total_ibu)
        else: 
            mypb.setValue(target *2)    
        val_ibu='{0:.1f}'.format(total_ibu)
        #val_target='{0:.1f}'.format(self.recipe.targeted_bitterness)
        val_target='{0:.1f}'.format(target)
        self.ibu_bar_label.setText(self.tr('Calculated IBUs vs. Target ⇒ ') + val_ibu+' / '+val_target)   
        
        
    def update_pitching_bar(self,target,value):
        yr_unit=self.model.get_unit('yeast_rate')
        mypb=self.util.get_by_name(self.yeast_header_layout,'pitching')
        mypb.setRange(0,target *2*100)
        if value<=target*2:
            mypb.setValue(value*100)
        else:
            mypb.setValue(value*2*100)  
                      
        val_rate=self.util.convert_to(yr_unit, value)
        val_target=self.util.convert_to(yr_unit,target)
        self.pitching_rate_bar_label.setText(self.tr('Current Pitching Rate vs. Recommended Rate ⇒ ') + val_rate+' / '+val_target)   
                  
        
    def update_rest_view(self,rests):       
        self.util.clearLayout(self.rest_layout)
        for r in  rests:
            hl=QHBoxLayout()
            purpose_edit=QLineEdit()
            purpose_edit.setAccessibleName('purpose')
            purpose_edit.setReadOnly(True)
            purpose_edit.setText(r.purpose)
            hl.addWidget(purpose_edit)#for purpose
            
            duration_edit=QLineEdit()
            duration_edit.setAccessibleName('duration')
            duration_edit.setMaximumSize(60,30)#duration
            duration_edit.setStyleSheet(sty.field_styles['read_only'])
            duration_edit.setReadOnly(True)
            duration_edit.setText(str(r.duration))
            hl.addWidget(duration_edit)
            
            duration_unit_edit=QLabel('min')
            duration_unit_edit.setAccessibleName('duration_unit')
            duration_edit.setFont(self.model.in_use_fonts['field'])
            duration_unit_edit.setMaximumWidth(40)
            hl.addWidget(duration_unit_edit)
            
            temperature_edit=QLineEdit()
            temperature_edit.setAccessibleName('temperature')
            temperature_edit.setMaximumSize(60,30)#temperature
            temperature_edit.setStyleSheet(sty.field_styles['read_only'])
            temperature_edit.setFont(self.model.in_use_fonts['field'])
            temperature_edit.setReadOnly(True)  
            unit=self.model.get_unit('temperature')
            if unit: unit_label=self.util.get_unit_label(unit)
            
            temperature_edit.setText(str(self.util.convert_to(unit, r.temperature)))
            hl.addWidget(temperature_edit)
            
            temperature_unit_edit=QLabel('°C')
            temperature_unit_edit.setAccessibleName('temperature_unit')
            temperature_unit_edit.setMaximumWidth(40)
            temperature_unit_edit.setText(unit_label)
            hl.addWidget(temperature_unit_edit)            
   
            self.rest_layout.addLayout(hl) 
            
    def zero_ibu_bar(self): 
        mypb=  self.util.get_by_name(self.hops_header_layout,'ibu') 
        if  mypb: mypb.setValue(0)
        
    def zero_pitching_bar(self):
        mypb=self.util.get_by_name(self.yeast_header_layout,'pitching')  
        if mypb: mypb.setValue(0)      
            
'''
        
if __name__ == "__main__":
 
    app = QApplication(sys.argv)
    MainWindow = MainWindow(translator)
    ui = MainWindowUI.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    '''
            
            
            
        