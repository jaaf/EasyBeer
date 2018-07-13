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
from gen import FeedbackUI
from model.Hop import Hop
import view.styles as sty
import platform
import view.constants as vcst
from model.Unit import Unit

#from PyQt4.QtGui import QStandardItemModel,QStandardItem,QItemSelectionModel

class Feedback(QDialog,FeedbackUI.Ui_Dialog ):
    
    def __init__(self,model,util,parent=None):
        QDialog.__init__(self,None,QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.model=model
        self.util=util
        self.model.subscribe_model_changed(['fontset'],self.on_model_changed)
        self.set_connections()
        
    def cancel(self):
        'in order to discard last changes'
        self.load_feedback()
        
        
    def edit(self):
        self.set_writable()
    
    def explain(self,txt):
        mb=QMessageBox()
        mb.setIcon(QMessageBox.Information)
        mb.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        mb.setText(self.tr(''))
        mb.setInformativeText(txt)
        mb.setStandardButtons(QMessageBox.Ok)
        mb.exec_()
    
    def explain_fermentor_observation(self):
        txt=self.tr('''
        Describe here what you have observed during fermentation. How did you prepare your pitching. How long it took before bubbling. 
        How long was the high-growth phase? How long was the maturation phase? Did you transfer the wort into a secondary fermentor after 
        primary fermentation? Did you practice a cold conditionning?
        ''')
        self.explain(txt)
       
    def explain_fermentor_volume(self):
        txt=self.tr('It is the volume of wort you put into the fermentor just after cooling the wort')
        self.explain(txt)
    
    
    def explain_FG(self):
        txt=self.tr('The specific gravity you measured just before priming.')
        self.explain(txt)
    
    def explain_IG(self):
        txt=self.tr('If you transferred the wort into a secondary fermentor for secondary fermentation, what was the specific gravity at this time.')
        self.explain(txt)
    
    
    def explain_OG(self):
        txt=self.tr('The specific gravity you measured when transferring the wort from boiler to fermentor. Give it at 20 °C.')
        self.explain(txt)
    
    def explain_preboil_volume(self):
        txt=self.tr('The volume of wort in the boiler just at boil starting')
        self.explain(txt)
        
    
    def explain_quality(self):
        txt=self.tr('Give feedback on how the beer was and when.')
        self.explain(txt)
    
    
    def explain_water_treatment(self):
        txt=self.tr('Give feedback about what you did to prepare the water')
        self.explain(txt)
        
    def load_feedback(self):
        session=self.model.get_session(self.current_session_name)
        self.name_edit.setText(session.name)
        self.water_treatment_edit.setText(session.feedback_water_treatment_text)
        self.mash_PH_edit.setText(str(session.feedback_mash_ph))
        self.preboil_volume_edit.setText(str(session.feedback_preboil_volume))
        self.fermentor_volume_edit.setText(str(session.feedback_fermentor_volume))
        self.OG_edit.setText(str(session.feedback_original_gravity))
        self.IG_edit.setText(str(session.feedback_intermediate_gravity))
        self.FG_edit.setText(str(session.feedback_final_gravity))
        self.IG_time_elapsed.setText(str(session.feedback_IG_time_elapsed))
        self.FG_time_elapsed.setText(str(session.feedback_FG_time_elapsed))
        self.fermentation_observation_edit.setText(session.feedback_fermentation_observation)
        self.beer_quality_edit.setText(session.feedback_beer_quality_observation)
        self.set_ro()
        
                   
    
    def on_model_changed(self,target):
        print('model changed in feedback')
        if target == 'fontset':
            self.set_fonts()
     
    def save(self): 
        v_unit=self.model.get_unit('water_volume')
        t_unit=self.model.get_unit('temperature')
        'all accept None value'
        water_treatment=self.water_treatment_edit.toPlainText()
        mash_ph=self.util.check_input(self.mash_PH_edit, False,self.tr('mash_PH'), True, vcst.MIN_PH,vcst.MAX_PH,None,None)
        preboil_volume=self.util.check_input(self.preboil_volume_edit,False,self.tr('Preboil Volume'),True,0,vcst.MAX_VOLUME,None,v_unit)
        fermentor_volume=volume=self.util.check_input(self.fermentor_volume_edit,False,self.tr('Fermentor Volume'),True,0,vcst.MAX_VOLUME,None,v_unit)
        OG=self.util.check_input(self.OG_edit,False,self.tr('Original gravity'),True,0,vcst.MAX_OG,None,None)
        IG=self.util.check_input(self.IG_edit,False,self.tr('Intermediate gravity'),True,0,vcst.MAX_OG,None,None)
        FG=self.util.check_input(self.FG_edit,False,self.tr('Original gravity'),True,0,vcst.MAX_OG,None,None)
        IG_time_elapsed=self.util.check_input(self.IG_time_elapsed,False,self.tr('IG time elapsed since pitching'),True,0,7000,None,None)
        FG_time_elapsed=self.util.check_input(self.FG_time_elapsed,False,self.tr('FG time elapsed since pitching'),True,0,7000,None,None)
        fermentation_observation=self.fermentation_observation_edit.toPlainText()
        beer_quality_observation=self.beer_quality_edit.toPlainText()
        
        name=self.current_session_name
        feedback ={'name':name,
             'water_treatment': water_treatment,
             'mash_ph':mash_ph,
             'preboil_volume':preboil_volume,
             'fermentor_volume': fermentor_volume,
             'OG':OG,
             'IG':IG,
             'FG':FG,
             'IG_time_elapsed': IG_time_elapsed,
             'FG_time_elapsed': FG_time_elapsed,
             'fermentation_observation': fermentation_observation,
             'beer_quality_observation':beer_quality_observation}
        self.model.update_session(feedback)
        self.load_feedback()
        
    def set_connections(self):
        self.edit_button.clicked.connect(self.edit)    
        self.save_button.clicked.connect(self.save)
        self.cancel_button.clicked.connect(self.cancel)
        self.close_button.clicked.connect(self.close)
        self.water_treatment_button.clicked.connect(self.explain_water_treatment)
        self.preboil_button.clicked.connect(self.explain_preboil_volume)
        self.fermentor_button.clicked.connect(self.explain_fermentor_volume)
        self.OG_button.clicked.connect(self.explain_OG)
        self.IG_button.clicked.connect(self.explain_IG)
        self.FG_button.clicked.connect(self.explain_FG)
        self.fermentation_observation_button.clicked.connect(self.explain_fermentor_observation)
        self.observed_quality_button.clicked.connect(self.explain_quality)
        
        
    def set_fonts(self):
        self.edit_button.setFont(self.model.in_use_fonts['button'])
        self.save_button.setFont(self.model.in_use_fonts['button'])
        self.cancel_button.setFont(self.model.in_use_fonts['button'])
        self.close_button.setFont(self.model.in_use_fonts['button'])
        self.name_edit.setFont(self.model.in_use_fonts['field'])
        self.water_treatment_button.setFont(self.model.in_use_fonts['button'])
        self.preboil_button.setFont(self.model.in_use_fonts['button'])
        self.fermentor_button.setFont(self.model.in_use_fonts['button'])
        self.OG_button.setFont(self.model.in_use_fonts['button'])
        self.IG_button.setFont(self.model.in_use_fonts['button'])
        self.FG_button.setFont(self.model.in_use_fonts['button'])
        self.fermentation_observation_button.setFont(self.model.in_use_fonts['button'])
        self.observed_quality_button.setFont(self.model.in_use_fonts['button'])
        
        self.mash_PH_edit.setFont(self.model.in_use_fonts['field'])
        self.water_treatment_edit.setFont(self.model.in_use_fonts['field'])
        self.preboil_volume_edit.setFont(self.model.in_use_fonts['field'])
        self.fermentor_volume_edit.setFont(self.model.in_use_fonts['field'])
        self.OG_edit.setFont(self.model.in_use_fonts['field'])
        self.IG_edit.setFont(self.model.in_use_fonts['field'])
        self.FG_edit.setFont(self.model.in_use_fonts['field'])
        self.IG_time_elapsed.setFont(self.model.in_use_fonts['field'])
        self.FG_time_elapsed.setFont(self.model.in_use_fonts['field'])
        self.fermentation_observation_edit.setFont(self.model.in_use_fonts['field'])
        self.beer_quality_edit.setFont(self.model.in_use_fonts['field'])
        
        self.mash_PH_label.setFont(self.model.in_use_fonts['field'])
        self.preboil_volume_label.setFont(self.model.in_use_fonts['field'])
        self.preboil_volume_unit_label.setFont(self.model.in_use_fonts['field'])
        self.fermentor_volume_label.setFont(self.model.in_use_fonts['field'])
        self.fermentor_volume_unit_label.setFont(self.model.in_use_fonts['field'])
        self.OG_label.setFont(self.model.in_use_fonts['field'])
        self.IG_label.setFont(self.model.in_use_fonts['field'])
        self.IG_date_label.setFont(self.model.in_use_fonts['field'])
        self.FG_date_label.setFont(self.model.in_use_fonts['field'])
        
        self.feedback_label.setFont(self.model.in_use_fonts['title'])
        self.water_treatment_label.setFont(self.model.in_use_fonts['title_slanted'])
        self.observed_data_label.setFont(self.model.in_use_fonts['title_slanted'])
        self.Fermentation_observation_label.setFont(self.model.in_use_fonts['title_slanted'])
        self.observed_beer_quality_label.setFont(self.model.in_use_fonts['title_slanted'])
        
    def set_ro(self):
        self.water_treatment_edit.setStyleSheet(sty.field_styles['read_only'])   
        self.water_treatment_edit.setEnabled(False) 
        self.mash_PH_edit.setStyleSheet(sty.field_styles['read_only']) 
        self.mash_PH_edit.setEnabled(False)
        self.preboil_volume_edit.setStyleSheet(sty.field_styles['read_only']) 
        self.preboil_volume_edit.setEnabled(False)
        self.fermentor_volume_edit.setStyleSheet(sty.field_styles['read_only']) 
        self.fermentor_volume_edit.setEnabled(False)
        self.OG_edit.setStyleSheet(sty.field_styles['read_only']) 
        self.OG_edit.setEnabled(False)
        self.IG_edit.setStyleSheet(sty.field_styles['read_only']) 
        self.IG_edit.setEnabled(False)
        self.FG_edit.setStyleSheet(sty.field_styles['read_only']) 
        self.FG_edit.setEnabled(False)
        self.IG_time_elapsed.setStyleSheet(sty.field_styles['read_only']) 
        self.IG_time_elapsed.setEnabled(False)
        self.FG_time_elapsed.setStyleSheet(sty.field_styles['read_only']) 
        self.FG_time_elapsed.setEnabled(False)
        self.fermentation_observation_edit.setStyleSheet(sty.field_styles['read_only'])  
        self.fermentation_observation_edit.setEnabled(False) 
        self.beer_quality_edit.setStyleSheet(sty.field_styles['read_only'])  
        self.beer_quality_edit.setEnabled(False)   
        self.save_button.hide()
        self.cancel_button.hide()
        self.edit_button.show()
        
    def set_writable(self):
        self.water_treatment_edit.setStyleSheet(sty.field_styles['editable'])   
        self.water_treatment_edit.setEnabled(True) 
        self.mash_PH_edit.setStyleSheet(sty.field_styles['editable']) 
        self.mash_PH_edit.setEnabled(True)
        self.preboil_volume_edit.setStyleSheet(sty.field_styles['editable']) 
        self.preboil_volume_edit.setEnabled(True)
        self.fermentor_volume_edit.setStyleSheet(sty.field_styles['editable']) 
        self.fermentor_volume_edit.setEnabled(True)
        self.OG_edit.setStyleSheet(sty.field_styles['editable']) 
        self.OG_edit.setEnabled(True)
        self.IG_edit.setStyleSheet(sty.field_styles['editable']) 
        self.IG_edit.setEnabled(True)
        self.FG_edit.setStyleSheet(sty.field_styles['editable']) 
        self.FG_edit.setEnabled(True)
        self.IG_time_elapsed.setStyleSheet(sty.field_styles['editable']) 
        self.IG_time_elapsed.setEnabled(True)
        self.FG_time_elapsed.setStyleSheet(sty.field_styles['editable']) 
        self.FG_time_elapsed.setEnabled(True)
        self.fermentation_observation_edit.setStyleSheet(sty.field_styles['editable'])  
        self.fermentation_observation_edit.setEnabled(True) 
        self.beer_quality_edit.setStyleSheet(sty.field_styles['editable'])  
        self.beer_quality_edit.setEnabled(True) 
        self.save_button.show()
        self.cancel_button.show()
        self.edit_button.hide()
        
        
        
    def set_session_name(self,name):
        self.current_session_name=name    
        
    def showEvent(self,event):
        self.set_fonts()   
        self.load_feedback()     
        
        
        