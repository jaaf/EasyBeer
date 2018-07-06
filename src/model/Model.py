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

import model.constants as mcst
import os
import inspect
import sqlite3 as lite
import pickle
from sqlite3 import Error
from model.Malt import Malt
from model.Hop import Hop
from model.Yeast import Yeast
from model.Rest import Rest
from model.Recipe import Recipe
from model.Equipment import Equipment
from model.Session import Session
from model.FontSet import FontSet
from model.Unit import Unit
import view.constants as vcst



import shelve, inspect
from pycparser.c_ast import Switch
from pip._vendor.requests.sessions import session
from cgitb import small
import platform

#from builtins import property



class Model(object):
    '''
    This class is the model. It keeps a state of the data in the form
    of lists (malt,recipe, equipment,...)
    '''

    def __init__(self,bundle_dir=None):
        '''
        Constructor
        '''
        'bundle_dir is available only in the frozen bundled environment'
        self.bundle_dir=bundle_dir
        if self.bundle_dir:
            self.database_path=self.bundle_dir
        else: self.database_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..' ) 
      
        'below are the lists of function that are subscribed by widgets as callbacks whenever the model changes'
        self._update_funcs_malt = []
        self._update_funcs_hop = []
        self._update_funcs_rest = []
        self._update_funcs_yeast=[]  
        self._update_funcs_recipe=[]
        self._update_funcs_equipment=[]
        self._update_funcs_style=[]
        self._update_funcs_fontset=[]
        self.update_funcs_unit=[]
        
        'read the keys in all the databases'
        self.update_from_db('malt')
        self.update_from_db('hop')
        self.update_from_db('yeast')
        self.update_from_db('rest')
        self.update_from_db('recipe')
        self.update_from_db('equipment')
        self.update_from_db('session')
        self.update_from_db('style')
        self.update_from_db('fontset')
        self.update_from_db('unit')
        
        'containers for callback functions'
        self._target_func={
            'malt': [],
            'hop': [],
            'rest':[],
            'yeast':[],
            'recipe':[],
            'equipment':[],
            'session':[],
            'style':[], 
            'fontset':[],
            'unit':[]
            }
        self.in_use_fonts=None
        
    def post_init(self):
        self.update_from_db('malt')
        self.update_from_db('hop')
        self.update_from_db('yeast')
        self.update_from_db('rest')
        self.update_from_db('recipe')
        self.update_from_db('equipment')
        self.update_from_db('session')
        self.update_from_db('style')
        self.update_from_db('fontset')   
        self.update_from_db('unit') 

    def subscribe_model_changed(self,target_list,func):
        for target in target_list:
            if func not in self._target_func[target]:
                self._target_func[target].append(func)
                
                
    def unsubscribe_model_changed(self,target, func): 
        if func in self._target_func[target]:
            self._target_func[target].remove(func)       
                
    def announce_model_changed(self,target):
        for func in self._target_func[target]:     
            func(target)
      
 
        
    @property
    def malt_list(self):
        return self.__malt_list
    
    @malt_list.setter
    def malt_list(self,l):
        self.__malt_list=l
        
        
    @property
    def hop_list(self):
        return self.__hop_list
    
    @hop_list.setter
    def hop_list(self,l):
        self.__hop_list=l
        
    @property
    def rest_list(self):
        return self.__rest_list
    
    @rest_list.setter
    def rest_list(self,l):
        self.__rest_list=l
        
            
    @property
    def yeast_list(self):
        return self.__yeast_list
    
    @yeast_list.setter
    def yeast_list(self,l):
        self.__yeast_list=l    
        
    @property
    def recipe_list(self):
        return self.__recipe_list
    
    @recipe_list.setter
    def recipe_list(self,l):
        self.__recipe_list=l 
        
    @property
    def equipment_list(self):
        return self.__equipment_list
    
    @equipment_list.setter
    def equipment_list(self,l):
        self.__equipment_list=l  
        
    @property
    def session_list(self):
        return self.__session_list
        
    @session_list.setter
    def session_list(self,l):
        self.__session_list=l    
        
        
        
    @property
    def style_list(self):
        return self.__style_list
        
    @style_list.setter
    def style_list(self,l):
        self.__style_list=l  
        
    @property
    def font_set_list(self):
        return self.__font_set_list
        
    @font_set_list.setter
    def font_set_list(self,s):
        self.__font_set_list=s    
    
    
    @property
    def unit_list(self):
        return self.__unit_list
        
    @unit_list.setter
    def unit_list(self,ul):
        self.__unit_list=ul          
        
        
    def add_equipment(self,equipment):
        eq=equipment
        con=lite.connect('easybeer.db')
        c=con.cursor()
        try:
            c.execute("insert into equipments values (?,?,?,?,?,?,?,?,?,?,?)",(eq.name,eq.brewing_efficiency,eq.boiler_size,eq.boiler_dead_space,eq.boiler_evaporation_rate,eq.fermentor_size,eq.fermentor_dead_space,eq.type,eq.mash_tun_size,eq.mash_tun_dead_space,eq.mash_tun_heat_losses))
            con.commit()
        except Error as e:
            print('There was an error while inserting new equipment')
            print(e)
        c.close()
        con.close()
        self.update_from_db('equipment')
        self.announce_model_changed('equipment')
        
            
    def add_recipe(self,recipe):
       
        con=lite.connect('easybeer.db')
        c=con.cursor()
        mim=pickle.dumps(recipe.malts_in_mash)
        hir=pickle.dumps(recipe.hops_in_recipe)
        mr=pickle.dumps(recipe.mash_rests)
        yir=pickle.dumps(recipe.yeast_in_recipe)
        try:
            'recipes table already exists as created in self.update_from_db'
            
            c.execute("insert into recipes values (\
            :name,\
            :malts_in_mash,\
            :mash_rests,\
            :hops_in_recipe,\
            :targeted_original_gravity,\
            :targeted_bitterness,\
            :boiling_time,\
            :yeast_in_recipe,\
            :fermentation_explanation)",
            {'name':recipe.name, 
             'malts_in_mash':mim,
             'mash_rests':mr,
             'hops_in_recipe':hir,
             'targeted_original_gravity':recipe.targeted_original_gravity,
             'targeted_bitterness':recipe.targeted_bitterness,
             'boiling_time':recipe.boiling_time,
             'yeast_in_recipe':yir,
             'fermentation_explanation':recipe.fermentation_explanation
            })
            
            con.commit()   
        except Error as e :
            print('there is an error during insertion of a new recipe')
            print(e)   
        c.close()
        con.close()
        self.update_from_db('recipe')
        self.announce_model_changed('recipe')
    
    def change_active_font_set(self, category):
        con=lite.connect('easybeer.db')
        c=con.cursor()
        c.execute("""select * from fontsets where status=:status""",{'status':'active'})
        l=c.fetchall()
        for f in l: self.update_font_set(FontSet(f[0],'inactive'))
        self.update_font_set(FontSet(category,'active'))
        c.close()
        con.close()
        
        
    def drop_units(self):
        con=lite.connect('easybeer.db')
        c=con.cursor()
        c.execute('drop table if exists units')
        c.close()
        con.close()    
            
    def get_malt(self,key):
        'return a malt given its name'   
        con=lite.connect('easybeer.db')
        c = con.cursor()  
        c.execute("""select * from malts where name=:name""",{'name':key})
        m=c.fetchone()
        malt=Malt(m[0],m[1],m[2],m[3],m[4],m[5])     
        return malt
    
    def get_hop(self,key):
        'return a hop given its name'   
        con=lite.connect('easybeer.db')
        c = con.cursor()  
        c.execute("""select * from hops where name=:name""",{'name':key})
        h=c.fetchone()
        hop=Hop(h[0],h[1],h[2])     
        return hop
    

    
    def get_rest(self,key):
        'return a rest given a key'
        con=lite.connect('easybeer.db')
        c = con.cursor()  
        c.execute("""select * from rests where name=:name""",{'name':key})
        r=c.fetchone()
        rest=Rest(r[0],pickle.loads(r[1]),pickle.loads(r[2]),r[3],r[4])     
        return rest
    
    
    
    def get_recipe(self,key):
        recipe=None
        con=lite.connect('easybeer.db')
        c = con.cursor()
        c.execute("""select * from recipes where name=:name""",{'name':key})
        rcp=c.fetchone()
        recipe=Recipe(rcp[0],pickle.loads(rcp[1]),pickle.loads(rcp[2]),pickle.loads(rcp[3]),rcp[4],rcp[5],rcp[6],pickle.loads(rcp[7]),rcp[8])
        return recipe
        
           
    def get_equipment(self,key):
        'return an equipment given its name'
        con=lite.connect('easybeer.db')
        c=con.cursor()
        c.execute("""select * from equipments where name=:name""",{'name':key})
        eq=c.fetchone()
        equipment=Equipment(eq[0],eq[1],eq[2],eq[3],eq[4],eq[5],eq[6],eq[7],eq[8],eq[9],eq[10])
        return equipment
    
    def get_session(self,key):
        'return a session given its designation'
        con=lite.connect('easybeer.db')
        c=con.cursor()
        c.execute("""select * from sessions where designation=:designation""",{'designation':key})
        s=c.fetchone()
        mis=pickle.loads(s[9])#malts_in_session'
        ris=pickle.loads(s[10])#rests in session
        his=pickle.loads(s[11])#hops in session
        yis=pickle.loads(s[12])#yeast in session
        session=Session(s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7],s[8],mis,ris,his,yis,s[13],s[14],s[15],s[16],s[17],s[18],s[19],s[20],s[21])
        return session
        
    
    def get_style(self,category):
        'return a style given its category'
        con=lite.connect('easybeer.db')
        c=con.cursor()
        c.execute("""select * from styles where category=:category""",{'category':category})
        s=c.fetchone()
        'this is a specific case where the object returned excludes the key'
        if s: style=pickle.loads(s[1])
        else:  style=None
        c.close()
        con.close()
        return style
        '''
        self.style_base=shelve.open(os.path.join(self.database_path,'style.db'))#(mcst.STYLE_DB)
        styles=self.style_base[category]
        self.style_base.close()
        return styles
        '''
    def get_active_font_set(self):
        'return a fontset given its category'
        con=lite.connect('easybeer.db')
        c=con.cursor()
        c.execute("""select * from fontsets where status=:status""",{'status':'active'})
        fs=c.fetchone()
        if fs: 
            return FontSet(fs[0],fs[1])
        else: return None
        
    def get_unit(self, name):
        con=lite.connect('easybeer.db')
        c=con.cursor()
        c.execute("""select * from units where name=:name""", {'name':name})
        u=c.fetchone()
        c.close()
        con.close()
        if u: return Unit(u[0],u[1])    
        else: return None
        
    def get_yeast(self,key):
        'return a yeast given its name'   
        con=lite.connect('easybeer.db')
        c = con.cursor()  
        c.execute("""select * from yeasts where name=:name""",{'name':key})
        y=c.fetchone()
        yeast=Yeast(y[0],y[1],y[2],y[3],y[4],y[5],y[6],y[7],y[8])     
        return yeast    
        
    def is_used(self,malt_name):
        recipe_base=shelve.open(os.path.join(self.database_path,'recipe.db'))#(mcst.RECIPE_DB)
        for key in recipe_base:
            recipe=recipe_base[key]
            for maltT in recipe.malts_in_mash:
                if maltT.malt ==malt_name:
                    return True
        return False        
               
        recipe_base.close()
        
    def remove_equipment(self,key):
        'remove an equipment from db given its name' 
        con=lite.connect('easybeer.db')
        c = con.cursor()  
        try:
            c.execute("""delete from equipments where name=:name""",{'name':key})
            con.commit()
        except Error as e:
            print(e)    
        c.close()
        con.close()  
        self.update_from_db('equipment')
        self.announce_model_changed('equipment')     
                
    def remove_hop(self,key):
        'remove a hop from db given its name' 
        con=lite.connect('easybeer.db')
        c = con.cursor()  
        try:
            c.execute("""delete from hops where name=:name""",{'name':key})
            con.commit()
        except Error as e:
            print(e)    
        c.close()
        con.close()  
        self.update_from_db('hop')
        self.announce_model_changed('hop') 
        
    
    def remove_malt(self,key):
        'remove a malt from db given its name' 
        con=lite.connect('easybeer.db')
        c = con.cursor()  
        try:
            c.execute("""delete from malts where name=:name""",{'name':key})
            con.commit()
        except Error as e:
            print(e)    
        c.close()
        con.close()  
        self.update_from_db('malt')
        self.announce_model_changed('malt') 
        
    def remove_recipe(self,key):
        'remove a recipe from db given its key' 
        con=lite.connect('easybeer.db')
        c = con.cursor()  
        try:
            c.execute("""delete from recipes where name=:name""",{'name':key})
            con.commit()
        except Error as e:
            print(e)    
        c.close()
        con.close()  
        self.update_from_db('recipe')
        self.announce_model_changed('recipe')
        
    def remove_rest(self,key):
        'remove a rest from db given its key'
        con=lite.connect('easybeer.db')
        c = con.cursor()  
        try:
            c.execute("""delete from rests where name=:name""",{'name':key})
            con.commit()
        except Error as e:
            print(e)    
        c.close()
        con.close()
        self.update_from_db('rest')
        self.announce_model_changed('rest')    
        
    def remove_session(self,key):
        'remove a brewing session from db' 
        con=lite.connect('easybeer.db')
        c = con.cursor()  
        try:
            c.execute("""delete from sessions where designation=:designation""",{'designation':key})
            con.commit()
        except Error as e:
            print(e)    
        c.close()
        con.close()  
        self.update_from_db('session')
        self.announce_model_changed('session') 
        
        
    def remove_yeast(self,key):
        'remove a yeast from db given its name' 
        con=lite.connect('easybeer.db')
        c = con.cursor()  
        try:
            c.execute("""delete from yeasts where name=:name""",{'name':key})
            con.commit()
        except Error as e:
            print(e)    
        c.close()
        con.close()  
        self.update_from_db('yeast')
        self.announce_model_changed('yeast')  
        
     
        
    
        
    
        
    
        
    def save_font_set(self,font_set):
        con=lite.connect('easybeer.db')
        c=con.cursor()
        'fonts is a list and needs pickling'
        
        try:
            c.execute("insert into  fontsets values (:category,:fonts)",(font_set.category,font_set.status))
            con.commit()
        except Error as e:
            print('There was an error while inserting new font_set')
            print(e)
        c.close()
        con.close()
        self.update_from_db('fontset')
        self.announce_model_changed('fontset')                
        
    

    def save_hop(self,hop):
        con = lite.connect('easybeer.db')
        c = con.cursor()
        try:
            'hops table already exists as created in self.update_from_db'
            c.execute("insert into hops values (:name,:alpha_acid,:form)",
                  {'name':hop.name, 'alpha_acid':hop.alpha_acid,'form':hop.form})
            con.commit()
            c.execute("select * from hops")    
        except Error as e :
            print(e)   
        c.close()
        con.close()
        self.update_from_db('hop') #reread the actual key state of db
        self.announce_model_changed('hop')        
        
  
    def save_malt(self,malt):
        con = lite.connect('easybeer.db')
        c = con.cursor()
        try:
            'malts table already exists as created in self.update_from_db'
            c.execute("insert into malts values (:name,:maker,:max_yield,:color,:kolbach_min, :kolbach_max)",
                  {'name':malt.name, 'maker':malt.maker, 'max_yield':malt.max_yield, 'color':malt.color, 'kolbach_min':malt.kolbach_min,'kolbach_max':malt.kolbach_max})
            con.commit()
            #c.execute("select * from malts")    
        except Error as e :
            print(e)   
        c.close()
        con.close()
        self.update_from_db('malt') #reread the actual key state of db
        self.announce_model_changed('malt') 
        
    def save_rest(self,rest):
        con = lite.connect('easybeer.db')
        c = con.cursor()
        try:
            'rests table already exists as created in self.update_from_db'
            c.execute("insert into rests values (:name,:phs,:temperatures,:guidance,:removable)",
                  {'name':rest.name, 'phs':pickle.dumps(rest.phs), 'temperatures':pickle.dumps(rest.temperatures),'guidance':rest.guidance,'removable':rest.removable})
            con.commit()
            c.execute("select * from hops")    
        except Error as e :
            print(e)   
        c.close()
        con.close()
        self.update_from_db('rest')
        self.announce_model_changed('rest')
        
        
    def save_session(self,session):
        'save or update a session'
        s=session
        con=lite.connect('easybeer.db')
        c=con.cursor()
        mis=pickle.dumps(s.malts_in_session)#malts_in_session'
        ris=pickle.dumps(s.rests_in_session)#rests in session
        his=pickle.dumps(s.hops_in_session)#hops in session
        yis=pickle.dumps(s.yeast_in_session)#yeast in session
        try:
            c.execute("insert into sessions values (\
            :designation,\
            :recipe,\
            :equipment,\
            :batch_volume,\
            :grain_temperature,\
            :targeted_original_gravity,\
            :targeted_bitterness,\
            :boiling_time,\
            :brewing_efficiency,\
            :malts_in_session,\
            :rests_in_session,\
            :hops_in_session,\
            :yeast_in_session,\
            :mash_water_volume,\
            :strike_temperature,\
            :mash_sparge_water_volume,\
            :boiler_dead_space,\
            :feedback_water_treatment_text,\
            :feedback_mash_ph,\
            :feedback_preboil_volume,\
            :feedback_original_gravity,\
            :feedback_fermentor_volume)",
            (
            s.designation,
            s.recipe,
            s.equipment,
            s.batch_volume,
            s.grain_temperature,
            s.targeted_original_gravity,
            s.targeted_bitterness,
            s.boiling_time,
            s.brewing_efficiency,
            mis,
            ris,
            his,
            yis,
            s.mash_water_volume,
            s.strike_temperature,
            s.mash_sparge_water_volume,
            s.boiler_dead_space,
            s.feedback_water_treatment_text,
            s.feedback_mash_ph,
            s.feedback_preboil_volume,
            s.feedback_original_gravity,
            s.feedback_fermentor_volume
             ))
            con.commit()
        except Error as e:
            #print('There was an error while inserting new session')
            print(e)
        c.close()
        con.close()
        self.update_from_db('session')
        self.announce_model_changed('session')

        
    def save_style(self,category, value):
        con=lite.connect('easybeer.db')
        c=con.cursor()
        'value is a list and needs pickling'
        v=pickle.dumps(value)
        try:
            c.execute("insert into  styles values (:category,:cols)",(category,v))
            con.commit()
        except Error as e:
            print('There was an error while inserting new style')
            print(e)
        c.close()
        con.close()
        self.update_from_db('style')
        self.announce_model_changed('style')
        
        
        
    def save_yeast(self,yeast):
        con = lite.connect('easybeer.db')
        c = con.cursor()
        try:
            'yeasts table already exists as created in self.update_from_db'
            c.execute("insert into yeasts values (:name,:maker,:max_allowed_temperature,:min_allowed_temperature,:max_advised_temperature, :min_allowed_temperature, :form, :attenuation, :floculation)",
                 {'name':yeast.name, 'maker':yeast.maker, 'max_allowed_temperature':yeast.max_allowed_temperature, 'min_allowed_temperature':yeast.min_allowed_temperature,'max_advised_temperature':yeast.max_advised_temperature,'min_advised_temperature':yeast.max_advised_temperature, 'form':yeast.form, 'attenuation':yeast.attenuation, 'floculation':yeast.floculation})
            #c.execute("insert into yeasts values (?,?,?,?,?,?,?,?,?)",{yeast.name,yeast.maker,yeast.max_allowed_temperature,yeast.min_allowed_temperature,yeast.max_advised_temperature,yeast.min_advised_temperature,yeast.form,yeast.attenuation,yeast.floculation})
            con.commit()
            #c.execute("select * from yeasts")    
        except Error as e :
            print(e)   
        c.close()
        con.close()
        self.update_from_db('yeast') #reread the actual key state of db
        self.announce_model_changed('yeast')
        
        
    def set_in_use_fonts(self):
        font_set=self.get_active_font_set()
        pf=platform.system()
        
        if font_set:
            def f_tiny():
                if pf=='Windows':
                    self.in_use_fonts=vcst.FONT_SET_W_TINY
                elif pf=='Linux':
                    self.in_use_fonts=vcst.FONT_SET_L_TINY
                    
            def f_small():
                if pf=='Windows':
                    self.in_use_fonts=vcst.FONT_SET_W_SMALL
                elif pf=='Linux':
                    self.in_use_fonts=vcst.FONT_SET_L_SMALL

            
            def f_big():
                if pf=='Windows':
                    self.in_use_fonts=vcst.FONT_SET_W_BIG
                elif pf=='Linux':
                    self.in_use_fonts=vcst.FONT_SET_L_BIG
                
            def f_huge():
                if pf=='Windows':
                    self.in_use_fonts=vcst.FONT_SET_W_HUGE
                elif pf=='Linux':
                    self.in_use_fonts=vcst.FONT_SET_L_HUGE
                
            
            switch_options={
                'tiny':f_tiny,
                'small':f_small,
                'big': f_big,
                'huge':f_huge     
                }
            
            switch_options[font_set.category] () 
            
        elif pf=='Windows':
            self.in_use_fonts=vcst.FONT_SET_W_TINY
        elif pf=='Linux':
            self.in_use_fonts=vcst.FONT_SET_L_TINY    
        
    
        
    
        
    
        
        
    def update_equipment(self,equipment):
        eq=equipment
        con=lite.connect('easybeer.db')
        c=con.cursor()
        try:
            c.execute("update equipments set brewing_efficiency=:brewing_efficiency,boiler_size=:boiler_size,\
            boiler_dead_space=:boiler_dead_space,boiler_evaporation_rate=:boiler_evaporation_rate,\
            fermentor_size=:fermentor_size,fermentor_dead_space=:fermentor_dead_space,type=:type,\
            mash_tun_size=:mash_tun_size, mash_tun_dead_space=:mash_tun_dead_space,mash_tun_heat_losses=:mash_tun_heat_losses where \
            name=:name",
            {'name':eq.name,'brewing_efficiency':eq.brewing_efficiency,'boiler_size':eq.boiler_size,
             'boiler_dead_space':eq.boiler_dead_space,'boiler_evaporation_rate':eq.boiler_evaporation_rate,
             'fermentor_size':eq.fermentor_size,'fermentor_dead_space':eq.fermentor_dead_space,'type':eq.type,
             'mash_tun_size':eq.mash_tun_size,'mash_tun_dead_space':eq.mash_tun_dead_space,'mash_tun_heat_losses':eq.mash_tun_heat_losses})
            con.commit()
        except Error as e:
            print('There was an error while updating equipment')
            print(e)
        c.close()
        con.close()
        self.update_from_db('equipment')
        self.announce_model_changed('equipment')    
        
    def update_malt(self,malt):
        con = lite.connect('easybeer.db')
        c = con.cursor()
        try:
            'malts table already exists as created in self.update_from_db'
            c.execute("update malts set maker=:maker,max_yield=:max_yield,color=:color,kolbach_min=:kolbach_min, kolbach_max=:kolbach_max where name=:name",
                  {'name':malt.name, 'maker':malt.maker, 'max_yield':malt.max_yield, 'color':malt.color, 'kolbach_min':malt.kolbach_min,'kolbach_max':malt.kolbach_max})
            con.commit()
            #c.execute("select * from malts")    
        except Error as e :
            print('there was an error while updating the malt')
            print(e)   
        c.close()
        con.close()
        self.update_from_db('malt') #reread the actual key state of db
        self.announce_model_changed('malt')    
        
    def update_hop(self,hop):
        print('updating a hop in model')
        con = lite.connect('easybeer.db')
        c = con.cursor()
        try:
             
            'hops table already exists as created in self.update_from_db'
            c.execute("update hops set alpha_acid=:alpha_acid,form=:form",{'name':hop.name, 'alpha_acid':hop.alpha_acid, 'form':hop.form})
            con.commit()
            c.execute("select * from hops")    
        except Error as e :
            print('there was an error while updating the malt')
            print(e)   
        c.close()
        con.close()
        self.update_from_db('malt') #reread the actual key state of db
        self.announce_model_changed('malt')      
        
    def update_recipe(self,recipe): 
        con=lite.connect('easybeer.db')
        c=con.cursor()
        mim=pickle.dumps(recipe.malts_in_mash)
        hir=pickle.dumps(recipe.hops_in_recipe)
        mr=pickle.dumps(recipe.mash_rests)
        yir=pickle.dumps(recipe.yeast_in_recipe)
        try:
            'recipes table already exists as created in self.update_from_db'
            
            c.execute("update recipes set  \
            malts_in_mash=:malts_in_mash,\
            mash_rests=:mash_rests,\
            hops_in_recipe=:hops_in_recipe,\
            targeted_original_gravity=:targeted_original_gravity,\
            targeted_bitterness=:targeted_bitterness,\
            boiling_time=:boiling_time,\
            yeast_in_recipe=:yeast_in_recipe,\
            fermentation_explanation=:fermentation_explanation where name=:name",
            {'name':recipe.name,
             'malts_in_mash':mim,
             'mash_rests':mr,
             'hops_in_recipe':hir,
             'targeted_original_gravity':recipe.targeted_original_gravity,
             'targeted_bitterness':recipe.targeted_bitterness,
             'boiling_time':recipe.boiling_time,
             'yeast_in_recipe':yir,
             'fermentation_explanation':str(recipe.fermentation_explanation)
             })
            con.commit()   
        except Error as e :
            print('this is an error during updating of recipe ')
            print(e)   
        c.close()
        con.close()
        self.update_from_db('recipe')
        self.announce_model_changed('recipe')
        
    def update_rest(self, rest):
        con=lite.connect('easybeer.db')
        c=con.cursor()
        phs=pickle.dumps(rest.phs)
        tps=pickle.dumps(rest.temperatures)
        try:
            c.execute("update rests set \
             phs=:phs,\
             temperatures=:temperatures,\
              guidance=:guidance,\
              removable=:removable where name=:name",
                      {'name':rest.name,'phs':phs,'temperatures':tps,'guidance':rest.guidance,'removable':rest.removable})  
            con.commit()
        except Error as e:
            print('there was an error in updating of rest')
            print(e)
        c.close()
        con.close()
        self.update_from_db('rest')
        self.announce_model_changed('rest')   
        
    def update_yeast(self,yeast):
        con = lite.connect('easybeer.db')
        c = con.cursor()
        try:
            'yeasts table already exists as created in self.update_from_db'
            c.execute("update yeasts set maker=:maker,max_allowed_temperature=:max_allowed_temperature,min_allowed_temperature=:min_allowed_temperature,\
            max_advised_temperature=:max_advised_temperature, min_advised_temperature=:min_advised_temperature, form=:form, attenuation=:attenuation,\
            floculation= :floculation where name=:name",
                 {'name':yeast.name, 'maker':yeast.maker, 'max_allowed_temperature':yeast.max_allowed_temperature, 'min_allowed_temperature':yeast.min_allowed_temperature,'max_advised_temperature':yeast.max_advised_temperature,'min_advised_temperature':yeast.min_advised_temperature, 'form':yeast.form, 'attenuation':yeast.attenuation, 'floculation':yeast.floculation})
            con.commit()
            #c.execute("select * from yeasts")    
        except Error as e :
            print(e)   
        c.close()
        con.close()
        self.update_from_db('yeast') #reread the actual key state of db
        self.announce_model_changed('yeast')         
        
    def update_font_set(self,font_set):
        con=lite.connect('easybeer.db')
        c=con.cursor()
        try:
            c.execute("update fontsets set status = :status  where category=:category",{'category':font_set.category,'status':font_set.status})
            con.commit()
        except Error as e:
            print('There was an error while updating new size')
            print(e)
        c.close()
        con.close()
        'we must change active fonts before announcing the change to the dialogs'
        self.set_in_use_fonts()
        self.update_from_db('fontset')
        self.announce_model_changed('fontset')    
        
        
    def update_from_db(self,target):
        'in model update from db'
        def f_malt():
            c.execute("""select name from malts""")
            r=list(c.fetchall())
            self.__malt_list=list()  
            for m in r:
                self.__malt_list.append(m[0])   
            self.__malt_list.sort()
            
        def f_hop():
            c.execute("""select name from hops""")
            r=list(c.fetchall())
            self.__hop_list=list()  
            for h in r:
                self.__hop_list.append(h[0])   
            self.__hop_list.sort()    
            
            
        def f_rest():
            c.execute("""select name from rests""")
            r=list(c.fetchall())
            self.__rest_list=list()  
            for re in r:
                self.__rest_list.append(re[0])   
            self.__rest_list.sort()  
            
            
        def f_yeast():
            c.execute("""select name from yeasts""")
            r=list(c.fetchall())
            self.__yeast_list=list()  
            for y in r:
                self.__yeast_list.append(y[0])   
            self.__yeast_list.sort() 
                    
        def f_recipe():
            c.execute("""select name from recipes""")
            r=list(c.fetchall())
            self.__recipe_list=list()  
            for rec in r:
                self.__recipe_list.append(rec[0])   
            self.__recipe_list.sort()  
        
        def f_equipment():
            c.execute("""select name from equipments""")
            e=list(c.fetchall())
            self.__equipment_list=list()  
            for eq in e:
                self.__equipment_list.append(eq[0])   
            self.__equipment_list.sort() 
            
        
        def f_session():
            c.execute("""select designation from sessions""")
            ses=list(c.fetchall())
            self.__session_list=list()
            for s in ses:
                self.__session_list.append(s[0])
            self.__session_list.sort()    
           
        
        def f_style():
            c.execute("""select category from styles""")
            sts=list(c.fetchall())
            self.__style_list=list()
            for st in sts:
                self.__style_list.append(st[0])
            self.__style_list.sort()    
          
        def f_fontset():
            c.execute("""select category from fontsets""")
            fss=list(c.fetchall())
            self.__font_set_list=list()
            for fs in fss:
                self.__font_set_list.append(fs[0])
            self.__font_set_list.sort()  
            
        def f_unit():
            c.execute("""select name from units""")
            units=list(c.fetchall())
            self.__unit_list=list()
            for unit in units:
                self.__unit_list.append(unit[0])
            self.__unit_list.sort()
              
     
        con=lite.connect("easybeer.db")
        c=con.cursor()
        try:
            sql = """create table if not exists malts (name text primary key not null,maker text,max_yield real,color real,kolbach_min real,kolbach_max real)"""
            c.execute(sql)  
              
            sql = """create table if not exists hops (name text primary key not null,alpha_acid real,form text)"""
            c.execute(sql)  
            
            sql = """create table if not exists yeasts (name text primary key not null,maker text,max_allowed_temperature real,min_allowed_temperature real, 
            max_advised_temperature real,min_advised_temperature  real, form text, attenuation text, floculation text)"""
            c.execute(sql) 

            sql = """create table if not exists rests (name text primary key not null,phs text,temperatures text, guidance text,removable text)"""
            c.execute(sql)      
            
            sql = """create table if not exists recipes (name text primary key not null,malts_in_mash text, mash_rests text, hops_in_recipe text,targeted_original_gravity real,targeted_bitterness real, boiling_time real,
            yeast_in_recipe text,fermentation_explanation text)"""
            c.execute(sql)  
            
            sql = """create table if not exists equipments (name text primary key not null,brewing_efficiency real,boiler_size real, boiler_dead_space real,boiler_evaporation_rate real,fermentor_size real,fermentor_dead_space real,type integer,mash_tun_size real,mash_tun_dead_space real,mash_tun_heat_losses real)"""
            c.execute(sql)      
            
            sql = """create table if not exists sessions (\
            designation text primary key not null,\
            recipe text,\
            equipment text,\
            batch_volume real,\
            grain_temperature real,\
            targeted_original_gravity real,\
            targeted_bitterness real,\
            boiling_time real,\
            brewing_efficiency real,\
            malts_in_session text,\
            rests_in_session text,\
            hops_in_session text,\
            yeast_in_session text,\
            mash_water_volume real,\
            strike_temperature real,\
            mash_sparge_water_volume real,\
            boiler_dead_space real,\
            feedback_water_treatment_text text,\
            feedback_mash_ph real,\
            feedback_preboil_volume real,\
            feedback_original_gravity real ,\
            feedback_fermentor_volume real)"""
            c.execute(sql)
            
            sql="""create table if not exists styles (category text primary key not null, cols text) """
            c.execute(sql)
            
            sql="""create table if not exists fontsets (category text primary key not null, status text) """#fonts is pickled as it is a list
            c.execute(sql)
            
            sql="""create table if not exists units (name text primary key not null, unit text) """
            c.execute(sql)
        
            con.commit()
           
            
        except Error as e :
            print(e)  
         
        switch_options ={
            'malt': f_malt,
            'hop':  f_hop,
            'yeast':f_yeast,
            'rest': f_rest,
            'recipe': f_recipe,
            'equipment': f_equipment,
            'session': f_session,
            'style': f_style,
            'fontset':f_fontset,
            'unit':f_unit
            }
        switch_options[target]()
        
        
        
    def update_style(self,category, value):
        con=lite.connect('easybeer.db')
        c=con.cursor()
        'value is a list and needs pickling'
        v=pickle.dumps(value)
        try:
            c.execute("update styles set cols = :cols  where category=:category",{'category':category,'cols':v})
            con.commit()
        except Error as e:
            print('There was an error while updating new style')
            print(e)
        c.close()
        con.close()
        self.update_from_db('style')
        self.announce_model_changed('style')
        
        
    
        
    def update_unit(self,unit):
        con=lite.connect('easybeer.db')
        c=con.cursor()
        if self.get_unit(unit.name):
            try:
                c.execute("update units set unit=:unit where name=:name",{'name':unit.name,'unit':unit.unit})
                con.commit()
            except Error as e:
                print('there was an error while updating unit '+unit.name)
                print(e)
        else:
            try:
                c.execute("insert into units values  (:name,:unit)",(unit.name,unit.unit))  
                con.commit() 
            except Error as e:
                print('there was an error while inserting unit '+unit.name )             
            
        self.update_from_db('unit')
        self.announce_model_changed('unit')    
        