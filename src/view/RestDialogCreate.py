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


from PyQt5.QtWidgets import  QWidget

from gen import RestDialogCreateUI

from model.Rest import Rest
import model.constants as mcst
import view.styles as sty
import view.constants as vcst
import platform



class RestDialogCreate(QWidget,RestDialogCreateUI.Ui_Form ):
    """
       class docs
    """   


    def __init__(self,model,controller,util):
        QWidget.__init__(self)
        self.setupUi(self)
        self.model = model
        self.controller=controller
        self.util=util
        self.current_rest=None # the rest currently selected
        
        # register function with model for future model update announcements
        self.model.subscribe_model_changed(['rest','fontset'],self.on_model_changed_rest_create)
        
        self.add_button.hide()
        self.cancel_button.hide()
        self.delete_button.hide()
        self.edit_button.hide()
        self.update_button.hide()
        self.set_ro()
        self.init_dialog_and_connections()
        
             
        self.rest_key_list=self.model.rest_list        
        self.ensure_unremovable_rests()  
        self.refresh_rest_list_combo()  
        
        

        
    def cancel(self):
        self.clear_edits()
        self.set_ro()
        self.cancel_button.hide()
        self.add_button.hide()
        self.update_button.hide()
        self.new_button.show()
        pass    
        
    def clear_edits(self):
        self.refresh_rest_list_combo()
        self.name_edit.setText('')
        for i in range(self.ph_layout.count()):
            item=self.ph_layout.itemAt(i)
            if item:
                item.widget().setText('')
        for i in range(self.temperature_layout.count()):
            item=self.temperature_layout.itemAt(i)
            if item:
                item.widget().setText('')
        self.usage_guidance_edit.setText('')        
     
    def create_unremovable_rests(self):
      
       
        self.TEXT_REST_BETA_GLUCANASE=self.tr('''<h2 style="color:red; font-style:italic;">This rest cannot be edited or deleted</h2>
        <h2>Beta-glucanase Rest</h2>
            <p>When using a significant amount of unmalted barley, and/or rye, oatmeal, wheat the mash may become too stiff and
            cause lautering difficulties. The stiffness comes from beta-glucan polysaccharides. Beta-glucan polysaccharides can be
            broken down using a rest of about 20 min. at 104-108 &deg;F</p>
            <p>Such a rest is recommended when using more than 20&nbsp;% of unmalted or flaked barley, oatmeal or wheat in the grain bill.
            It is optional when this percentage is between 10&nbsp;% and 20&nbsp;%.''')
        
        self.beta_glucan_rest=Rest('Beta-glucanase Rest',[4.5,5,5.5,6],[28,40,48,49],self.TEXT_REST_BETA_GLUCANASE,'no')
        
        TEXT_REST_PROTEIN=self.tr('''
           
            <h2 style="color:red; font-style:italic;">This rest cannot be edited or deleted</h2>
            <h2>Protein Rest</h2>
            <p>During malting and mashing, amino acids are cleaved from the peptides (amino acid chains)  by
            specialized enzymes called 'proteolytic enzymes' ( proteolysis being the breakdown of polypeptides 
            into smaller ones).</p>
            <p>Some of these enzymes cleave the large insoluble protein chains into smaller soluble protein which 
            enhance the head retention of the beer but contribute to haze formation.</p>

            <p>Other proteolytic enzyme remove amino acid from the ends of the protein chains to produce small 
            peptides and individual amino acids that the yeast can use as nutrients.In fact, the enzyme do the 
            greatest part of their job during malting.</p>

            <p>Well modified malts do not require such a rest and a long ( >30mn) protein rest at 50 &deg;C could
            be counterproductive regarding foam stability and body.</p>

            <p>This rest is used by craft brewer that want to take more control of the mashing process using
            moderately modified malts or a proportion of unmalted adjunct more than 20 %. 
           In such a case a rest of 15 30 mn at 50 &deg;C is used.
           It can also be combined with a beta-glucanase rest:  30mn at 45-50 &deg;C (113-122 &deg;F)</p>
           
            
           ''')
        self.prot_rest=Rest('Protein Rest',[4.4, 5, 6, 6.1],[27,45,55,65],TEXT_REST_PROTEIN,'no')
        
        TEXT_REST_SACH=self.tr('''
             <h2 style="color:red; font-style:italic;">This rest cannot be edited or deleted</h2>
            <h2>Saccharification </h2>

            <p>This kind of rest is the main event in the mashing process. It allows the conversion of starches
            into fermentable sugars.</p>

            <p>Before explaining what happen during this rest let's present the various kind of sugar the wort
            generally contains before fermentation.</p>
                        <ul>
                <li><strong>Glucose:</strong> 10 to 15%. It is a monosaccharide that we will note G </li>
                <li><strong>Fructose:</strong> 1 to 2%. It is a monosaccharid (isomer of G) that we will not F</li>
                <li><strong>Sucrose:</strong> 1 to 2%.It is a disaccharide consisting of one G and one F bound together</li>
                <li><strong>Maltose:</strong> 50 to 60%. It is a disaccharide consisting of 2 G</li>
                <li><strong>Maltotriose:</strong> 15 to 20%. It a trisaccharide consisting of  3 G bound together</li>
                <li><strong>Dextrins:</strong> 20 to 30%. They are larger suggars called oligosaccharides consisting
                of more than 3G. Dextrins are <strong>not fermentable</strong></li>
            </ul>
            <p>The enzymes involved in the  process of breaking down starches are called <strong>diastatic enzymes</strong>, each one having its own
            capacity in breaking down the <strong>amyloses</strong> - amyloses are single straight-chain starch molecules, typically hundreds or thousands of glucose
            units long. The can even branch to each other forming very large molecules called <strong>amylopectines</strong>.</p>

            <p>Let's review the diastatic enzymes and their temperature and ph range of effectiveness:</p>
            <ul>
                <li> <strong>Beta-amylases :</strong> 
                <ul>
                    <li>PH active 5 - 6, PH preferred 5.4 - 5.5</li>
                    <li>  Temp active 55 - 65 &deg;C / 131 - 149 &deg;,  Temp preferred 55 - 65 &deg;C / 131 - 149 &deg;F</li>
       
                </ul>
                <p>Beta-amylases enzymes remove maltose chains (2G) only from the twig extremities of amylopectines not the root
             or the middle of the branch.
            They cannot get close to the branch joints.They stop working about 3G away from the branch joints.
            They leave behind amylopectines with small 3G branches that are called beta-amylase limit dextrin</p>
            </li>
            <li> <strong>Alpha-amylases :</strong>
            <ul>
                <li>PH active 5 - 6 *** PH preferred 5.6 - 5.8</li>
                <li>  Temp active 60 - 75 &deg;C / 140 - 176 &deg;F *** Temp preferred 60 - 70 &deg;C / 140 - 158 &deg;F</li>
       
            </ul>
            <p>Alpha-amylases enzymes unlike beta-amylases can break the amylopectines anywhere. Thus they make smaller
             amylopectines that the beta-amylases can work on. Nevertheless they cannot get close to the branch joints. They stop a 1G 
            away from the branch joints letting behind alpha-amylases limit dextrin </p>

             </li>
             <li><strong>Limit dextrinases :</strong>
             <ul>
                 <li>PH active 4.5 - 5.8 *** PH preferred 4.8 - 5.4</li>
                 <li>  Temp active 60 - 67 &deg;C / 140 - 153 &deg;F *** Temp preferred 60 - 65 &deg;C / 140 - 149 &deg;F</li>
       
            </ul>
             <p>Limit-dextrinase enzymes can cut up the limit-dextrin into smaller chains letting behind unbranched chains that 
              can be used by alpha and beta-amylases to produce more glucose, maltose and maltotriose.  </p>
            </li>
            </ul>

            <p>Practically :
            <ul>
                <li>Temperatures 62 - 65 &deg;C / 144 - 149 &deg;F favor beta-amylases and are still in the optimal range of 
                limit dextrinases leading to beer with a <strong>light body</strong>.</li>
                <li>Temperature 68- 72 &deg;C / 154 - 162 &deg;F favor alpha-amylases but are no longer in the active range of 
                limit-dextrinases leading to a beer with a <strong>heavy body and less attenuated</strong>.</li>
                            <li>Temperature in between produces a range of body and fermentability.</li>
            </ul>

            <p>Regarding the duration of this rest, it can vary between 30 and 60 mn depending of factors such as
             mash ph (see optimal values for each category of enzymes), water to grain ratio and temperature.
                  To guaranty a high level of fermentability <strong>60 mn </strong> is the recommended duration.
        ''')
        print(TEXT_REST_SACH)
        self.sach_rest_LB=Rest('Saccharification Rest Light Body',[5, 5.2, 5.6, 6],[55,62,65,75],TEXT_REST_SACH,'no') 
        self.sach_rest_HB=Rest('Saccharification Rest Heavy Body',[5, 5.2, 5.6, 6],[55,68,72,75],TEXT_REST_SACH,'no') 
        
    def create_rest(self):
        self.set_rw()
        self.clear_edits()
        self.add_button.show() 
        self.cancel_button.show()
        self.new_button.hide()
        self.delete_button.hide()
        self.edit_button.hide()
        
    def delete_rest(self):
        name=str(self.name_combo.currentText())
        r=self.model.get_rest(name)
        if r.removable=='no':
            self.util.alerte(self.tr('You cannot delete this basic rest'))
            return
        
        self.current_rest=None
        self.model.remove_rest(name)
        
    
          
    def edit_rest(self):   
        name=str(self.name_combo.currentText())
        r=self.model.get_rest(name)
        if r.removable=='no':
            self.util.alerte(self.tr('You cannot edit this kind of basic rest'))
            return
        self.update_button.show() 
        self.cancel_button.show()
        self.edit_button.hide()
        self.delete_button.hide()
        self.new_button.hide()
        self.set_rw()
       
    def ensure_unremovable_rests(self):
        
        self.create_unremovable_rests()
        self.model.remove_rest('Beta-glucanase Rest')
        if not('Beta-glucanase Rest' in self.rest_key_list):
            print('creating beta-glucanase rest')
            self.model.save_rest(self.beta_glucan_rest)
        self.model.remove_rest('Protein Rest')    
        if not ('Protein Rest' in self.rest_key_list):
            print('creating protein rest')
            self.model.save_rest(self.prot_rest)
        self.model.remove_rest('Saccharification Rest Light Body')    
        if not('Saccharification Rest Light Body' in self.rest_key_list):
            self.model.save_rest(self.sach_rest_LB)   
        self.model.remove_rest('Saccharification Rest Heavy Body')    
        if not('Saccharification Rest Heavy Body' in self.rest_key_list):
            self.model.save_rest(self.sach_rest_HB)        
            
           
        
    def name_combo_current_item_changed(self):
        unit=self.model.get_unit('temperature')
        if unit:
            unit_label=self.util.get_unit_label(unit)
        name=str(self.name_combo.currentText())
        if name:
            rest=self.model.get_rest(name)
            self.name_edit.setText(rest.name)
               
            for i in range(self.ph_layout.count()):
                item=self.ph_layout.itemAt(i)
                if item:
                    item.widget().setText(str(rest.phs[i]))
            for i in range(self.temperature_layout.count()):
                item=self.temperature_layout.itemAt(i)
                if item:
                    item.widget().setText(str(self.util.convert_to(unit,rest.temperatures[i]))  )   
                    self.temp_unit_label.setText(unit_label)
            self.usage_guidance_edit.setHtml(rest.guidance) 
            if rest.removable=='no':
                self.usage_guidance_edit.setStyleSheet('color:green')
            else: 
                self.usage_guidance_edit.setStyleSheet('color:blue')
                self.edit_button.show()  
                self.delete_button.show()         
       
        
        
        
            
        
    def read_input(self):
        unit=self.model.get_unit('temperature')
        name=self.util.check_input(self.name_edit,True,self.tr('Name'),False)
        if not name: 
            return
        phs=[]
        for i in range(self.ph_layout.count()):
            item=self.ph_layout.itemAt(i)
            if item:
                ph=self.util.check_input(item.widget(),False,self.tr('PH value ' + str(i)), False,0,14)
                if not ph: 
                    return
                else:
                    phs.append(ph)                          
        temperatures=[]
        for i in range(self.temperature_layout.count()):
            item=self.temperature_layout.itemAt(i)
            if item:
                t=self.util.check_input(item.widget(),False,self.tr('Temperature value ' + str(i)), False,0,80,None,unit)
                if not t :return
                else: temperatures.append(t)                     
        guidance=self.usage_guidance_edit.toPlainText()                        
        return Rest(name,phs,temperatures,guidance)    
    
    
    def refresh_rest_list_combo(self):
        self.name_combo.clear()
        self.name_combo.addItem('')
        for r in self.rest_key_list:
            self.name_combo.addItem(r)
        
        
        if self.current_rest:
            index = self.name_combo.findData(self.current_rest)
            self.name_combo.setCurrentIndex(index) 
        else:
            index = self.name_combo.findData('')
            self.name_combo.setCurrentIndex(index)    
             
     
    def on_model_changed_rest_create(self,target):
        '''
        This function is called by the model when it changes
        due to the fact that it is subscribed as callback
        on initialization
        '''
        if target == 'rest':
            self.rest_key_list=self.model.rest_list 
            self.refresh_rest_list_combo()
            self.clear_edits()   
            
        'we must wait for fonts to be initialized in model'    
        if target == 'fontset':
            if (self.model.in_use_fonts):
                self.set_fonts()         
        
    def save_rest(self):
        'save or update the rest that is defined by the GUI'
        rest=self.read_input()
        self.current_rest=rest.name # in order to be able to select it back on refresh    
        self.model.save_rest(rest)
        self.set_ro()
        self.add_button.hide()
        
        
    def init_dialog_and_connections(self):
        self.add_button.clicked.connect(self.save_rest)
        self.edit_button.clicked.connect(self.edit_rest)
        self.cancel_button.clicked.connect(self.cancel)
        self.update_button.clicked.connect(self.update_rest)
        self.new_button.clicked.connect(self.create_rest)
        self.delete_button.clicked.connect(self.delete_rest)
        self.name_combo.currentIndexChanged.connect(self.name_combo_current_item_changed)
        #self.close_button.clicked.connect(self.close)  
     
     
    def set_fonts(self):
        pf=platform.system()
        self.add_button.setStyleSheet('background-color:lightgreen;')
        self.update_button.setStyleSheet('background-color:lightgreen;')
        self.cancel_button.setStyleSheet('background-color:pink:ont-family')
        self.add_button.setFont(self.model.in_use_fonts['button'])
        self.update_button.setFont(self.model.in_use_fonts['button'])
        self.cancel_button.setFont(self.model.in_use_fonts['button'])
        self.edit_button.setFont(self.model.in_use_fonts['button'])
        self.delete_button.setFont(self.model.in_use_fonts['button'])
        self.new_button.setFont(self.model.in_use_fonts['button'])
        self.main_label.setFont(self.model.in_use_fonts['title'])
        self.choose_label.setFont(self.model.in_use_fonts['title_slanted'])
        self.name_label.setFont(self.model.in_use_fonts['field'])
        self.ph_range_label.setFont(self.model.in_use_fonts['field'])
        self.temperature_label.setFont(self.model.in_use_fonts['field'])
        self.name_edit.setFont(self.model.in_use_fonts['field'])
        self.name_combo.setFont(self.model.in_use_fonts['field'])
        self.ph_max.setFont(self.model.in_use_fonts['field'])
        self.ph_min.setFont(self.model.in_use_fonts['field']) 
        self.optimal_ph_max.setFont(self.model.in_use_fonts['field'])
        self.optimal_ph_min.setFont(self.model.in_use_fonts['field'])
        self.temperature_max.setFont(self.model.in_use_fonts['field'])
        self.temperature_min.setFont(self.model.in_use_fonts['field'])
        self.optimal_temperature_max.setFont(self.model.in_use_fonts['field'])
        self.optimal_temperature_min.setFont(self.model.in_use_fonts['field']) 
        self.temp_unit_label.setFont(self.model.in_use_fonts['field'])   
        self.usage_guidance_edit.setFont(self.model.in_use_fonts['field'])       
            
            
        
           
    def set_ro(self):
        #self.name_combo.setEnabled(False)
        self.name_edit.setReadOnly(True)
        self.name_edit.setStyleSheet(sty.field_styles['read_only'])
        for i in range (self.ph_layout.count()):
            item=self.ph_layout.itemAt(i)
            if item:
                item.widget().setReadOnly(True)
                item.widget().setStyleSheet(sty.field_styles['read_only'])
                
        for i in range (self.temperature_layout.count()):
            item=self.temperature_layout.itemAt(i)
            if item:
                item.widget().setReadOnly(True)
                item.widget().setStyleSheet(sty.field_styles['read_only'])  
                
        self.usage_guidance_edit.setReadOnly(True)
        self.usage_guidance_edit.setStyleSheet(sty.field_styles['read_only'])    
        
    def set_rw(self):
        
        self.name_combo.setEnabled(True)
        self.name_edit.setReadOnly(False)
        self.name_edit.setStyleSheet(sty.field_styles['editable'])
        for i in range (self.ph_layout.count()):
            item=self.ph_layout.itemAt(i)
            if item:
                item.widget().setReadOnly(False)
                item.widget().setStyleSheet(sty.field_styles['editable'])
                
        for i in range (self.temperature_layout.count()):
            item=self.temperature_layout.itemAt(i)
            if item:
                item.widget().setReadOnly(False)
                item.widget().setStyleSheet(sty.field_styles['editable'])  
                
        self.usage_guidance_edit.setReadOnly(False)
        self.usage_guidance_edit.setStyleSheet(sty.field_styles['editable'])  
        
    
        
    def showEvent(self,e): 
        #self.ensure_unremovable_rests()  
        self.set_fonts()   
        
    def update_rest(self):
        'update the rest that is defined by the GUI'
        rest=self.read_input()
        self.current_rest=rest.name # in order to be able to select it back on refresh    
        self.model.update_rest(rest)
        self.set_ro()
        #self.set_read_only_style()
        self.update_button.hide()  
        self.cancel_button.hide()
                          
                
                    
     