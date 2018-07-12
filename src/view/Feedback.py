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
        
        
    def edit(self):
        pass    
    
    def explain_fermentor_observation(self):
        pass
    

    def explain_fermentor_volume(self):
        pass
    
    
    def explain_FG(self):
        pass
    
    def explain_IG(self):
        pass
    
    
    def explain_OG(self):
        pass
    
    
    def explain_preboil_volume(self):
        pass
    
    def explain_quality(self):
        pass
    
    
    def explain_water_treatment(self):
        pass
    
    
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
        
    def set_connections(self):
        self.edit_button.clicked.connect(self.edit)    
        self.save_button.clicked.connect(self.save)
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
        
    def set_session_name(self,name):
        self.current_session_name=name    
        
    def showEven(self,event):
        self.set_fonts()        
        
        
        