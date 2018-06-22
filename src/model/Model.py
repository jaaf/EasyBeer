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
import sqlite3 as lite
import pickle
from sqlite3 import Error
from model.Malt import Malt
from model.Hop import Hop
from model.Yeast import Yeast
from model.Rest import Rest
from model.Recipe import Recipe
from model.Equipment import Equipment



import shelve, inspect
from pycparser.c_ast import Switch
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
        print('the path in development is'+self.database_path+', which is the src directory')
      
        'below are the lists of function that are subscribed by widgets as callbacks whenever the model changes'
        self._update_funcs_malt = []
        self._update_funcs_hop = []
        self._update_funcs_rest = []
        self._update_funcs_yeast=[]  
        self._update_funcs_recipe=[]
        self._update_funcs_equipment=[]
        self._update_funcs_style=[]
        
        'read the keys in all the databases'
        self.update_from_db('malt')
        self.update_from_db('hop')
        self.update_from_db('yeast')
        self.update_from_db('rest')
        self.update_from_db('recipe')
        self.update_from_db('equipment')
        self.update_from_db('session')
        self.update_from_db('style')
        
        'containers for callback functions'
        self._target_func={
            'malt': [],
            'hop': [],
            'rest':[],
            'yeast':[],
            'recipe':[],
            'equipment':[],
            'style':[] 
            }
        
    def post_init(self):
        self.update_from_db('malt')
        self.update_from_db('hop')
        self.update_from_db('yeast')
        self.update_from_db('rest')
        self.update_from_db('recipe')
        self.update_from_db('equipment')
        self.update_from_db('session')
        self.update_from_db('style')    

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
        rest=Rest(r[0],pickle.loads(r[1]),pickle.loads(r[2]),r[3])     
        return rest
    
    def get_yeast(self,key):
        'return a yeast given its name'   
        con=lite.connect('easybeer.db')
        c = con.cursor()  
        c.execute("""select * from yeasts where name=:name""",{'name':key})
        y=c.fetchone()
        yeast=Yeast(y[0],y[1],y[2],y[3],y[4],y[5],y[6],y[7],y[8])     
        return yeast
    
    def get_recipe(self,key):
        'return a recipe given its name'
        con=lite.connect('easybeer')
        c = con.cursor()
        c.execute("""select * from recipe where name=:name""",{'name':key})
        rcp=c.fetchone()
        recipe=Recipe(rcp[0],pickle.loads(rcp[1]),pickle.loads(rcp[2]),pickle.loads(rcp[3]),rcp[4],rcp[5],rcp[6],pickle.loads(rcp[7]),rcp[8])
        return recipe
        
           
    def get_equipment(self,key):
        'return an equipment by key'
        self.equipment_base=shelve.open(os.path.join(self.database_path,'equipment.db'))#(mcst.EQUIPMENT_DB)
        equipment=self.equipment_base[key]
        self.equipment_base.close()
        return equipment
    
    def get_session(self,key):
        'return a session by key'
        self.session_base=shelve.open(os.path.join(self.database_path,'session.db'))#(mcst.SESSION_DB)
        session=self.session_base[key]
        self.session_base.close()
        return session
    
    def get_styles(self,category):
        self.style_base=shelve.open(os.path.join(self.database_path,'style.db'))#(mcst.STYLE_DB)
        styles=self.style_base[category]
        self.style_base.close()
        return styles
    
    
        
    def save_malt(self,malt):
        print('saving malt with sqlite')
        con = lite.connect('easybeer.db')
        c = con.cursor()
        try:
            'malts table already exists as created in self.update_from_db'
            c.execute("insert into malts values (:name,:maker,:max_yield,:color,:kolbach_min, :kolbach_max)",
                  {'name':malt.name, 'maker':malt.maker, 'max_yield':malt.max_yield, 'color':malt.color, 'kolbach_min':malt.kolbach_min,'kolbach_max':malt.kolbach_max})
            con.commit()
            c.execute("select * from malts")    
        except Error as e :
            print(e)   
        c.close()
        con.close()
        self.update_from_db('malt') #reread the actual key state of db
        self.announce_model_changed('malt')

    def save_hop(self,hop):
        print('saving hop with sqlite')
        con = lite.connect('easybeer.db')
        c = con.cursor()
        try:
            'hops table already exists as created in self.update_from_db'
            c.execute("insert into hops values (:name,:alpha_acid,:form)",
                  {'name':hop.name, 'alpha_acid':hop.alpha_acid, 'form':hop.form})
            con.commit()
            c.execute("select * from hops")    
        except Error as e :
            print(e)   
        c.close()
        con.close()
        self.update_from_db('hop') #reread the actual key state of db
        self.announce_model_changed('hop')        
  

        
    def save_rest(self,rest):
        print('saving rest with sqlite')
        con = lite.connect('easybeer.db')
        c = con.cursor()
        try:
            'rests table already exists as created in self.update_from_db'
            c.execute("insert into rests values (:name,:phs,:temperatures,:guidance)",
                  {'name':rest.name, 'phs':pickle.dumps(rest.phs), 'temperatures':pickle.dumps(rest.temperatures),'guidance':rest.guidance})
            con.commit()
            c.execute("select * from hops")    
        except Error as e :
            print(e)   
        c.close()
        con.close()
        self.update_from_db('rest')
        self.announce_model_changed('rest')
        
    def save_yeast(self,yeast):
        print('saving yeast with sqlite')
        con = lite.connect('easybeer.db')
        c = con.cursor()
        try:
            'yeast table already exists as created in self.update_from_db'
            c.execute("insert into yeasts values (:name,:maker,:max_allowed_temperature,:min_allowed_temperature,:max_advised_temperature, :min_allowed_temperature, :form, :attenuation, :floculation)",
                  {'name':yeast.name, 'maker':yeast.maker, 'max_allowed_temperature':yeast.max_allowed_temperature, 'min_allowed_temperature':yeast.min_allowed_temperature,
                    'max_advised_temperature':yeast.max_advised_temperature,'min_advised_temperature':yeast.max_advised_temperature, 'form':yeast.form, 'attenuation':yeast.attenuation, 'floculation':yeast.floculation})
            con.commit()
            c.execute("select * from yeasts")    
        except Error as e :
            print(e)   
        c.close()
        con.close()
        self.update_from_db('yeast') #reread the actual key state of db
        self.announce_model_changed('yeast')
        
    def add_recipe(self,recipe):
        con = lite.connect('easybeer.db')
        c = con.cursor()
        try:
            'recipes table already exists as created in self.update_from_db'
            c.execute("insert into recipes values (:name,:malts_in_mash,:mash_rests,:hops_in_recipe,:targeted_original_gravity,:targeted_bitterness,:boiling_time,:yeasts_in_recipe,:fermentation_explanation)",
                  {'name':recipe.name, 'malts_in_mash':pickle.dumps(recipe.malts_in_mash), 'mash_rests':pickle.dumps(recipe.mash_rests),'hops_in_recipe':recipe.hops_in_recipe,
                   'targeted_original_gravity':recipe.targeted_original_gravity,'targeted_bitterness':recipe.targeted_bitterness,'boiling_time':recipe.boiling_time,'yeast_in_recipe':recipe.yeast_in_recipe,
                   'fermentation_explanation':recipe.fermentation_explanation})
            con.commit()
            c.execute("select * from recipes")    
        except Error as e :
            print(e)   
        c.close()
        con.close()
        self.update_from_db('rest')
        self.announce_model_changed('rest')
        
    def add_equipment(self,equipment):
        'add an equipment persisting it to the db' 
        self.equipment_base=shelve.open(os.path.join(self.database_path,'equipment.db'))#(mcst.EQUIPMENT_DB)
        self.equipment_base[equipment.name]=equipment
        self.equipment_base.close()
        self.update_from_db('equipment')
        self.announce_model_changed('equipment') 
        
    def save_session(self,session):
        'save or update a session'
        self.session_base=shelve.open(os.path.join(self.database_path,'session.db'))#(mcst.SESSION_DB)
        self.session_base[session.designation]=session
        self.session_base.close()
        self.update_from_db('session')
        
    def save_style(self,category, value):
        print('save or update a style')
        self.style_base=shelve.open(os.path.join(self.database_path,'style.db'))#(mcst.STYLE_DB)
        self.style_base[category]=value
        self.style_base.close()
        self.update_from_db('style')  
        self.announce_model_changed('style')      
            
        
    def is_used(self,malt_name):
        recipe_base=shelve.open(os.path.join(self.database_path,'recipe.db'))#(mcst.RECIPE_DB)
        for key in recipe_base:
            recipe=recipe_base[key]
            for maltT in recipe.malts_in_mash:
                if maltT.malt ==malt_name:
                    return True
        return False        
               
        recipe_base.close()
        

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
        
    def remove_session(self,key):
        'remove a brewing session from db' 
        self.session_base=shelve.open(os.path.join(self.database_path,'session.db'))#(mcst.SESSION_DB)   
        del self.session_base[key]
        self.session_base.close()
        self.update_from_db('session')
        
        
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
        
    def remove_equipment(self,key):
        'remove an equipment from db given its key' 
        self.equipment_base=shelve.open(os.path.join(self.database_path,'equipment.db'))#(mcst.EQUIPMENT_DB)
        del self.equipment_base[key]
        self.equipment_base.close()
        self.update_from_db('equipment')
        self.announce_model_changed('equipment')    
        
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
        
        
    def update_from_db(self,target):
        'in model update from db'
        def f_malt():
            print('getting malt list from db')
            c.execute("""select name from malts""")
            r=list(c.fetchall())
            self.__malt_list=list()  
            for m in r:
                self.__malt_list.append(m[0])   
            self.__malt_list.sort()
            
        def f_hop():
            print('getting hop list from db')
            c.execute("""select name from hops""")
            r=list(c.fetchall())
            self.__hop_list=list()  
            for h in r:
                self.__hop_list.append(h[0])   
            self.__hop_list.sort()    
            
            
        def f_rest():
            print('getting rest list from db')
            c.execute("""select name from rests""")
            r=list(c.fetchall())
            self.__rest_list=list()  
            for re in r:
                self.__rest_list.append(re[0])   
            self.__rest_list.sort()  
            
            
        def f_yeast():
            print('getting yeast list from db')
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
                self.__rest_list.append(rec[0])   
            self.__recipe_list.sort()  
        
        def f_equipment():
            self.equipment_base=shelve.open(os.path.join(self.database_path,'equipment.db'))#(mcst.EQUIPMENT_DB)
            self.__equipment_list=list(self.equipment_base.keys())
            self.equipment_list.sort()
            self.equipment_base.close() 
        
        def f_session():
            self.session_base=shelve.open(os.path.join(self.database_path,'session.db'))#(mcst.SESSION_DB)
            self.__session_list = list(self.session_base.keys())
            self.session_list.sort()
            self.session_base.close()   
        
        def f_style():
            self.style_base=shelve.open(os.path.join(self.database_path,'style.db'))#(mcst.STYLE_DB)
            self.__style_list=list(self.style_base.keys())
            self.style_base.close()  
              
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

            sql = """create table if not exists rests (name text primary key not null,phs text,temperatures text, guidance text)"""
            c.execute(sql)      
            
            sql = """create table if not exists recipes (name text primary key not null,malts_in_mash text, mash_rests text, hops_in_recipe text,targeted_original_gravity real,targeted_bitterness real, boiling_time real,
            yeast_in_recipe text)"""
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
            'style': f_style
            }
        switch_options[target]()
        