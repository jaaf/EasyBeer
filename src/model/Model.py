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
        
        #containers for callback functions
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
        'return a malt given a key'
        self.malt_base=shelve.open(os.path.join(self.database_path,'malt.db'))#(mcst.MALT_DB)
        malt=self.malt_base[key]
        self.malt_base.close()
        return malt
    
    def get_hop(self,key):
        'return a hop given a key'
        self.hop_base=shelve.open(os.path.join(self.database_path,'hop.db'))#(mcst.HOP_DB)
        hop=self.hop_base[key]
        self.hop_base.close()
        return hop
    
    def get_rest(self,key):
        'return a rest given a key'
        self.rest_base=shelve.open(os.path.join(self.database_path,'rest.db'))#(mcst.REST_DB)
        rest=self.rest_base[key]
        self.rest_base.close()
        return rest
    
    def get_yeast(self,key):
        'return a yeast given a key'
        self.yeast_base=shelve.open(os.path.join(self.database_path,'yeast.db'))#(mcst.YEAST_DB)
        yeast=self.yeast_base[key]
        self.yeast_base.close()
        return yeast
    
    def get_recipe(self,key):
        'return a recipe by key'
        self.recipe_base=shelve.open(os.path.join(self.database_path,'recipe.db'))#(mcst.RECIPE_DB)
        recipe=self.recipe_base[key]
        self.recipe_base.close()
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
        'add a malt persisting it to the db'
        print('writing in malt.db')
        self.malt_base=shelve.open(os.path.join(self.database_path,'malt.db'))#(mcst.MALT_DB)
        self.malt_base[malt.name]=malt
        self.malt_base.close()
        self.update_from_db('malt') #reread the actual key state of db
        self.announce_model_changed('malt')
        
    def add_hop_view(self,hop):
        'add a hop persisting it to the db'
        self.hop_base=shelve.open(os.path.join(self.database_path,'hop.db'))#(mcst.HOP_DB)
        self.hop_base[str(hop.name)]=hop
        self.hop_base.close()
        self.update_from_db('hop') #reread the actual key state of db
        self.announce_model_changed('hop')
        
    def save_rest(self,rest):
        'add or update a rest in the db'
        self.rest_base=shelve.open(os.path.join(self.database_path,'rest.db'))#(mcst.REST_DB)
        self.rest_base[str(rest.name)]=rest
        self.rest_base.close()
        self.update_from_db('rest')
        self.announce_model_changed('rest')
        
    def save_yeast(self,yeast):
        'add a yeast persisting it to the db'
        self.yeast_base=shelve.open(os.path.join(self.database_path,'yeast.db'))#(mcst.YEAST_DB)
        self.yeast_base[str(yeast.name)]=yeast
        self.yeast_base.close()
        self.update_from_db('yeast') #reread the actual key state of db  
        self.announce_model_changed('yeast') 
        
    def add_recipe(self,recipe):
        'add a recipe persisting it to the db' 
        self.recipe_base=shelve.open(os.path.join(self.database_path,'recipe.db'))#(mcst.RECIPE_DB)
        self.recipe_base[recipe.name]=recipe
        self.recipe_base.close()
        self.update_from_db('recipe')
        self.announce_model_changed('recipe') 
        
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
        'remove a malt from db'
        self.malt_base=shelve.open(os.path.join(self.database_path,'malt.db'))#(mcst.MALT_DB)
        del self.malt_base[key]
        self.malt_base.close()
        self.update_from_db('malt')
        self.announce_model_changed('malt')  
        
    def remove_hop(self,key):
        'remove a hop from db'
        self.hop_base=shelve.open(os.path.join(self.database_path,'hop.db'))#(mcst.HOP_DB)
        del self.hop_base[key]
        self.hop_base.close()
        self.update_from_db('hop')
        self.announce_model_changed('hop')
        
    def remove_session(self,key):
        'remove a brewing session from db' 
        self.session_base=shelve.open(os.path.join(self.database_path,'session.db'))#(mcst.SESSION_DB)   
        del self.session_base[key]
        self.session_base.close()
        self.update_from_db('session')
        
        
    def remove_yeast(self,key):
        'remove a yeast from db'
        self.yeast_base=shelve.open(os.path.join(self.database_path,'yeast.db'))#(mcst.YEAST_DB)
        del self.yeast_base[key]
        self.yeast_base.close()
        self.update_from_db('yeast')
        self.announce_model_changed('yeast')    
        
    def remove_recipe(self,key):
        'remove a recipe from db given its key' 
        self.recipe_base=shelve.open(os.path.join(self.database_path,'recipe.db'))#(mcst.RECIPE_DB)
        del self.recipe_base[key]
        self.recipe_base.close()
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
        self.rest_base=shelve.open(os.path.join(self.database_path,'rest.db'))#(mcst.REST_DB)
        del self.rest_base[key]
        self.rest_base.close()
        self.update_from_db('rest')
        self.announce_model_changed('rest')    
        
        
    def update_from_db(self,target):
        'in model update from db'
        def f_malt():
            print('readinq in /malt.db')
            self.malt_base=shelve.open(os.path.join(self.database_path,'malt.db'))#('malt.db')#(mcst.MALT_DB)
            self.__malt_list=list(self.malt_base.keys())
            self.__malt_list.sort()
            self.malt_base.close() 
            
        def f_hop():
            self.hop_base=shelve.open(os.path.join(self.database_path,'hop.db'))#('hop.db')#(mcst.HOP_DB)
            self.__hop_list=list(self.hop_base.keys())
            self.__hop_list.sort()
            self.hop_base.close()
            
        def f_rest():
            self.rest_base=shelve.open(os.path.join(self.database_path,'rest.db'))#(mcst.REST_DB)
            self.__rest_list=list(self.rest_base.keys())
            self.__rest_list.sort()
            self.rest_base.close()
            
        def f_yeast():
            self.yeast_base=shelve.open(os.path.join(self.database_path,'yeast.db'))#(mcst.YEAST_DB)
            self.__yeast_list=list(self.yeast_base.keys())
            self.__yeast_list.sort()
            self.yeast_base.close() 
                    
        def f_recipe():
            self.recipe_base=shelve.open(os.path.join(self.database_path,'recipe.db'))#(mcst.RECIPE_DB)
            self.__recipe_list=list(self.recipe_base.keys())
            self.recipe_list.sort()
            self.recipe_base.close()
        
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
        