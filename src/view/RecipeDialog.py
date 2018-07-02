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
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,QLabel,QComboBox,QHBoxLayout,QLineEdit,QPushButton,QMessageBox,QVBoxLayout

from gen import RecipeDialogUI


from model.Recipe import Recipe
from model.MaltInMash import MaltInMash
from model.HopInRecipe import HopInRecipe
from model.YeastInRecipe import YeastInRecipe
from model.RestInRecipe import RestInRecipe
import view.constants as vcst
import view.styles as sty
from view.MaltChooser import MaltChooser
from view.HopChooser import HopChooser
from view.YeastChooser import YeastChooser



from view.RestDialog import RestDialog

from PyQt5.QtCore import pyqtSignal


class customLabel(QLabel):
    '''
    A class to functionally transform label into a clickable button
    '''
    clicked = pyqtSignal()
    
    def __init__(self,caption):
        QLabel.__init__(self)
        self.setText(caption)
        self.setStyleSheet(vcst.CUSTOM_LABEL_STYLE)
        
    def set_caption(self,caption):
        self.setText(caption)   
        
    def set_font(self,font):
        print('inside customLabel setFont')
        self.setFont(font)     

    def mousePressEvent(self,event):
        #print('MousePressEvent')
        self.clicked.emit()


class RecipeDialog(QWidget,RecipeDialogUI.Ui_Form ):
    '''
    classdocs
    '''

    def __init__(self,model,controller,util):
        
        QWidget.__init__(self,None,QtCore.Qt.WindowStaysOnTopHint) 
        self.setupUi(self)
        self.model = model
        self.controller=controller
        self.util=util
        self.current_recipe=None # the recipe currently selected
        #get the list of malts from db and load into the malt_list widget
        self.malt_key_list=self.model.malt_list 
        self.recipe_key_list=self.model.recipe_list
        # register function with model for future model update announcements
        self.set_subscriptions()
        self.malt_type_list=[]
        self.rest_list=[]
        self.malt_chooser=MaltChooser(self)
        self.hop_chooser=HopChooser(self)
        self.yeast_chooser=YeastChooser(self)
        self.rest_dialog=RestDialog(self)         
        self.refresh_recipe_list_widget()          
        self.list_malt_in_mash=[]
        self.list_hop_in_recipe=[]   
        self.targeted_original_gravity_edit.setAccessibleName('Targeted Original Gravity')
        self.targeted_original_gravity_label.setAccessibleName('Targeted Original Gravity Label')
        self.targeted_original_gravity_unit_label.setAccessibleName('Targeted Original Gravity Unit Label')
        self.add_subdialog_buttons()   
        self.malt_for_mash_label.setMaximumSize(300,30)
        self.malt_for_mash_label.setMinimumSize(300,30)
        self.mash_rests_label.setMaximumSize(300,30)
        self.mash_rests_label.setMinimumSize(300,30)
        self.hop_list_label.setMaximumSize(300,30)
        self.hop_list_label.setMinimumSize(300,30)
        self.adjuncts_list_label.setMaximumSize(300,30)
        self.adjuncts_list_label.setMinimumSize(300,30)
        self.recipe_add_button.hide()
        self.recipe_update_button.hide()
        self.recipe_cancel_button.hide()
        self.recipe_add_button.setStyleSheet('background-color:lightgreen')
        self.recipe_update_button.setStyleSheet('background-color:lightgreen')
        self.recipe_cancel_button.setStyleSheet('background-color:pink')   
        self.init_dialog_and_connections()
        self.recipe_edit_button.hide()
        self.recipe_delete_button.hide()
        self.recipe_new_button.show()

        
    def add_hop_view(self,hop_type,usage=None,duration=None,hop_rate=None): 
        'prepare a hop view from the data loaded and add it to the hop layout' 
        hopT=hop_type
        hl=QHBoxLayout()
        
        name_edit=QLineEdit()
        name_edit.setAccessibleName('name')
        name_edit.setMinimumSize(400,30)
        name_edit.setText(hopT.name)
        hl.addWidget(name_edit)
        
        info_label=QLabel()
        info_label.setMinimumSize(400,30)
        info_label.setAccessibleName('info')
        info= ' – '+hopT.form + ' – ' +str(hopT.alpha_acid)+ ' % AA'
        info_label.setText(info) 
        hl.addWidget(info_label)

        usage_combo=QComboBox()
        usage_combo.setAccessibleName('usage')
        usage_combo.setStyleSheet(sty.field_styles['editable'])
        usage_combo.setMinimumWidth(150)
        hl.addWidget(usage_combo)
        
        'in the menu view we use the val i.e. the translated string'
        for key,val in self.util.hop_usage_dic.items():
            usage_combo.addItem(val)
        try:        
            index = usage_combo.findText(self.util.hop_usage_dic[usage])
        except:
            index=0  
        if index and index >= 0:
            usage_combo.setCurrentIndex(index) 
        usage_combo.currentIndexChanged.connect(self.show_hide_hop_duration)    
            
        duration_edit=QLineEdit()   
        duration_edit.setAccessibleName('duration')
        hl.addWidget(duration_edit)
        duration_edit.setStyleSheet(sty.field_styles['editable'])
        duration_edit.setMaximumSize(40,30)
        if duration:
            duration_edit.setText(str(duration))     
             
        duration_unit_label=QLabel() 
        duration_unit_label.setText('min')
        duration_unit_label.setAccessibleName('duration_unit')
        hl.addWidget(duration_unit_label)
        hl.addStretch()
        

        self.add_hop_rate(hl,hop_rate)
        delete_button=QPushButton('X')
        delete_button.setAccessibleName('delete_button')
        delete_button.setMaximumSize(20,30)
        delete_button.setStyleSheet(vcst.BUTTON_DELETE_STYLE)  
        delete_button.clicked.connect(self.remove_hop_view) 
        hl.addWidget(delete_button)
        
        name_edit.setFont(self.model.in_use_fonts['field'])
        info_label.setFont(self.model.in_use_fonts['field'])
        usage_combo.setFont(self.model.in_use_fonts['field'])
        duration_edit.setFont(self.model.in_use_fonts['field'])
        
        
        self.hop_layout.addLayout(hl)
            
               
    def add_malt_view(self,malt_type,percent=None):
        maltT=malt_type    
        hl=QHBoxLayout()#create an horizontal layout to host widgets for one malt line
        
        name_edit=QLineEdit()
        name_edit.setAccessibleName('name')
        name_edit.setMinimumSize(400,30)
        name_edit.setReadOnly(True)
        name_edit.setText(maltT.name)
        hl.addWidget(name_edit)
        
        percentage_edit=QLineEdit()
        percentage_edit.setAccessibleName('percentage')
        percentage_edit.setMaximumSize(60,30)
        percentage_edit.setStyleSheet(sty.field_styles['editable'])
        hl.addWidget(percentage_edit)
        if percent:
            percentage_edit.setText(str(percent))
        
        percentage_unit=QLabel('%')   
        percentage_unit.setAccessibleName('percentage_unit')
        percentage_unit.setMaximumSize(30,30)
        #percentage_unit.setStyleSheet("font-size: 14px;")
        hl.addWidget(percentage_unit)      
        
        delete_button=QPushButton('X')
        delete_button.setAccessibleName('delete_button')
        delete_button.setMaximumSize(20,30)
        delete_button.setStyleSheet(vcst.BUTTON_DELETE_STYLE) 
        hl.addWidget(delete_button)
        delete_button.clicked.connect(self.remove_malt_view) 
        
        hidden_name=QLineEdit(maltT.name)
        hidden_name.setAccessibleName('hidden_name')
        hl.addWidget(hidden_name)
        hidden_name.hide()
        
        name_edit.setFont(self.model.in_use_fonts['field'])
        percentage_edit.setFont(self.model.in_use_fonts['field'])
        percentage_unit.setFont(self.model.in_use_fonts['field'])
        
      
        self.malt_layout.addLayout(hl)
    
    def alerte(self,texte):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        msg.setText(texte)
        msg.setWindowTitle(self.tr("Warning Text"))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_() 
        
        
    def set_yeast_view(self,yeast_type,rate=None):   
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
        
        vl1=QVBoxLayout()
        temp_label=QLabel(self.tr('Temperature range'),alignment=4)
        temp_label.setAccessibleName('temp_label')
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
        hl.addLayout(vl1)
        
        vl2=QVBoxLayout()
        hl2=QHBoxLayout()
        pitch_label=QLabel(self.tr('Pitching rate'),alignment=4)
        pitch_label.setAccessibleName('pitch_label')
        vl2.addWidget(pitch_label)
        
        rate_edit=QLineEdit()
        rate_edit.setAccessibleName('rate')
        rate_edit.setMaximumSize(60,30)
        rate_edit.setStyleSheet(sty.field_styles['editable'])
        hl2.addWidget(rate_edit)
        if rate:
            rate_edit.setText(str(rate))
        
        rate_unit=QLabel('billions/°P/liter')   
        rate_unit.setAccessibleName('rate_unit')
        rate_unit.setMaximumSize(150,30)
        #rate_unit.setStyleSheet("font-size: 14px;")
        hl2.addWidget(rate_unit)  
        vl2.addLayout(hl2)
        hl.addLayout(vl2)
        
        maker_edit.setFont(self.model.in_use_fonts['field'])
        name_edit.setFont(self.model.in_use_fonts['field'])
        form_edit.setFont(self.model.in_use_fonts['field'])
        temp_label.setFont(self.model.in_use_fonts['field'])
        pitch_label.setFont(self.model.in_use_fonts['field'])
        min_advised_temperature_edit.setFont(self.model.in_use_fonts['field'])
        min_allowed_temperature_edit.setFont(self.model.in_use_fonts['field'])
        max_advised_temperature_edit.setFont(self.model.in_use_fonts['field'])
        max_allowed_temperature_edit.setFont(self.model.in_use_fonts['field'])
        rate_edit.setFont(self.model.in_use_fonts['field'])
        rate_unit.setFont(self.model.in_use_fonts['field'])
        
        
        self.yeast_layout.addLayout(hl)
        
        
    def aroma_explain(self):
        mess='''
        Checking the aromatic checkbox allows you to define 
        a pitching rate for the hop used, and means that  
        this rate is fixed and will not be modified in the 
        brewing session contrarily to  the other hop that 
        are used for bitterness and for which an amount can 
        be adjusted to reach a given bitterness target.'''
        self.util.alerte(self.tr(mess))   

        
  
        
    def add_subdialog_buttons(self):
        caption=self.tr('+ Add a malt')
        self.show_malt_chooser_button = customLabel('')
        self.show_malt_chooser_button.setText('+ Add a malt')
        self.show_malt_chooser_button.clicked.connect(self.malt_chooser_show)
        self.malt_header_layout.insertWidget(1,self.show_malt_chooser_button)
        
       
        caption=self.tr('+ Add a hop')
        self.show_hop_chooser_button = customLabel(caption)
        self.show_hop_chooser_button.clicked.connect(self.hop_chooser_show)
        self.hop_header_layout.insertWidget(1,self.show_hop_chooser_button)
        
        caption=self.tr('+ Add an adjunct')
        self.show_adjunct_chooser_button = customLabel(caption)
        self.show_adjunct_chooser_button.clicked.connect(self.adjunct_chooser_show)
        self.adjunct_header_layout.insertWidget(1,self.show_adjunct_chooser_button)
        
        caption=self.tr('+ Add a rest')
        self.show_rest_dialog_button = customLabel(caption)
        self.show_rest_dialog_button.clicked.connect(self.rest_dialog_show)
        self.rest_header_layout.insertWidget(1,self.show_rest_dialog_button)  
        
        caption='+ Select or change the yeast'
        self.show_yeast_chooser_button =customLabel(caption)
        self.show_yeast_chooser_button.clicked.connect(self.yeast_chooser_show)
        self.yeast_header_layout.insertWidget(1,self.show_yeast_chooser_button)
        
         
        
    def adjunct_chooser_show(self):
        return
        self.adjunct_chooser.show()    
         
        
    def alerte_sum_percentage(self,val): 
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        text=self.tr('Sum of percentage for malts must be 100, presently it is : ')+str(float(val))
        msg.setText(text)
        msg.setWindowTitle(self.tr("Warning percentages"))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()   


    def add_hop_rate(self,layout,value=None):
        'add an input for hop rate in the layout'
        hop_rate_edit=QLineEdit()
        hop_rate_edit.setAccessibleName('hop_rate')
        hop_rate_edit.setFont(self.model.in_use_fonts['field'])
        hop_rate_edit.setMaximumSize(50,30)
        hop_rate_edit.setMinimumSize(50,30)
        hop_rate_edit.setStyleSheet(sty.field_styles['editable'])
        layout.addWidget(hop_rate_edit)
        hop_rate_unit_label=QLabel('g/l')
        hop_rate_unit_label.setAccessibleName('hop_rate_unit')
        hop_rate_unit_label.setFont(self.model.in_use_fonts['field'])
        layout.addWidget(hop_rate_unit_label)
        if value: hop_rate_edit.setText(str(value))            
                               
    def clear_edits(self):
        self.recipe_name_edit.setText('')
        self.util.clearLayout(self.malt_layout) 
        self.util.clearLayout(self.yeast_layout)
        self.targeted_bitterness_edit.setText('')
        self.targeted_original_gravity_edit.setText('')
        self.boiling_time_edit.setText('')
        self.fermentation_explain_edit.setText('')          
        
        
    def closeEvent(self,event):   
        self.malt_chooser.close() 
        self.rest_dialog.close()
        self.hop_chooser.close() 
        self.close()
                       

    def delete_recipe(self):
        recipe=self.model.get_recipe(self.recipe_list_widget.currentItem().text())
        self.current_recipe=None
        self.model.remove_recipe(recipe.name)
        self.refresh_recipe_list_widget()  
        self.util.clearLayout(self.malt_layout)  
        self.clear_edits()        
                         
                         
    def edit_recipe(self):
        self.recipe_add_button.setText(self.tr('Add this recipe'))  
        
        self.recipe_add_button.hide()
        self.recipe_update_button.show()
        self.recipe_cancel_button.show()
        self.recipe_delete_button.hide()
        self.recipe_new_button.hide()
        self.recipe_edit_button.hide()
        self.unset_ro_and_color()
        self.update_rest_view(self.current_recipe, False)
        
                                 

    def hop_chooser_show(self):
        self.hop_chooser.show()      
        self.hop_chooser.window().raise_()    
        
        
    def insert_rest(self,position,rest):
        self.rest_list.insert(position,rest)
        self.update_rest_view(self.current_recipe, False)        
           
            
    def load_selected_recipe(self):
        if self.recipe_list_widget.currentItem():
            recipe=self.model.get_recipe(str(self.recipe_list_widget.currentItem().text()))        
            self.clear_edits()
            self.set_ro_and_color()
            self.recipe_name_edit.setText(recipe.name) 
            for m in recipe.malts_in_mash:
                malt= self.model.get_malt(m.malt)
                self.add_malt_view(malt, m.percentage)  
                
            if hasattr(recipe,'mash_rests'):
                self.update_rest_view(recipe)
                
            if hasattr(recipe,'hops_in_recipe'):
                self.update_hop_view(recipe)    
                
            if hasattr(recipe,'targeted_original_gravity'):
                self.targeted_original_gravity_edit.setText(str(recipe.targeted_original_gravity))   
                
            if hasattr(recipe,'targeted_bitterness'):
                self.targeted_bitterness_edit.setText(str(recipe.targeted_bitterness))   
                
            if hasattr(recipe,'boiling_time'):
                self.boiling_time_edit.setText(str(recipe.boiling_time))   
                
            if hasattr(recipe,'yeast_in_recipe'):
                yir=recipe.yeast_in_recipe
                yeast=self.model.get_yeast(yir.yeast)  
                self.set_yeast_view(yeast, yir.pitching_rate)  
                
            if hasattr(recipe,'fermentation_explanation'):
                self.fermentation_explain_edit.setPlainText(recipe.fermentation_explanation)          
                 
            self.set_ro_and_color()    
            self.current_recipe=recipe.name
    
    def malt_chooser_show(self):
        self.malt_chooser.show()      
        self.malt_chooser.window().raise_()
              
            
    def new_recipe(self):
        self.recipe_add_button.setText(self.tr('Record this new recipe'))
        self.util.clearLayout(self.malt_layout)
        self.util.clearLayout(self.rest_layout)
        self.util.clearLayout(self.hop_layout)
        self.recipe_list_widget.clear()
        
        self.recipe_add_button.show()
        self.recipe_update_button.hide()
        self.recipe_cancel_button.show()
        self.recipe_edit_button.hide()
        self.recipe_delete_button.hide()
        self.recipe_new_button.hide()
        self.unset_ro_and_color()
        self.clear_edits() 
        self.rest_list=[]
        
    def cancel(self):
        'after canceling an update or a creation'  
        'to prevent reselect after cancellation or creation'
        self.current_recipe=None
        self.selection_changed_recipe()  
        self.refresh_recipe_list_widget()
        'because selection_changed show them'
        self.recipe_edit_button.hide()
        self.recipe_delete_button.hide()
        self.recipe_new_button.show()    
        
        
    def on_model_changed_recipe(self,target):
        '''
        This function is called by the model when it changes
        due to the fact that it is subscribed as callback
        on initialization
        '''
        if target == 'recipe':
            self.recipe_key_list=self.model.recipe_list 
            self.refresh_recipe_list_widget()   
            
        if target == 'fontset':
            if (self.model.in_use_fonts):
                self.set_fonts()         
    
    def prepare_a_recipe_to_save(self):
        """" Read the GUI to prepare a recipe for adding or updating it into the database
        """
        util=self.util
        'Malts in mash'
        self.list_malt_in_mash =[]
        sum_percentage=0
        for i in range(self.malt_layout.count()):
            item =self.malt_layout.itemAt(i)
            
            if item:
                w_hidden_name=self.util.get_by_name(item.layout(),'hidden_name')
                t=w_hidden_name.text()
                w_percentage=self.util.get_by_name(item.layout(),'percentage')
                p=util.check_input(w_percentage, False,self.tr('Percentage'),False,0,100)
                if not p:
                    print('return at 1 in prepare_a_recipe_to_save')
                    return
                sum_percentage=sum_percentage+p           
                malt_in_mash=MaltInMash(t,p)
                self.list_malt_in_mash.append(malt_in_mash)
                
        if sum_percentage != 100 :
            self.alerte_sum_percentage(sum_percentage) 
            return  
        name=util.check_input(self.recipe_name_edit,True,self.tr('Repipe name'))
        if not name:
            print('return at 2 in prepare_a_recipe_to_save')
            return
        
        'gravity, boiling time and bitterness'
        gravity=util.check_input(self.targeted_original_gravity_edit,False,self.tr('Targeted Original Gravity'),False,1.030,1.140)
        if not gravity: return 
        
        bitterness=util.check_input(self.targeted_bitterness_edit,False,self.tr('Targeted bitterness'),False,0, 1000)
        if not bitterness: 
            print('return at 3 in prepare_a_recipe_to_save')
            return
        
        boiling_time = util.check_input(self.boiling_time_edit,False,self.tr('Boiling Time'),False, 30,200)
        if not boiling_time: return
        
        'Rests'
        self.rest_list=[]
        for i in range(self.rest_layout.count()):
            item=self.rest_layout.itemAt(i)#get a row item
            if item:
                w_purpose=self.util.get_by_name(item.layout(),'purpose')#the purpose widget
                purpose=util.check_input(w_purpose,True,self.tr('Rest purpose'))
                if not purpose: return
                
                w_duration=self.util.get_by_name(item.layout(),'duration') 
                duration=util.check_input(w_duration,False,self.tr('Rest duration'),False,0,200)
                if not duration: return
                
                w_temperature=self.util.get_by_name(item.layout(),'temperature')
                temperature=util.check_input(w_temperature,False,self.tr('Rest temperature'),False,0,100)
                if not temperature: return
                
                rest=RestInRecipe(purpose, duration,temperature)
                self.rest_list.append(rest)

                   
        'Hops in recipe'
        #print('reaching hops in recipe')
        self.list_hop_in_recipe=[]
        for i in range(self.hop_layout.count()):
            item=self.hop_layout.itemAt(i)
            if item:
                tx=item.layout().itemAt(0).widget().text() 
                #aromatic_checkbox=self.util.get_by_name_recursive(item.layout(), 'aroma')
              
                hop_rate_edit=self.util.get_by_name_recursive(item.layout(), 'hop_rate')
                if not hop_rate_edit: 
                    self.alerte(self.tr('Hop rate is not accessible'))
                    return
                hop_rate=util.check_input(hop_rate_edit,False,self.tr('Hop rate'),False, 0,100)
   
                'in the database we store the key name, not the translated string'
                'This way of doing things allows to change the language even after hops have been stored in the database'
                usage=self.util.get_usage_key(item.layout().itemAt(2).widget().currentText())
                if not usage : return
                
                if usage == vcst.HOP_BOILING_HOPPING:
                    duration=util.check_input(item.layout().itemAt(3).widget(),False,self.tr('Hop Duration'),False,0,1000)  
                    if not duration: return
                    hir=HopInRecipe(tx,usage,duration,hop_rate)
                else:
                    duration=None
                    hir=HopInRecipe(tx,usage,duration,hop_rate)
                      
                self.list_hop_in_recipe.append(hir)    
   
                
        'Yeast in recipe'
        yeast_name_edit=self.util.get_by_name_recursive(self.yeast_layout,'name')
      
        if not yeast_name_edit: 
            self.alerte('You must select a yeast')
        else: yeast_name= yeast_name_edit.text()
        w=self.util.get_by_name_recursive(self.yeast_layout, 'rate')
        if not w: return 
        pitching_rate=util.check_input(w,False,self.tr('Pitching Rate'),False, 0,1)
        if not pitching_rate: return
        yir=YeastInRecipe(yeast_name,pitching_rate)
        fermentation_explanation=self.fermentation_explain_edit.toPlainText()
                    
               
        'use previous to make a Recipe object'
        recipe=Recipe(name,self.list_malt_in_mash,self.rest_list,\
                      self.list_hop_in_recipe,gravity,bitterness,boiling_time,yir,fermentation_explanation)
        self.current_recipe=recipe.name
        #last add it to the database
        self.malt_chooser.close()
        self.hop_chooser.close()
        self.rest_dialog.close()
        #self.adjunct_chooser.close()
        self.yeast_chooser.close()
        return recipe    
        
    def refresh_recipe_list_widget(self,select=None):
        self.recipe_list_widget.clear()
        for key in self.recipe_key_list:
            self.recipe_list_widget.addItem(key)

        if self.current_recipe:
            item=self.recipe_list_widget.findItems(self.current_recipe,QtCore.Qt.MatchExactly)
            self.recipe_list_widget.setCurrentItem(item[0])      
    
            
    def remove_malt_view(self):
        'remove a malt view from the GUI after the user used the Delete button'
        s= self.sender()
        for i in range(self.malt_layout.count()):
            item =self.malt_layout.itemAt(i)
            if item:
                if s == item.layout().itemAt(3).widget():
                    self.util.clearLayout(item.layout())
                    self.malt_layout.removeItem(item)
                    return   
            
                
    def remove_rest_view(self):
        
        s=self.sender()
        for i in range(self.rest_layout.count()):
            item = self.rest_layout.itemAt(i)
            if item:
                if s == item.layout().itemAt(5).widget():
                    del self.rest_list[i]
                    self.update_rest_view(self.current_recipe, False)
                    self.rest_dialog.update_rest_list()
                    return   
           
                
    def remove_hop_view(self):
        'remove a hop view from the GUI after the user used Delete button in it'
        s=self.sender()
        for i in range(self.hop_layout.count()):
            item = self.hop_layout.itemAt(i)
            if item:
                delete_button=self.util.get_by_name_recursive(item.layout(),'delete_button')
                #if s == item.layout().itemAt(5).widget():#5 est la position du bouton 
                if s == delete_button:
                    self.util.clearLayout(item.layout())  
                    self.hop_layout.removeItem(item)
                    return             
    
    
    def rest_dialog_show(self):
        self.rest_dialog.show()
        self.rest_dialog.window().raise_()
        
    def set_fonts(self):
        
        print('enter set_fonts')
        
        self.show_malt_chooser_button.setFont(self.model.in_use_fonts['title_slanted']) 
        self.show_hop_chooser_button.setFont(self.model.in_use_fonts['title_slanted'])  
        self.show_adjunct_chooser_button.setFont(self.model.in_use_fonts['title_slanted'])  
        self.show_rest_dialog_button.setFont(self.model.in_use_fonts['title_slanted']) 
        self.show_yeast_chooser_button.setFont(self.model.in_use_fonts['title_slanted'])
        
        self.recipe_list_label.setFont(self.model.in_use_fonts['title'])
        self.recipe_list_widget.setFont(self.model.in_use_fonts['field'])
        self.recipe_edit_button.setFont(self.model.in_use_fonts['button'])
        self.recipe_delete_button.setFont(self.model.in_use_fonts['button'])
        self.recipe_add_button.setFont(self.model.in_use_fonts['button'])
        
        self.recipe_name_edit.setFont(self.model.in_use_fonts['field'])
        self.recipe_name_label.setFont(self.model.in_use_fonts['title'])
        self.targets_name_label.setFont(self.model.in_use_fonts['title'])
        self.targeted_original_gravity_label.setFont(self.model.in_use_fonts['field'])
        self.targeted_original_gravity_edit.setFont(self.model.in_use_fonts['field'])
        self.targeted_bitterness_unit_label.setFont(self.model.in_use_fonts['field'])
        self.targeted_bitterness_edit.setFont(self.model.in_use_fonts['field'])
        self.targeted_bitterness_label.setFont(self.model.in_use_fonts['field'])
        
        self.mash_label.setFont(self.model.in_use_fonts['title'])
        self.malt_for_mash_label.setFont(self.model.in_use_fonts['title_slanted'])
        self.mash_rests_label.setFont(self.model.in_use_fonts['title_slanted'])
        
        self.boiling_label.setFont(self.model.in_use_fonts['title'])
        self.boiling_time_label.setFont(self.model.in_use_fonts['field'])
        self.boiling_time_edit.setFont(self.model.in_use_fonts['field'])
        self.boiling_time_unit_label.setFont(self.model.in_use_fonts['field'])
        
        self.hop_list_label.setFont(self.model.in_use_fonts['title_slanted'])
        'should be renamed as fermentation_label'
        self.boiling_label_2.setFont(self.model.in_use_fonts['title'])
        self.adjuncts_list_label.setFont(self.model.in_use_fonts['title_slanted'])
        self.fermentation_explain_edit.setFont(self.model.in_use_fonts['field'])
        self.recipe_close_button.setFont(self.model.in_use_fonts['button'])
        
        for i in range(self.malt_layout.count()):
            item =self.malt_layout.itemAt(i)
            if item:
                w_name=self.util.get_by_name(item.layout(),'name')
                if w_name: w_name.setFont(self.model.in_use_fonts['field'])
                
                w_percentage=self.util.get_by_name(item.layout(),'percentage')
                if w_percentage: w_percentage.setFont(self.model.in_use_fonts['field'])
                
                w_percentage_unit=self.util.get_by_name(item.layout(),'percentage_unit')
                if w_percentage_unit: w_percentage_unit.setFont(self.model.in_use_fonts['field'])
                
              
        for i in range(self.hop_layout.count()):
            item=self.hop_layout.itemAt(i) 
            if item:
                w_name=self.util.get_by_name(item.layout(),'name')
                if w_name: w_name.setFont(self.model.in_use_fonts['field'])
                
                w_info=self.util.get_by_name(item.layout(),'info')
                if w_info: w_info.setFont(self.model.in_use_fonts['field'])
                
                w_usage=self.util.get_by_name(item.layout(),'usage')
                if w_usage: w_usage.setFont(self.model.in_use_fonts['field'])
                
                w_duration=self.util.get_by_name(item.layout(),'duration')
                if w_duration: w_duration.setFont(self.model.in_use_fonts['field'])
                
                w_duration_unit=self.util.get_by_name(item.layout(),'duration_unit')
                if w_duration_unit: w_duration_unit.setFont(self.model.in_use_fonts['field'])
                
                w_hop_rate=self.util.get_by_name_recursive(item.layout(),'hop_rate')
                if w_hop_rate: w_hop_rate.setFont(self.model.in_use_fonts['field'])
                else: print('hop_rate not found')
                
                w_hop_rate_unit=self.util.get_by_name_recursive(item.layout(),'hop_rate_unit')
                if w_hop_rate_unit: w_hop_rate_unit.setFont(self.model.in_use_fonts['field'])
                
        for i in range(self.yeast_layout.count()):
            item = self.yeast_layout.itemAt(i) 
            if item:
                       
                w_maker=self.util.get_by_name(item.layout(),'maker')
                if w_maker: w_maker.setFont(self.model.in_use_fonts['field'])
                
                w_name=self.util.get_by_name(item.layout(),'name')
                if w_name: w_name.setFont(self.model.in_use_fonts['field'])
                
                w_form=self.util.get_by_name(item.layout(),'form')
                if w_form: w_form.setFont(self.model.in_use_fonts['field'])
                
                w_temp_label=self.util.get_by_name_recursive(item.layout(),'temp_label')
                if w_temp_label: w_temp_label.setFont(self.model.in_use_fonts['field'])
                
                w_pitch_label=self.util.get_by_name_recursive(item.layout(),'pitch_label')
                if w_pitch_label: w_pitch_label.setFont(self.model.in_use_fonts['field'])
                
                w_min_allowed_temperature=self.util.get_by_name_recursive(item.layout(),'min_allowed_temperature')
                if w_min_allowed_temperature: w_min_allowed_temperature.setFont(self.model.in_use_fonts['field'])
                
                w_min_advised_temperature=self.util.get_by_name_recursive(item.layout(),'min_advised_temperature')
                if w_min_advised_temperature: w_min_advised_temperature.setFont(self.model.in_use_fonts['field'])
                
                w_max_advised_temperature=self.util.get_by_name_recursive(item.layout(),'max_advised_temperature')
                if w_max_advised_temperature: w_max_advised_temperature.setFont(self.model.in_use_fonts['field'])
                
                w_max_allowed_temperature=self.util.get_by_name_recursive(item.layout(),'max_allowed_temperature')
                if w_max_allowed_temperature: w_max_allowed_temperature.setFont(self.model.in_use_fonts['field'])
                
                w_rate=self.util.get_by_name_recursive(item.layout(),'rate')
                if w_rate: w_rate.setFont(self.model.in_use_fonts['field'])
                
                w_rate_unit=self.util.get_by_name_recursive(item.layout(),'rate_unit')
                if w_rate_unit: w_rate_unit.setFont(self.model.in_use_fonts['field'])
            
    
    
        
    def save_recipe(self):
        recipe=self.prepare_a_recipe_to_save()
        if not recipe: return #the dialog may have aborted because on field was let empty  
        'use the model to save the recipe'
        self.model.add_recipe(recipe)
        item=self.recipe_list_widget.findItems(recipe.name,QtCore.Qt.MatchExactly)
        self.recipe_list_widget.setCurrentItem(item[0])     
        self.set_ro_and_color()  
        self.recipe_add_button.hide() 
        self.recipe_delete_button.setEnabled(True)
        self.recipe_new_button.setEnabled(True)
      
           
    def selection_changed_recipe(self):
        #print('RecipeDialog : Recipe selection changed') 
        self.recipe_add_button.hide()
        self.recipe_update_button.hide()
        self.recipe_cancel_button.hide()
        self.load_selected_recipe() 
        self.recipe_edit_button.show()
        self.recipe_delete_button.show() 
        self.recipe_new_button.show()          
        
        
    def init_dialog_and_connections(self):
        self.recipe_edit_button.clicked.connect(self.edit_recipe)
        self.recipe_new_button.clicked.connect(self.new_recipe)
        self.recipe_delete_button.clicked.connect(self.delete_recipe)
        self.recipe_list_widget.currentItemChanged.connect(self.selection_changed_recipe)
        self.recipe_add_button.clicked.connect(self.save_recipe)  
        self.recipe_update_button.clicked.connect(self.update_recipe) 
        self.recipe_cancel_button.clicked.connect(self.cancel)
        self.recipe_close_button.clicked.connect(self.close)
        
        
         
        
    def set_ro_and_color(self):
        self.show_malt_chooser_button.hide()
        self.show_hop_chooser_button.hide()
        self.show_adjunct_chooser_button.hide()
        self.show_rest_dialog_button.hide()
        self.show_yeast_chooser_button.hide()
        self.recipe_name_edit.setReadOnly(True)
        self.recipe_name_edit.setStyleSheet(sty.field_styles['read_only'])
        self.targeted_original_gravity_edit.setReadOnly(True)
        self.targeted_original_gravity_edit.setStyleSheet(sty.field_styles['read_only'])
        self.targeted_bitterness_edit.setReadOnly(True)
        self.targeted_bitterness_edit.setStyleSheet(sty.field_styles['read_only'])
        self.boiling_time_edit.setReadOnly(True)
        self.boiling_time_edit.setStyleSheet(sty.field_styles['read_only'])
        
        'MALTS'
        for i in range(self.malt_layout.count()):
            item =self.malt_layout.itemAt(i)
            if item: 
                percentage_edit=self.util.get_by_name(item.layout(), 'percentage')
                if  percentage_edit: 
                    percentage_edit.setReadOnly(True)
                    percentage_edit.setStyleSheet(sty.field_styles['read_only'])
                delete_button=self.util.get_by_name(item.layout(), 'delete_button')  
                if delete_button: delete_button.hide()      
        
        'HOPS'        
        for i in range(self.hop_layout.count()):
            item = self.hop_layout.itemAt(i)       
            if item:                
                usage_combo=self.util.get_by_name(item.layout(), 'usage') 
                if usage_combo: 
                    usage_combo.setEnabled(False)
                    usage_combo.setStyleSheet(sty.field_styles['read_only'])
                duration_edit=self.util.get_by_name(item.layout(), 'duration')  
                if duration_edit:
                    duration_edit.setReadOnly(True)
                    duration_edit.setStyleSheet(sty.field_styles['read_only'])
                aroma_checkbox=self.util.get_by_name_recursive(item.layout(), 'aroma')  
                if aroma_checkbox: aroma_checkbox.setEnabled(False)  
                hop_rate_edit=self.util.get_by_name_recursive(item.layout(), 'hop_rate')
                if hop_rate_edit: 
                    hop_rate_edit.setReadOnly(True)
                    hop_rate_edit.setStyleSheet(sty.field_styles['read_only'])
                delete_button=self.util.get_by_name(item.layout(), 'delete_button')
                if delete_button: delete_button.hide()
                
        'YEAST'        
        pitching_rate_edit=self.util.get_by_name_recursive(self.yeast_layout, 'rate') 
        if pitching_rate_edit: 
            pitching_rate_edit.setReadOnly(True)
            pitching_rate_edit.setStyleSheet(sty.field_styles['read_only'])    
        
        w_min_allowed_temperature=self.util.get_by_name_recursive(self.yeast_layout,'min_allowed_temperature')
        if w_min_allowed_temperature: w_min_allowed_temperature.setStyleSheet(sty.field_styles['read_only']) 
                
        w_min_advised_temperature=self.util.get_by_name_recursive(self.yeast_layout,'min_advised_temperature')
        if w_min_advised_temperature: w_min_advised_temperature.setStyleSheet(sty.field_styles['read_only']) 
                
        w_max_advised_temperature=self.util.get_by_name_recursive(self.yeast_layout,'max_advised_temperature')
        if w_max_advised_temperature: w_max_advised_temperature.setStyleSheet(sty.field_styles['read_only']) 
                
        w_max_allowed_temperature=self.util.get_by_name_recursive(self.yeast_layout,'max_allowed_temperature')
        if w_max_allowed_temperature: w_max_allowed_temperature.setStyleSheet(sty.field_styles['read_only'])       
                
    def set_subscriptions(self):
        self.model.subscribe_model_changed(['recipe','fontset'],self.on_model_changed_recipe)
                         
    def set_translatable_textes(self):
        self.setWindowTitle(self.tr('Create a Recipe'))
        self.recipe_list_label.setText(self.tr('Recipe Database List'))
        self.recipe_name_label.setText(self.tr('Recipe Name'))
        self.targets_name_label.setText(self.tr('Recipe Targets'))
        self.targeted_original_gravity_label.setText(self.tr('Original gravity'))
        self.targeted_bitterness_label.setText(self.tr('Bitterness'))
        self.boiling_time_label.setText(self.tr('Boiling time'))
        self.recipe_edit_button.setText(self.tr('Edit'))
        self.recipe_delete_button.setText(self.tr('Delete'))
        self.recipe_new_button.setText(self.tr('New'))
        self.malt_for_mash_label.setText(self.tr('Malts for mash'))
        self.hop_list_label.setText(self.tr('Hops'))
        self.adjuncts_list_label.setText(self.tr('Adjuncts'))
        self.mash_rests_label.setText(self.tr('Mash Rests'))
        #self.add_subdialog_buttons()
        self.recipe_close_button.setText(self.tr('Close'))

        
   
    def showEvent(self,e):  
        self.set_translatable_textes()
        #self.add_subdialog_buttons#already done, just to refresh translation
        self.set_ro_and_color()
        self.set_fonts()
   
        
    def show_hide_hop_duration(self):
        'Hide the duration edit when not needed and show it when needed'
        send=self.sender()
        for i in range(self.hop_layout.count()):
            hl=self.hop_layout.itemAt(i).layout()
            if hl.itemAt(2).widget() == send:
                txt= hl.itemAt(2).widget().currentText()
                
                if txt ==self.util.hop_usage_dic[vcst.HOP_BOILING_HOPPING] :
                    hl.itemAt(3).widget().setEnabled(True)  
                    hl.itemAt(3).widget().setStyleSheet(sty.field_styles['editable']) 
                    hl.itemAt(3).widget().setReadOnly(False) 
                    
                else:
                    hl.itemAt(3).widget().setText('')
                    hl.itemAt(3).widget().setEnabled(False)
                    hl.itemAt(3).widget().setStyleSheet(sty.field_styles['read_only'])
                                 
                
    def unset_ro_and_color(self):
        self.show_malt_chooser_button.show()
        self.show_hop_chooser_button.show()
        self.show_adjunct_chooser_button.show()
        self.show_rest_dialog_button.show()    
        self.show_yeast_chooser_button.show()    
        self.recipe_name_edit.setReadOnly(False)
        self.recipe_name_edit.setStyleSheet(sty.field_styles['editable'])
        self.targeted_original_gravity_edit.setReadOnly(False)
        self.targeted_original_gravity_edit.setStyleSheet(sty.field_styles['editable'])
        self.targeted_bitterness_edit.setReadOnly(False)
        self.targeted_bitterness_edit.setStyleSheet(sty.field_styles['editable'])
        self.boiling_time_edit.setReadOnly(False)
        self.boiling_time_edit.setStyleSheet(sty.field_styles['editable'])
        
        for i in range(self.malt_layout.count()):
            item =self.malt_layout.itemAt(i)
            if item: 
                percentage_edit=self.util.get_by_name(item.layout(), 'percentage')
                if  percentage_edit: 
                    percentage_edit.setReadOnly(False)
                    percentage_edit.setStyleSheet(sty.field_styles['editable'])
                delete_button=self.util.get_by_name(item.layout(), 'delete_button')  
                if delete_button: delete_button.show() 
                
        for i in range(self.hop_layout.count()):
            item = self.hop_layout.itemAt(i)
            if item:
                usage_combo=self.util.get_by_name(item.layout(), 'usage') 
                if usage_combo:
                    usage_combo.setEnabled(True)
                    usage_combo.setStyleSheet(sty.field_styles['editable']) 
                    if (usage_combo.currentText()== self.util.hop_usage_dic[vcst.HOP_BOILING_HOPPING] ):
                        duration_edit=self.util.get_by_name(item.layout(), 'duration')
                        if duration_edit: 
                            duration_edit.setReadOnly(False) 
                            duration_edit.setStyleSheet(sty.field_styles['editable'])
                aroma_checkbox=self.util.get_by_name_recursive(item.layout(), 'aroma')  
                if aroma_checkbox: aroma_checkbox.setEnabled(True)  
                hop_rate_edit=self.util.get_by_name_recursive(item.layout(), 'hop_rate')
                if hop_rate_edit: 
                    hop_rate_edit.setReadOnly(False) 
                    hop_rate_edit.setStyleSheet(sty.field_styles['editable'])       
                delete_button=self.util.get_by_name(item.layout(), 'delete_button') 
                if delete_button: delete_button.show()   
                
        pitching_rate_edit=self.util.get_by_name_recursive(self.yeast_layout, 'rate') 
        if pitching_rate_edit: 
            pitching_rate_edit.setReadOnly(False) 
            pitching_rate_edit.setStyleSheet(sty.field_styles['editable']) 
                  
                
    def update_hop_view(self,recipe):
        self.list_hop_in_recipe.clear()
        self.util.clearLayout(self.hop_layout)
        for h in recipe.hops_in_recipe:
            hop=self.model.get_hop(h.hop)
            #print (str(h.hop))
            #print(str(h.usage))
            #print(str(h.hop_rate))   
            self.add_hop_view(hop, h.usage, h.duration,h.hop_rate)     
               
    def update_yeast_view(self,recipe):
        self.util.clearLayout(self.yeast_layout)
        yir=recipe.yeast_in_recipe
        yeast=self.model.get_yeast(yir.yeast)
        self.set_yeast_view(yeast,yir.pitching_rate)
        
    def update_recipe(self):
        boiling_time = self.util.check_input(self.boiling_time_edit,False,self.tr('Boiling Time'),False, 30,200)
        
        recipe=self.prepare_a_recipe_to_save()
        
        'use the model to save the recipe'
        self.model.update_recipe(recipe)
        item=self.recipe_list_widget.findItems(recipe.name,QtCore.Qt.MatchExactly)
        self.recipe_list_widget.setCurrentItem(item[0])     
        self.set_ro_and_color()  
        self.recipe_add_button.hide() 
        self.recipe_delete_button.setEnabled(True)
        self.recipe_new_button.setEnabled(True)    
            
    def update_rest_view_disabled(self,recipe,in_mem=True): 
        if in_mem: self.rest_list=recipe.mash_rests       
        self.util.clearLayout(self.rest_layout)
        for r in self.rest_list:
            rest_view=self.util.create_rest_view(r.purpose,r.duration,r.temperature,in_mem,recipe) 
            rest_view.itemAt(5).widget().clicked.connect(self.remove_rest_view)  
            self.rest_layout.addLayout(rest_view)     
                
    def update_rest_view(self,recipe,in_mem=True):
        '''
        if in_men=True update the rest_layout from the given recipe as is in database
        else update it from the temporary (under edition) rest list 
        '''
        edit_style=sty.field_styles['editable']
        ro=False
        if in_mem:
            self.rest_list=recipe.mash_rests
            edit_style=sty.field_styles['read_only']
            ro=True   
            
        self.util.clearLayout(self.rest_layout)
        for r in self.rest_list:
            hl=QHBoxLayout()
            purpose=QLineEdit()
            purpose.setAccessibleName('purpose')
            purpose.setMinimumSize(400,30)
            purpose.setStyleSheet(edit_style)
            purpose.setReadOnly(ro)
            hl.addWidget(purpose)
            purpose.setText(r.purpose)

            duration=QLineEdit()  
            duration.setAccessibleName('duration')
            duration.setMaximumSize(60,30)#duration
            duration.setStyleSheet(edit_style)
            duration.setReadOnly(ro)
            hl.addWidget(duration)
            duration.setText(str(r.duration))
            
            duration_unit =QLabel('min')
            duration_unit.setMaximumSize(40,30)
            hl.addWidget(duration_unit)
            
            temperature = QLineEdit()
            temperature.setAccessibleName('temperature')
            temperature.setMaximumSize(60,30)
            temperature.setStyleSheet(edit_style)
            temperature.setReadOnly(ro)  
            hl.addWidget(temperature)
            temperature.setText(str(r.temperature))
            
            temperature_unit =QLabel('°C')
            temperature_unit.setMaximumSize(40,30)
            hl.addWidget(temperature_unit)
            
            delete_button=QPushButton('X')
            delete_button.setAccessibleName('delete_button')
            delete_button.setStyleSheet(vcst.BUTTON_DELETE_STYLE)
            delete_button.setMaximumSize(20,30)
            delete_button.clicked.connect(self.remove_rest_view) 
            hl.addWidget(delete_button)
            if in_mem:
                delete_button.hide()
            else:
                delete_button.show()
                     
            self.rest_layout.addLayout(hl)      
            
                      
    def yeast_chooser_show(self):

        self.yeast_chooser.show()      
        self.yeast_chooser.window().raise_()     
        'remove the StayOnToHint for Recipe Dialog'
        #self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)   
        'as the previous hide it, show it again'   
        #self.show()      
               

        