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
from view.HelpWindow import HelpWindow
from view.Utils import Utils
import view.constants as vcst
import view.styles as sty
from view.CustomProgressBar import CustomProgressBar
from doc.Documentation import Documentation
from view.FolderChooser import FolderChooser
from view.ImportExportDb import ImportExportDb

     
import sys
import datetime
import os

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
    
    def __init__(self, translator,parent=None):
        super(MainWindow,self).__init__(parent)
        self.setupUi(self)
        self.translator=translator
        
        'Folder structure is quite different when running in a bundle'
        'Please see pyinstaller’s documentation'
        self.frozen = 'not' 
        if getattr(sys, 'frozen', False):
            # we are running in a bundle
            #print('Frozen')
            self.frozen = 'yes'
            self.bundle_dir = sys._MEIPASS
            self.model = Model(self.bundle_dir)
            'the path to the translated .qm files'
            self.trad_path=os.path.join(self.bundle_dir ,'translate')
   
        else: 
            #print('Not frozen')
            'l’import export is reserved to the frozen application (bundled)'
            self.actionImport_Export_Databases.setVisible(False)
            self.model = Model()
            'the path to the .qm translated files'
            (filepath,filename)=os.path.split(__file__)
            self.trad_path=os.path.join(filepath,'..','translate')
        
        self.util=Utils()
        self.util.init_hop_usage_dic()
        self.controller = Controller(self.model)
        #colors must be set before all dialogs
        self.style_key_list=self.model.style_list
        self.set_active_colors() 
        self.maltDialog = MaltDialog(self.model,self.controller,self.util)
        self.hopDialog = HopDialog(self.model,self.controller,self.util)
        self.restDialogCreate = RestDialogCreate(self.model,self.controller,self.util)
        self.yeastDialog = YeastDialog(self.model,self.controller,self.util)
        self.recipeDialog = RecipeDialog(self.model,self.controller,self.util)
        self.colorDialog = ColorDialog(self.model,self.controller,self.util)
        self.equipmentDialog = EquipmentDialog(self.model,self.controller,self.util)
        
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
        
       
  
    def save_hop(self,hop,usage=None,duration=None,hop_rate=None):
        #print('dans save_hop hop_rate='+str(hop_rate))
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
        #print('dans save_hop : usage= '+usage)      
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
        if usage == 'Boil hopping' :
            hl.addWidget(QLabel('min.'))#4for unit
        else:
            hl.addWidget(QLabel(''))#4for unit   
           
        label_advised_amount=QLabel(self.tr('Advised by recipe'))
        label_advised_amount.setAlignment(Qt.Qt.AlignRight)
        hl.addWidget(label_advised_amount)
                       
        edit_advised_amount=QLineEdit()
        edit_advised_amount.setAccessibleName('advised_amount')#the amount indicated in the recipe
        edit_advised_amount.setStyleSheet(sty.field_styles['calculated'])
        edit_advised_amount.setReadOnly(True) 
        edit_advised_amount.setMaximumSize(50,30)
       
        hl.addWidget(edit_advised_amount)
        hl.addWidget(QLabel('g'))
        
        'the amount the user decides to use'
        label_amount=QLabel(self.tr('Adopted'))
        label_amount.setAlignment(Qt.Qt.AlignRight)
        hl.addWidget(label_amount)
        edit_amount=QLineEdit()
        edit_amount.setAccessibleName('amount')
        edit_amount.setStyleSheet(sty.field_styles['editable'])
        edit_amount.setMaximumSize(50,30)
    
        if hop_rate:
            hidden_hop_rate=QLineEdit()
            hidden_hop_rate.setText(str(hop_rate))
            hidden_hop_rate.setVisible(False)
            hidden_hop_rate.setAccessibleName('hidden_hop_rate')
            hl.addWidget(hidden_hop_rate)
            
        'recalculate IBU whenever the user changes the amount'           
        edit_amount.editingFinished.connect(self.calculate_IBU)
        hl.addWidget(edit_amount)
        
        hl.addWidget(QLabel('g'))#6 for weight unit
        
        label_calculated_IBU=QLabel()
        label_calculated_IBU.setAccessibleName('calculated_IBU')
        hl.addWidget(label_calculated_IBU)    
      
        hl.addWidget(QLabel('IBU'))  #8 
        
        label_hidden_alpha=QLabel()
        label_hidden_alpha.setAccessibleName('hidden_alpha')
        label_hidden_alpha.setText(str(hopT.alpha_acid))
        hl.addWidget(label_hidden_alpha)
        label_hidden_alpha.hide()

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
        
        label_percentage_unit=QLabel('%')
        label_percentage_unit.setMaximumSize(30,30)
        label_percentage_unit.setStyleSheet("font-size: 14px;")
        hl.addWidget(label_percentage_unit)
        
        edit_calculated_mass=QLineEdit()
        edit_calculated_mass.setAccessibleName('calculated_mass')
        edit_calculated_mass.setMaximumSize(60,30)
        edit_calculated_mass.setStyleSheet(sty.field_styles['calculated'])
        edit_calculated_mass.setReadOnly(True)  
        hl.addWidget(edit_calculated_mass)
        
        label_mass_unit=QLabel('kg')
        label_mass_unit.setStyleSheet("font-size: 14px;")
        label_mass_unit.setMaximumSize(40,30)
        hl.addWidget(label_mass_unit)
              
        self.malt_layout.addLayout(hl)
     
          
        
    def batch_volume_changed(self): 
        self.clean_results()
        self.set_aroma_amounts()   
        
    def calculate_hop_amounts(self): 
        'calculate hop amounts based on hop rate (g/l) and final boiling volume'  
        'this function is called whenever the user click the "Reset to Recipe values" in the hop area of the MainWindow' 
        'It sets values both in the advised and the adopted fields'
        
        batch_size=self.util.check_input(self.batch_volume_edit,False,self.tr('Batch Volume'),False, 0,100)
        if not batch_size:
            return
        if not self.equipment:
            warning_text='Warning : Hop Amount Calculation'
            self.util.alerte(self.tr('Please select an equipment'),QMessageBox.Warning, warning_text)
            return
        end_boiling_volume=batch_size+self.equipment.boiler_dead_space
        #print('end boiling volume = '+str(end_boiling_volume))
        for i in range(self.hop_layout.count()):
            hl=self.hop_layout.itemAt(i).layout()
            w_amount= self.util.get_by_name(hl,'amount')
            w_hidden_rate=self.util.get_by_name(hl, 'hidden_hop_rate') 
            rate=self.util.check_input(w_hidden_rate, False, self.tr(' Hop rate '+str(i)), False, 0, 50, True)
            if not rate:
                return
            #print ('hop'+str(i))
            #print ('rate= '+str(rate))
            w_advised=self.util.get_by_name(hl,'advised_amount')
            advised_value=rate*end_boiling_volume
            display_value='{0:.2f}'.format(advised_value)
            w_advised.setText(display_value)
            w_amount.setText(display_value)
            self.calculate_IBU(w_amount)
        
    def calculate_malt_amounts(self):
        'calculate malt amounts based on percentages and gravity target'
        'This function is called after a recipe, an equipment, a batch size and a grain temperature have been defined'
        'whenever the user click the calculate button in the malt area of the main window'
        
        self.set_input_style()
        warning_text=self.tr('Warning : Malt Amount Calculation')
        
        if not self.recipe:
            self.util.alerte(self.tr('Please select a recipe'),QMessageBox.Warning, warning_text)
            return
        if not self.equipment:
            self.util.alerte(self.tr('Please select an equipment'),QMessageBox.Warning, warning_text)
        self.batch_volume = self.util.check_input(self.batch_volume_edit, False, self.tr('Batch volume'), False, 1, 100) 
        if not self.batch_volume: return 
        self.grain_temperature = self.util.check_input(self.grain_temperature_edit, False, 'Grain temperature', False, 0,35) 
        if not self.grain_temperature: return
        
        first_rest=self.rest_layout.itemAt(0)
        if first_rest:
            self.first_rest_temperature = float(first_rest.itemAt(3).widget().text())                                                    
        else:
            self.util.alerte('There should be at least one rest. Please select a recipe or check the recipe you have selected',
                             QMessageBox.Warning,warning_text)    
 
        calculator=Calculator(self.model,self.recipe,self.equipment,self.batch_volume,self.boiling_time)
        total_mass=calculator.get_malt_mass()
        
        for i in range(len(self.malts)):
            w_percentage=self.util.get_by_name(self.malt_layout.itemAt(i).layout(),'percentage')
            amount=total_mass*float(w_percentage.text())/100
            w_calculated_mass=self.util.get_by_name(self.malt_layout.itemAt(i).layout(),'calculated_mass')
            w_calculated_mass.setText(str(float(math.ceil(amount*100)/100)))

        if self.equipment.type == 1: self.mash_water_volume = calculator.get_mash_water_volume(1)
        if self.equipment.type == 0: self.mash_water_volume  = calculator.get_mash_water_volume(0)
        val='{0:.2f}'.format(self.mash_water_volume)
        self.mash_water_volume_edit.setText(val)
        strike_temperature = calculator.get_strike_temperature(self.mash_water_volume, total_mass, \
                            self.first_rest_temperature, self.grain_temperature)
        val='{0:.1f}'.format(strike_temperature)
        self.strike_temperature_edit.setText(val)
        self.sparge_water_volume = calculator.get_sparge_water_volume(self.mash_water_volume)
        val ='{0:.2f}'.format(self.sparge_water_volume)
        self.mash_sparge_water_volume_edit.setText(str(val))
 
    def calculate_IBU(self,s=None):
        #print('Entering calculate_IBU')
        '''
        this function is called afer hop amounts have been calculated or on editing finished for one specific hop adopted amount 
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
            #print('leaving IBU soon because not boiling or FWH')
            #print(usage)
            'no calculation in other usage cases'
            return 
        
        batch_volume = self.util.check_input(self.batch_volume_edit, False, self.tr('Batch volume'), False, 1, 100) 
        if not batch_volume:
            widg.setText('') 
            return 
        boiling_time=self.recipe.boiling_time
        if not boiling_time: 
            widg.setText('')
            return  
        #flag calculated determines the default style for the widget
        mass=self.util.check_input(widg, False, self.tr('Hop amount'), False, 0, 1000)
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
        
    def calculate_yeast_amount(self):
        batch_volume = self.util.check_input(self.batch_volume_edit, False, self.tr('Batch volume'), False, 1, 100) 
        if not batch_volume:#alert is given in check_input
            return
        original_gravity=self.util.check_input(self.targeted_original_gravity_value,False,self.tr('Targeted Original Gravity'),False,1.000,1.110 )
        if not original_gravity:#alert is given in check_input
            return
        pitching_rate = self.recipe.yeast_in_recipe.pitching_rate
        billions=pitching_rate * batch_volume * 1000 * (original_gravity -1)/4
        amount=billions/100*11
        val='{0:.0f}'.format(amount)
        w_amount=self.util.get_by_name_recursive(self.yeast_layout,'calculated_amount')
        w_amount.setText(val)
        w_adopted_amount=self.util.get_by_name_recursive(self.yeast_layout,'adopted_amount')
        w_adopted_amount.setText(val)
        adopted_yeast_amount_edit=self.util.get_by_name_recursive(self.yeast_layout, 'adopted_amount')
        if adopted_yeast_amount_edit: 
            adopted_yeast_amount_edit.setReadOnly(False)
            adopted_yeast_amount_edit.setStyleSheet(sty.field_styles['editable'])
            adopted_yeast_amount_edit.editingFinished.connect(self.calculate_adopted_pitching_rate)
        self.calculate_adopted_pitching_rate()
        
        
    def calculate_adopted_pitching_rate(self):
        batch_volume = self.util.check_input(self.batch_volume_edit, False, self.tr('Batch volume'), False, 1, 100) 
        if not batch_volume:#alert is given in check_input
            return
        original_gravity=self.util.check_input(self.targeted_original_gravity_value,False,self.tr('Targeted Original Gravity'),False,1.000,1.110 )
        if not original_gravity:#alert is given in check_input
            return
        widgt=self.util.get_by_name_recursive(self.yeast_layout,'adopted_amount')
        a = self.util.check_input(widgt,False,self.tr('Adopted yeast Amount'),False, 0,100)
        if not a: return
        advised_rate= self.recipe.yeast_in_recipe.pitching_rate
        billions=a *100/11
        platos=(original_gravity -1)*1000/4
        pitching_rate=  billions / batch_volume / platos
        val='{0:.2f}'.format(pitching_rate)
        calculated_p_rate_edit=self.util.get_by_name_recursive(self.yeast_layout,'calculated_pitching_rate')
        calculated_p_rate_edit.setText(val)
        self.update_pitching_bar(advised_rate,pitching_rate)   
        
    def changeEvent(self, event):
        #print('change event')
        #print(str(event.type))
        if event.type() == QtCore.QEvent.LanguageChange:
            #print('Event is lang change')
            
            self.retranslateUi(self)
        
    def clear_layouts(self):
        print('clearing mal layout')
        self.util.clearLayout(self.malt_layout)
        print('clearing hop layout')
        self.util.clearLayout(self.hop_layout)
        print('clearing yeast layout')
        self.util.clearLayout(self.yeast_layout)
        print('clearing rest layout')
        self.util.clearLayout(self.rest_layout)
        
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
     
    def create_icons(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap((":/icons/assets/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)    
        
    def edit_session(self):
        if self.session_combo.currentText():
            self.set_feedback_editable()
                                 
                                                     
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
                input'), False, 0, 100)
                l.append(val)
        return l   
    
    def hide_session_designation(self):
        widgets=self.util.get_included_widgets(self.current_session_intro_layout)
        for w in widgets:
            w.hide()   
            
    def hide_session_feedback(self):
        widgets=self.util.get_included_widgets(self.feedback_groupbox_layout)
        for w in widgets:
            ##print(w)
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
            self.session_combo.addItem(session.designation)
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
                self.save_hop(hop,use,hir.duration,hir.hop_rate)
            self.targeted_bitterness_value.setText(str(self.recipe.targeted_bitterness))  
            #self.calculate_hop_amounts()
            
            #YEAST
            self.util.clearLayout(self.yeast_layout)
            yeast=self.model.get_yeast(self.recipe.yeast_in_recipe.yeast)
            self.set_yeast_view(yeast,self.recipe.yeast_in_recipe.pitching_rate)
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
            #to prevent GUI refresh on recipe or equipment change in DB
            self.mode_session='view'
            session=self.model.get_session(str(self.session_combo.currentText())) 
            self.set_ro_session()
            self.designation_edit.setText(session.designation)
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
            
        
            self.batch_volume_edit.setText(str(session.batch_volume))
            self.grain_temperature_edit.setText(str(session.grain_temperature))
            

            malts=session.malts_in_session
            self.util.clearLayout(self.malt_layout)
            for i in range(len(malts)):
                ##print(malts[i].name)
                m=self.model.get_malt(malts[i].name)
                self.add_malt_view(m,malts[i].percentage)
                item=self.malt_layout.itemAt(i)
                if item:
                    amount_w=self.util.get_by_name(item.layout(), 'calculated_mass')
                    if amount_w: 
                        amount_w.setText(str(malts[i].amount))
                        amount_w.setReadOnly(True)
                        amount_w.setStyleSheet(sty.field_styles['read_only']) 
                        
            self.mash_water_volume_edit.setText(str(session.mash_water_volume))      
            self.strike_temperature_edit.setText(str(session.strike_temperature))    
            self.mash_sparge_water_volume_edit.setText(str(session.mash_sparge_water_volume))  
                        
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
                self.save_hop(h,his.usage,his.duration) 
                ibu=self.calculate_IBU_later(his.duration,session.batch_volume,
                                             session.targeted_original_gravity,his.amount,h.alpha_acid,session.batch_volume)
                ibus.append(ibu)
                  
                item=self.hop_layout.itemAt(i)
                if item:
                    amount_w=self.util.get_by_name(item.layout(), 'amount')   
                    if amount_w:
                        amount_w.setText(str(his.amount))
                        amount_w.setReadOnly(True)
                        amount_w.setStyleSheet(sty.field_styles['read_only'])
                        try:
                            amount_w.editingFinished.disconnect()
                        except:
                            pass  
                  
            yis=session.yeast_in_session
            self.util.clearLayout(self.yeast_layout)
            yeast=self.model.get_yeast(yis.name)
            if yeast: 
                self.set_yeast_view(yeast,None,False)
            adopted_amount=self.util.get_by_name_recursive(self.yeast_layout, 'adopted_amount')    
            if adopted_amount: 
                adopted_amount.setText(str(session.yeast_in_session.amount))
                try:
                    adopted_amount.editingFinished.disconnect()
                except:
                    pass   
            adopted_pitching_rate=self.util.get_by_name_recursive(self.yeast_layout, 'calculated_pitching_rate')
            plato=(session.targeted_original_gravity-1)*1000/4
            try:
               pitching_rate=session.yeast_in_session.amount/session.batch_volume/plato*100/11
               val='{0:.2f}'.format(pitching_rate)
               adopted_pitching_rate.setText(val)
               self.update_pitching_bar(session.yeast_in_session.recommended_pitching_rate,pitching_rate)
            except:
                self.util.alerte('There is something wrong in the arguments of pitching rate calculation') 
                
            
             
            
          
            for i in range(len(hops)):
                item=self.hop_layout.itemAt(i)
                if item:
                    calculated_ibu_w=self.util.get_by_name(item.layout(), 'calculated_IBU')
                    val='{0:.0f}'.format(ibus[i])
                    if calculated_ibu_w: calculated_ibu_w.setText(val)
                 
            self.update_ibu_bar(session.targeted_bitterness)
                 
            if hasattr(session,'feedback_water_treatment_text'):
                self.feedback_water_treatment_textedit.setText(session.feedback_water_treatment_text)
               
            if hasattr(session,'feedback_mash_ph'):
                if session.feedback_mash_ph:
                    self.feedback_mash_PH_edit_2.setText(str(session.feedback_mash_ph)) 
                else: self.feedback_mash_PH_edit_2.setText('')      
            if hasattr(session,'feedback_preboil_volume'):
                if session.feedback_preboil_volume:
                    self.feedback_preboil_volume_edit_2.setText(str(session.feedback_preboil_volume))  
                else:  self.feedback_preboil_volume_edit_2.setText('')                
            if hasattr(session,'feedback_original_gravity'):
                if session.feedback_original_gravity:
                    self.feedback_original_gravity_edit_2.setText(str(session.feedback_original_gravity))  
                else: self.feedback_original_gravity_edit_2.setText('')      
            if hasattr(session,'feedback_fermentor_volume'):
                if session.feedback_fermentor_volume:
                    self.feedback_fermentor_volume_edit.setText(str(session.feedback_fermentor_volume))
                else: self.feedback_fermentor_volume_edit.setText('')         
            self.show_session_feedback()   
    
    def new_session(self):
        'the hop_calculate_button can be hidden when displaying a past session'
        self.hop_calculate_button.show()
        self.init_session_combo()#to make the previous selection disappear
        self.hide_session_feedback()
        widgets=self.util.get_included_widgets(self.feedback_groupbox_layout)
        for w in widgets:
            w.hide()        
        self.hide_session_designation() 
        self.set_editable_session()
        #print('in new_session passing mode_session to create')
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
                    
                    
    def remove_session(self):
        session=self.session_combo.currentText()
        if session: self.model.remove_session(session)
        self.init_session_combo()
        self.set_disable_session()
        self.clear_layouts()
        self.clear_inputs()
        self.hide_session_feedback()
        

    def save_session_feedback(self):
        designation=self.designation_edit.text()
        session=self.model.get_session(designation)
        if not session: 
            return
        feedback_water_treatment_text=self.feedback_water_treatment_textedit.toPlainText()
        session.feedback_water_treatment_text=feedback_water_treatment_text
        feedback_mash_ph=self.util.check_input(self.feedback_mash_PH_edit_2, False, self.tr('Feedback Mash PH'), True, 3, 7)
        session.feedback_mash_ph=feedback_mash_ph
        feedback_preboil_volume=self.util.check_input(self.feedback_preboil_volume_edit_2, False, self.tr('Feedback Preboil Volume'), True, 0, 100)
        session.feedback_preboil_volume=feedback_preboil_volume
        feedback_original_gravity=self.util.check_input(self.feedback_original_gravity_edit_2, False, self.tr('Feedback Original Gravity'), True, 1, 2)
        session.feedback_original_gravity=feedback_original_gravity
        feedback_fermentor_volume=self.util.check_input(self.feedback_fermentor_volume_edit, False, self.tr('Feedback Fermentor Volume'), True, 0, 100)
        session.feedback_fermentor_volume=feedback_fermentor_volume
        self.model.save_session(session)
        self.show_session_feedback() #to get back to non editable state

        
    def save_session(self):
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
        
        batch_volume=self.util.check_input(self.batch_volume_edit, False, self.tr('Batch Volume'),False, 0, 100) 
        if not batch_volume: return#alert message is included in check_input
        
        grain_temperature=self.util.check_input(self.grain_temperature_edit, False,self.tr('Grain Temperature'), False, 0, 60)
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
                    amount=self.util.check_input(amount_w, False, self.tr('Malt Amount '+str(i)), False, 0, 50, True)
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
                if temperature_w: temperature=float(temperature_w.text())
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
                    duration=self.util.check_input(duration_w,False, self.tr('Hop duration '+str(i)), False, 0, 200)
                    if not duration: return
                    
                amount_w=self.util.get_by_name(item.layout(), 'amount')
                if amount_w:
                    amount=self.util.check_input(amount_w, False, self.tr('Hop Amount '+str(i)),False, 0, 200)
                    if not amount: return
                his=HopInSession(name,usage,duration,amount)
                hops_in_session.append(his)
                      
        'SAVE YEAST VALUES'   
        yeast_name_w=self.util.get_by_name_recursive(self.yeast_layout, 'name')
        if yeast_name_w: yeast_name=yeast_name_w.text()
        rate_edit=self.util.get_by_name_recursive(self.yeast_layout, 'rate')
        if rate_edit: rate=float(rate_edit.text())
        
        adopted_yeast_amount_edit=self.util.get_by_name_recursive(self.yeast_layout,'adopted_amount')
        if not adopted_yeast_amount_edit: 
            self.util.alerte(self.tr('Could not find the adopted yeast amount. This should never happen. Please file a bug'))
            return
        else:
            adopted_yeast_amount=self.util.check_input(adopted_yeast_amount_edit, False, self.tr('Adopted Yeast Amount. \
             Please use the calculate button and if you want change the value '), False,0,100)
            if not isinstance(adopted_yeast_amount,float):
                return
            #print('Saving yeast '+yeast_name +'  -- '+str(adopted_yeast_amount)+'  --  '+str(rate))
            yeast_in_session=YeastInSession(yeast_name,adopted_yeast_amount,rate)
        
            
        mash_water_volume=self.util.check_input(self.mash_water_volume_edit,False, self.tr('Mash Water Volume'),False,0,100)    
        if not mash_water_volume: return
        strike_temperature=self.util.check_input(self.strike_temperature_edit, False, self.tr('Strike Température'), False,0,100)
        if not strike_temperature: return
        mash_sparge_water_volume=self.util.check_input(self.mash_sparge_water_volume_edit, False, self.tr('Sparge Water Volume'), False, 0,100)
        equipment_object=self.model.get_equipment(equipment)   
        if equipment: boiler_dead_space=equipment_object.boiler_dead_space
        
        session=Session(designation,recipe,equipment,batch_volume,grain_temperature,
                        targeted_original_gravity,targeted_bitterness,boiling_time,brewing_efficiency,
                        malts_in_session,rests_in_session,hops_in_session,yeast_in_session,
                        mash_water_volume,strike_temperature,mash_sparge_water_volume,boiler_dead_space)
        
        self.model.save_session(session)
        self.init_session_combo()
        index = self.session_combo.findText(designation, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.session_combo.setCurrentIndex(index)
            
        #print('Session has been saved')    
        
        
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
        
     
    def set_disable_session(self):
            self.hide_session_designation()
            self.batch_volume_edit.setStyleSheet(sty.field_styles['read_only'])
            self.batch_volume_edit.setEnabled(False)
            self.grain_temperature_edit.setEnabled(False)
            self.grain_temperature_edit.setStyleSheet(sty.field_styles['read_only'])
            self.recipe_combo.setEnabled(False)
            self.equipment_combo.setEnabled(False)
            self.calculate_button.setEnabled(False)
            
            
            
    def select_combo_by_text(self,combo,text):    
        index = combo.findText(text, QtCore.Qt.MatchFixedString)
        if index >= 0:
            combo.setCurrentIndex(index)
            
    def set_connections(self):
        self.actionEdit_Malt_Database.triggered.connect(self.show_malt_dialog)
        self.actionEdit_Hop_Database.triggered.connect(self.show_hop_dialog)
        self.actionEdit_Rest_Database.triggered.connect(self.show_rest_dialog_create)
        self.actionEdit_Yeast_Database.triggered.connect(self.show_yeast_dialog)
        self.actionCustomize_colors.triggered.connect(self.show_color_dialog)
        self.actionImport_Export_Databases.triggered.connect(self.show_import_export_dialog)
        self.actionEdit_Recipe_Database.triggered.connect(self.show_recipe_dialog)
        self.actionEdit_Equipment_Database.triggered.connect(self.show_equipment_dialog)
        self.actionView_Help.triggered.connect(self.show_help)
        self.actionFrench.triggered.connect(self.set_language_fr)
        self.actionEnglish.triggered.connect(self.set_language_en)
        self.actionJapanese.triggered.connect(self.set_language_jp)

        
        self.calculate_button.clicked.connect(self.calculate_malt_amounts)
        self.hop_calculate_button.clicked.connect(self.calculate_hop_amounts)
        self.batch_volume_edit.editingFinished.connect(self.batch_volume_changed)    
        self.bar_button.clicked.connect(self.explain_ibu_bar)
        self.main_help_button.clicked.connect(self.explain_current_brewing_session)
        self.pitching_bar_button.clicked.connect(self.explain_yeast_bar)
        self.add_button.clicked.connect(self.save_session)
        self.new_button.clicked.connect(self.new_session)
        self.delete_button.clicked.connect(self.remove_session)   
        self.edit_button.clicked.connect(self.edit_session)  
        self.feedback_save_button.clicked.connect(self.save_session_feedback)   
        self.batch_volume_edit.editingFinished.connect(self.calculate_hop_amounts) 
        
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
        
    def set_subscriptions(self):
        self.model.subscribe_model_changed(['malt','hop','yeast','recipe','equipment','session','style'],self.on_model_changed_main)
        
    def show_color_dialog(self):
        self.colorDialog.show()    
        
    def show_help(self):
        self.helpWindow.show()
        self.helpWindow.textEdit.setHtml(Documentation.text)
            
           
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
        
    def set_active_colors(self):
        #print('setting active colors')
        self.active_colors={}
        for key in vcst.FIELD_DEFAULT_COLORS:
            if key in self.style_key_list:
                self.active_colors[key]=self.model.get_styles(key)
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
                
                
              
                        
    def set_aroma_amounts(self):
        for  i in range(self.hop_layout.count()):
            item =self.hop_layout.itemAt(i)
            if item:
                hidden_hop_rate=self.util.get_by_name_recursive(item.layout(),'hidden_hop_rate')
                if not hidden_hop_rate : continue
                else: hop_rate=self.util.check_input(hidden_hop_rate,False,self.tr('Hop rate'),False,0,4)
                if not hop_rate: continue
                
                hop_amount_edit=self.util.get_by_name_recursive(item.layout(),'amount')
                if not hop_amount_edit: continue
                else:
                    batch_size=self.util.check_input(self.batch_volume_edit,False,self.tr('Batch Volume'),False, 0,100)
                    if  batch_size:
                        hop_amount=batch_size * hop_rate
                        val='{0:.1f}'.format(hop_amount)
                        hop_amount_edit.setText(str(val))
                        hop_amount_edit.setStyleSheet(sty.field_styles['calculated'])
                        self.calculate_IBU(hop_amount_edit)
                          
            
    def set_calculated_style(self):
        
        self.mash_water_volume_edit.setStyleSheet(sty.field_styles['calculated'])
        self.mash_water_volume_edit.setReadOnly(True)
        self.strike_temperature_edit.setStyleSheet(sty.field_styles['calculated'])
        self.strike_temperature_edit.setReadOnly(True)
        self.mash_sparge_water_volume_edit.setStyleSheet(sty.field_styles['calculated'])
        self.mash_sparge_water_volume_edit.setReadOnly(True)
        
           
    def set_input_style(self):
        self.batch_volume_edit.setStyleSheet(sty.field_styles['editable'])
        self.grain_temperature_edit.setStyleSheet(sty.field_styles['editable'])  
        
    def set_language_jp(self):
        #print('Japanese language selected')  
        app=QApplication.instance()
        app.removeTranslator(self.translator)
        self.translator.load(os.path.join(self.trad_path,'ja_JP'))
        app.installTranslator(self.translator)
   
         
    def set_language_en(self):
        #print('English language selected') 
        app=QApplication.instance()
        app.removeTranslator(self.translator)
        self.translator.load(os.path.join(self.trad_path,'en_EN'))
        app.installTranslator(self.translator)   
        
        
    def set_language_fr(self):
        #print('French language selected') 
        app=QApplication.instance()
        app.removeTranslator(self.translator)
        self.translator.load(os.path.join(self.trad_path,'fr_FR'))
        '''reinstall of translator triggers an changeEvent that should be used in each widget that 
        needs translation. See changeEvent function in each widget'''
        app.installTranslator(self.translator)
        
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
             
        
    def set_tooltips (self):
        return
        if self.equipment:
            text='Brewing efficiency: '+str(self.equipment.brewing_efficiency) +\
             '\nBoiler size: '+str(self.equipment.boiler_size)+\
             '\nBoiler dead space: '+str(self.equipment.boiler_dead_space)+\
             '\nFermentor size: '+str(self.equipment.fermentor_size)+\
             '\nFermentor dead space: '+str(self.equipment.fermentor_dead_space)
            self.equipment_combo.setToolTip(text)
            
            
    def set_translatable_textes(self):
        self.menuFile.setTitle(self.tr("File"))
        self.menuDatabase.setTitle(self.tr("Database"))
        self.menuHelp.setTitle(self.tr( "Help"))
        self.menuSettings.setTitle(self.tr("Settings"))
        self.actionEdit_Malt_Database.setText(self.tr('Edit Malt Database'))
        self.actionEdit_Hop_Database.setText(self.tr('Edit Hop Database'))
        self.actionEdit_Yeast_Database.setText(self.tr('Edit Yeast Database'))
        self.actionEdit_Recipe_Database.setText(self.tr('Edit Recipe Database'))
        self.actionEdit_Equipment_Database.setText(self.tr('Edit Equipment Database'))
        self.actionEdit_Rest_Database.setText(self.tr('Edit Rest Database'))
        self.actionCustomize_colors.setText(self.tr('Customize Colors'))
        self.actionView_Help.setText(self.tr('View Help'))
        self.menuChoose_Language.setTitle(self.tr('Choose Language'))
        self.actionFrench.setText(self.tr('French'))
        self.actionEnglish.setText(self.tr('English'))
        self.actionJapanese.setText(self.tr('Japanese'))
        self.edit_button.setText(self.tr('Edit'))
        self.delete_button.setText(self.tr('Delete'))
        self.new_button.setText(self.tr('New'))
        self.designation_label.setText(self.tr('Designation'))
        
        self.current_brewing_session_label.setText(self.tr('Current Brewing Session')) 
        self.choose_session_label.setText(self.tr('Display or delete an existing session'))
        self.new_session_label.setText(self.tr('Create a new brewing session'))
        
        self.batch_volume_label.setText(self.tr('Batch Volume'))  
        self.batch_volume_unit_label.setText(self.tr('liters'))
        self.grain_temperature_label.setText(self.tr('Grain Temperature'))
        self.grain_temperature_unit_label.setText(self.tr('°C'))  
        self.add_button.setText(self.tr('Save Current Session'))
        
        self.recipe_label.setText(self.tr('Recipe'))
        self.equipment_label.setText(self.tr('Equipment'))
        
        self.boiling_time_label.setText(self.tr('Boiling Time'))
        self.boiling_time_unit_label.setText(self.tr('min.'))
        self.recipe_label.setText(self.tr('Recipe'))
        self.targeted_original_gravity_label.setText(self.tr('Targeted Original Gravity'))
        self.targeted_bitterness_label.setText(self.tr('Targeted Bitterness'))
        self.targeted_bitterness_unit_label.setText(self.tr('IBU'))
        self.brewing_efficiency_label.setText(self.tr('Brewing Efficiency'))
        
        self.mash_label.setText(self.tr('Mashing'))
        self.malt_label.setText(self.tr('Malts'))
        self.calculate_button.setText(self.tr('Calculate Button'))
        
        self.mash_rest_label.setText(self.tr('Mash Rests'))
        self.mash_water_volume_label.setText(self.tr('Mash Water Volume'))
        self.mash_water_volume_unit_label.setText(self.tr('liters'))
        
        self.strike_temperature_label.setText(self.tr('Strike Temperature'))
        self.strike_temperature_unit_label.setText(self.tr('°C'))
        
        self.mash_sparge_water_volume_label.setText(self.tr('Sparge Water Volume'))
        self.mash_sparge_water_volume_unit_label.setText(self.tr('liters'))
        
        self.boil_label.setText(self.tr('Boiling'))
        self.hop_label.setText(self.tr('Hops'))
        self.ibu_bar_label.setText(self.tr('Current Bitterness vs. Target'))
        self.hop_calculate_button.setText(self.tr('Reset to recipe values'))
        
        self.adjunct_label.setText(self.tr('Adjuncts'))
        
        self.pitching_label.setText(self.tr('Pitching'))
        self.yeast_label.setText(self.tr('Yeast'))
        self.pitching_rate_bar_label.setText(self.tr('Current Pitching Rate vs. Recommendation'))
        
        self.feedback_label.setText(self.tr('Feedback'))
        self.feedback_water_treatment_label.setText(self.tr('Water Treatment'))
        self.feedback_observed_data_label.setText(self.tr('Observed Data'))
        self.feedback_mash_PH_label_2.setText(self.tr('Mash PH'))
        self.feedback_preboil_volume_label_2.setText(self.tr('Preboil Volume'))
        self.feedback_preboil_volume_unit_label_2.setText(self.tr('liters'))
        self.feedback_original_gravity_label_2.setText(self.tr('Original Gravity'))
        self.feedback_fermentor_volume_label_2.setText(self.tr('Fermentor Volume'))
        self.feedback_fermentor_volume_unit_label_2.setText(self.tr('liters')) 
        self.feedback_save_button.setText(self.tr('Save Feedback'))    
        
        
    def set_yeast_view(self,yeast_type,rate=None,creation_mode=True):  
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
        temp_label=QLabel(self.tr('Temperature range'),alignment=4)
        vl1.addWidget(temp_label)
        hl1=QHBoxLayout()
        min_allowed_temperature_edit=QLineEdit()
        min_allowed_temperature_edit.setAccessibleName('min_allowed_temperature')
        min_allowed_temperature_edit.setMinimumSize(50,30)
        min_allowed_temperature_edit.setMaximumSize(50,30)
        min_allowed_temperature_edit.setStyleSheet(sty.field_styles['min_max_allowed'])
        min_allowed_temperature_edit.setReadOnly(True)
        min_allowed_temperature_edit.setText(str(yeastT.min_allowed_temperature))
        hl1.addWidget(min_allowed_temperature_edit)
        
        min_advised_temperature_edit=QLineEdit()
        min_advised_temperature_edit.setAccessibleName('min_advised_temperature')
        min_advised_temperature_edit.setMinimumSize(50,30)
        min_advised_temperature_edit.setMaximumSize(50,30)
        min_advised_temperature_edit.setStyleSheet(sty.field_styles['min_max_advised'])
        min_advised_temperature_edit.setReadOnly(True)
        min_advised_temperature_edit.setText(str(yeastT.min_advised_temperature))
        hl1.addWidget(min_advised_temperature_edit)
        
        max_advised_temperature_edit=QLineEdit()
        max_advised_temperature_edit.setAccessibleName('max_advised_temperature')
        max_advised_temperature_edit.setMinimumSize(50,30)
        max_advised_temperature_edit.setMaximumSize(50,30)
        max_advised_temperature_edit.setStyleSheet(sty.field_styles['min_max_advised'])
        max_advised_temperature_edit.setReadOnly(True)
        max_advised_temperature_edit.setText(str(yeastT.max_advised_temperature))
        hl1.addWidget(max_advised_temperature_edit)
        
        max_allowed_temperature_edit=QLineEdit()
        max_allowed_temperature_edit.setAccessibleName('max_allowed_temperature')
        max_allowed_temperature_edit.setMinimumSize(50,30)
        max_allowed_temperature_edit.setMaximumSize(50,30)
        max_allowed_temperature_edit.setStyleSheet(sty.field_styles['min_max_allowed'])
        max_allowed_temperature_edit.setReadOnly(True)
        max_allowed_temperature_edit.setText(str(yeastT.max_allowed_temperature))
        hl1.addWidget(max_allowed_temperature_edit)
        vl1.addLayout(hl1)
        vl1.addStretch()
        hl.addLayout(vl1)
        hl.addStretch()
        
        vl2=QVBoxLayout()
        if creation_mode:
            hl21=QHBoxLayout()
            hl22=QHBoxLayout()
            hl23=QHBoxLayout()
            pitch_label=QLabel(self.tr('Recommended Pitching rate'),alignment=4)
            hl21.addWidget(pitch_label)
            calculate_amount_button=QPushButton(self.tr('Calculate'))
            calculate_amount_button.setAccessibleName('calculate_button')
            calculate_amount_button.setMaximumSize(120, 30)
            calculate_amount_button.clicked.connect(self.calculate_yeast_amount)
            hl21.addWidget(calculate_amount_button)
            vl2.addLayout(hl21)
        
            rate_edit=QLineEdit()
            rate_edit.setAccessibleName('rate')
            rate_edit.setMaximumSize(60,30)
            rate_edit.setStyleSheet(sty.field_styles['read_only'])
            hl22.addWidget(rate_edit)
            if rate:
                rate_edit.setText(str(rate))
        
            rate_unit=QLabel('billions/°P/liter')   
            rate_unit.setAccessibleName('rate_unit')
            rate_unit.setMaximumSize(100,30)
            rate_unit.setStyleSheet("font-size: 14px;")
            hl22.addWidget(rate_unit) 
            calculated_amount_edit=QLineEdit()
            calculated_amount_edit.setAccessibleName('calculated_amount')
            calculated_amount_edit.setStyleSheet(sty.field_styles['calculated'])
            calculated_amount_edit.setReadOnly(True)
            calculated_amount_edit.setMaximumSize(60,30)
            hl22.addWidget(calculated_amount_edit)
            calculated_amount_unit=QLabel('g')
            calculated_amount_unit.setMaximumSize(30,30)
            hl22.addWidget(calculated_amount_unit) 

            vl2.addLayout(hl22)
            #4 lines to add an horizontal separator
            hline=QFrame()
            hline.setFrameShape(QFrame.HLine)
            hline.setFrameShadow(QFrame.Sunken)
            vl2.addWidget(hline)
            adopted_pitch_label=QLabel(self.tr('Adopted Pitching rate'),alignment=4)
            vl2.addWidget(adopted_pitch_label)
            calculated_rate_edit=QLineEdit()
            calculated_rate_edit.setAccessibleName('calculated_pitching_rate')
            calculated_rate_edit.setMaximumSize(60,30)
            calculated_rate_edit.setStyleSheet(sty.field_styles['calculated'])
            calculated_rate_edit.setReadOnly(True)
            hl23.addWidget(calculated_rate_edit)
            calculated_rate_unit=QLabel('billions/°P/liter')
            calculated_rate_unit.setAccessibleName('calculated_rate_unit')
            calculated_rate_unit.setStyleSheet("font-size: 14px")
            hl23.addWidget(calculated_rate_unit)
            adopted_amount_edit=QLineEdit()
            adopted_amount_edit.setAccessibleName('adopted_amount')
            adopted_amount_edit.setStyleSheet(sty.field_styles['read_only'])
            adopted_amount_edit.setReadOnly(True)
            adopted_amount_edit.editingFinished.connect(self.calculate_adopted_pitching_rate)
            adopted_amount_edit.setMaximumSize(60,30)
            hl23.addWidget(adopted_amount_edit)
            adopted_amount_unit=QLabel('g')
            adopted_amount_unit.setMaximumSize(30,30)
      
            hl23.addWidget(adopted_amount_unit) 
        
            vl2.addLayout(hl23)
        else:
            hl23=QHBoxLayout()
            adopted_pitch_label=QLabel(self.tr('Adopted Pitching rate'),alignment=4)
            vl2.addWidget(adopted_pitch_label)
            calculated_rate_edit=QLineEdit()
            calculated_rate_edit.setAccessibleName('calculated_pitching_rate')
            calculated_rate_edit.setMaximumSize(60,30)
            calculated_rate_edit.setStyleSheet(sty.field_styles['read_only'])
            calculated_rate_edit.setReadOnly(True)
            hl23.addWidget(calculated_rate_edit)
            calculated_rate_unit=QLabel('billions/°P/liter')
            calculated_rate_unit.setAccessibleName('calculated_rate_unit')
            calculated_rate_unit.setStyleSheet("font-size: 14px")
            hl23.addWidget(calculated_rate_unit)
            adopted_amount_edit=QLineEdit()
            adopted_amount_edit.setAccessibleName('adopted_amount')
            adopted_amount_edit.setStyleSheet(sty.field_styles['read_only'])
            adopted_amount_edit.setReadOnly(True)
            adopted_amount_edit.editingFinished.connect(self.calculate_adopted_pitching_rate)
            adopted_amount_edit.setMaximumSize(60,30)
            hl23.addWidget(adopted_amount_edit)
            adopted_amount_unit=QLabel('g')
            adopted_amount_unit.setMaximumSize(30,30)
      
            hl23.addWidget(adopted_amount_unit) 
        
            vl2.addLayout(hl23)  

        hl.addLayout(vl2)
        hl.addStretch()
        
        self.yeast_layout.addLayout(hl)
    def show_equipment_dialog(self):
        self.equipmentDialog.show()  
        
    def showEvent(self,ev):
        self.set_translatable_textes()
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
        self.hide_session_feedback()
        widgets=self.util.get_included_widgets(self.feedback_groupbox_layout)
        for w in widgets:
            w.hide()
            
        self.hide_session_designation() 
        #self.date_edit.setDate(date) 
        #self.show_folder_chooser()

        
    def  show_folder_chooser(self):
        
        #if getattr( sys, 'frozen', False ) :
        # running in a bundle
        return #not used at the moment
                
    def show_import_export_dialog(self):
        'bundle_dir is preset during initialization of this main window'      
        self.importExportDbDialog.show()
          
    def show_hop_dialog(self):
        ##print('MainWindow : showing hop dialog')
        self.hopDialog.show() 
        
    
    def show_recipe_dialog(self):
        ##print('MainWindow : showing recipe dialog')
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
        
        
    def zero_ibu_bar(self): 
        mypb=  self.util.get_by_name(self.hops_header_layout,'ibu') 
        if  mypb: mypb.setValue(0)
        
    def zero_pitching_bar(self):
        mypb=self.util.get_by_name(self.yeast_header_layout,'pitching')  
        if mypb: mypb.setValue(0)  
        
    def update_pitching_bar(self,target,value):
        mypb=self.util.get_by_name(self.yeast_header_layout,'pitching')
        mypb.setRange(0,target *2*100)
        if value<=target*2:
            mypb.setValue(value*100)
        else:
            mypb.setValue(value*2*100)  
                      
        val_rate='{0:.2f}'.format(value)
        val_target='{0:.2f}'.format(target)
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
            duration_unit_edit.setMaximumWidth(40)
            hl.addWidget(duration_unit_edit)
            
            temperature_edit=QLineEdit()
            temperature_edit.setAccessibleName('temperature')
            temperature_edit.setMaximumSize(60,30)#temperature
            temperature_edit.setStyleSheet(sty.field_styles['read_only'])
            temperature_edit.setReadOnly(True)  
            temperature_edit.setText(str(r.temperature))
            hl.addWidget(temperature_edit)
            
            temperature_unit_edit=QLabel('°C')
            temperature_unit_edit.setAccessibleName('temperature_unit')
            temperature_unit_edit.setMaximumWidth(40)
            hl.addWidget(temperature_unit_edit)            
   
            self.rest_layout.addLayout(hl)      
            

        
if __name__ == "__main__":
 
    app = QApplication(sys.argv)
    MainWindow = MainWindow(translator)
    ui = MainWindowUI.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())    