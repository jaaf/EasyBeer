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

from model.Equipment import Equipment
from model.Recipe import Recipe
#from lxml.html.builder import STRIKE
class Session(object):
    
    def __init__(self,name, timestamp,recipe, equipment, batch_volume,grain_temperature, targeted_original_gravity,
                 targeted_bitterness, boiling_time, brewing_efficiency, malts_in_session,rests_in_session,hops_in_session, 
                 yeast_in_session,mash_water_volume, strike_temperature, mash_sparge_water_volume,boiler_dead_space,
                 feedback_water_treatment_text=None,feedback_mash_ph=None, feedback_preboil_volume=None,
                 feedback_original_gravity=None,feedback_fermentor_volume=None):
        self.name = name
        self.timestamp =timestamp
        #self.session_date = session_date
        self.recipe=recipe
        self.equipment = equipment
        self.batch_volume = batch_volume
        self.grain_temperature =  grain_temperature
        self.targeted_original_gravity=targeted_original_gravity
        self.targeted_bitterness=targeted_bitterness
        self.boiling_time =boiling_time
        self.brewing_efficiency=brewing_efficiency
        self.malts_in_session=malts_in_session
        self.rests_in_session=rests_in_session
        self.hops_in_session=hops_in_session
        self.yeast_in_session=yeast_in_session
        self.mash_water_volume=mash_water_volume
        self.strike_temperature=strike_temperature
        self.mash_sparge_water_volume=mash_sparge_water_volume
        self.boiler_dead_space=boiler_dead_space
        
        self.feedback_water_treatment_text=feedback_water_treatment_text
        self.feedback_mash_ph=feedback_mash_ph
        self.feedback_preboil_volume=feedback_preboil_volume
        self.feedback_original_gravity=feedback_original_gravity
        self.feedback_fermentor_volume=feedback_fermentor_volume
        
        
        