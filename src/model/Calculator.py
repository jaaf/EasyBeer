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
#Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.­
'''
Created on 17 juin 2017

@author: jaaf
'''
#MaMousse
#Copyright (C) 2017 José FOURNIER

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

'''
Mass Calculation is based on three given numbers:
 — brewing_efficiency of the equipment: this value is not known the first time
 you use your equipment. In such a case a good starting value is 75%
 Once you have used it, you should measure it. See the relevant explanation 
 on how to do this in the help
 
 — targeted_original_gravity: the value entered by user is assumed to be a specific
 gravity i.e. density of wort/density of water
 
 — batch_volume: the volume that is drained into the fermentor: this volume
 is not exactly what is bottled due to the fermentor_dead_space (including
 volume used to measure gravity)
 
 To help understanding calculation, density is converted to Plato degrees.
 1 °P is 1g of soluble extract / 100 g of wort
 
 A common accepted approximation for relation between density and Plato degrees is:
 
 d = 259 (259 - P) or reversely
 
 P=259 - (259/d)
 
 Variables:
 
 batch_volume : given by user
 boiler_dead_space : given by user (equipment)
 mash_tun_dead_space: given by user (equiment)
 
 final_cold_boiler_volume: the volume of the wort at fermentation temperature
 
 (a) final_cold_boiler_volume = batch_volume + boiler_dead_space
 
 original_density: density of wort when input into the fermentor
 
(b) targeted_original_density = 0.998 kg/l * targeted_original_gravity

 0.998 is density of pure water at 20°C (the temperature is the one 
 at which the original gravity must be measured that is roughly the
 temperature at which the wort is put into the fermentor)
 
 (c) P=259 - (259 / targeted_original_density)
 
 example given:
 
 batch_volume=23 l, targeted_original_gravity = 1.060 , brewing_efficiency = 75 %
 boiler_dead_space=1 l
 (a) => final_cold_boiler_volume=23 l +1 l =24 l
 
 (b) => targeted_original_density = 1.060 * 0.998 l/kg = 1.057 kg/l
 
 (c) => P =259 -(259/1.057) =13.96 °P (% in mass)
 
 Once P is known, we can deduced the targeted total soluble extract yield
 
 (d) targeted_yield = final_cold_boiler_volume * targeted_original_density * P
 
 in the example: 24 l * 1.057 kg/l * 13.96 % =3.54 kg
 
 Given the malt's max_yield and the brewing_efficiency, we know we can expect:
 
 (e) expected_yield = malt_mass * malt_max_yield * brewing_efficiency
 
 As expected_yield must match targeted_yield we have:
 
 (f) malt_mass = (final_cold_boiler_volume * targeted_original_density * P )
 / (malt_max_xield * brewing_efficiency)
 
 in the example
 (f) => malt_mass=3.54 kg / 75% / 81 %) =5.82 kg
 
 
 STRIKE TEMPERATURE
 
 data required
 Tg: grain temperature (normally the room temperature if grain has stayed there long enough)
 T1: temperature of the first rest
 G: mass of the grain
 Dw density of water -0,0005125 t +1.0136550 for t between 50 and 70°C  e.g. at t=60°C d= 0.9829
 R weight per weight ration of water to grist
 Rv volume per weight ratio of water to grist Rv = Dw * R
 
 data calculated
 Ts strike temperature
 
 (g) Dw = -0.0005125 * T1 + 1.0136550 (We admit Ts is close enough to T1 to consider Dw as a constante)
 
 if K is the heat capacity of the water
 After stabilisation of temperature, water has lost:
 R*G * K (Ts-T1) 
 in the meantime, grain has gained
 G * 0.4 * K * (Tg-T1) 
 0.4 is the ratio between heat capacity of grain to heat capacity of water
 Thus we can write
 R * G (Ts - T1) = G * 0.4 (T1 - Tg) => 
 
 Ts = [ 0.4 (T1 -Tg) +R * T1] / R 
 
 (h) Tg = T1 + 0.4/R (T1 -Tg)
 
 SPARGE WATER VOLUME
 
 data required
 Vb batch volume , the volume you put into the fermentor
 Tb boiling time
 Hl boiler heat losses per hour (°C /hour)
 Vbds boiler dead space volume
 Vmtds mash tun dead space volume
 Vmw mash water volume
 Rr retention ratio water liters per dry malt kg (a constant roughly 1 l/kg)
 G total mass of grain
 
 Calculated
 Vsp Sparge water volume

Volume at the end of boil = Vb + Vbds (after cooling)
Volume at beginning of boil = Vb + Vbds + (Hl * Tb) (calculated from the end of process)

Volume at beginning of boil = Vmw - ( G * Rr) - Vmtds + Vsp

it comes

Vmw - (G * Rr) +Vsp = Vb +Vbds + (Hl * Tb)

(i)  Vsp = Vb + Vbds+ (Hl * Tb)  + (G *Rr) + Vmtds -Vmw

 


'''

import model.constants as mcst
import math
from model.Model import Model


class Calculator():
    ''''
    def __init__(self,batch_volume, boiler_dead_space,boiler_evaporation_rate, targeted_original_gravity,\
                  brewing_efficiency, malt_max_yield):
        self.batch_volume = batch_volume
        self.boiler_dead_space = boiler_dead_space
        self.boiler_evaporation_rate = boiler_evaporation_rate
        self.targeted_original_gravity = targeted_original_gravity
        self.brewing_efficiency = brewing_efficiency
        self.malt_max_yield = malt_max_yield
    '''    
    
    def __init__(self,model,recipe,equipment,batch_volume,boiling_time):
        self.recipe=recipe
        self.equipment=equipment
        self.batch_volume= batch_volume
        self.model=model
        self.boiling_time = boiling_time
        
    def get_final_cold_boiler_volume(self):
        return self.batch_volume + self.equipment.boiler_dead_space
      
    
    def get_targeted_original_density(self):
        return self.recipe.targeted_original_gravity * mcst.WATER_DENSITY_20
    
    def get_targeted_plato(self):
        tod = self.get_targeted_original_density()
        return 259 -(259/tod)
    
    def get_targeted_yield(self):
        P = self.get_targeted_plato()
        tod=self.get_targeted_original_density()
        fcbv = self.get_final_cold_boiler_volume()
        return fcbv * tod * P/100
    
    def get_malt_mass(self):
        max_yield=0
        for mim in self.recipe.malts_in_mash:
            #malt=mim.malt
            malt=self.model.get_malt(mim.malt)
            max_yield = max_yield +\
            ((malt.max_yield  * mim.percentage)/100)
        ty = self.get_targeted_yield()

        return ty / self.equipment.brewing_efficiency / max_yield *10000 #brewing_efficiency and malt_max_yiel are percentage
    
    def get_mash_water_volume(self, typ,ratio=None):
        tm=self.get_malt_mass()
        if typ ==1:#all in one type
            return tm * 2.7 + 3.5 #grainfather formulation
        if typ == 0:
            return tm * mcst.WATER_GRAIN_RATIO
        if typ==99:
            return tm * ratio
                
    def get_strike_temperature(self, water_volume, malt_mass, first_rest_temperature, grain_temperature):
        #(g) Dw = -0.0005125 * T1 + 1.0136550 (We admit Ts is close enough to T1 to consider Dw as a constante)
        water_density =    -0.0005125 * grain_temperature + 1.0136550
        R= (water_volume / malt_mass) * water_density
        # (h) Tg = T1 + 0.4/R (T1 -Tg)
        strike_temperature = first_rest_temperature + ((0.4/R)*(first_rest_temperature - grain_temperature))
        return strike_temperature
    
    def get_sparge_water_volume(self,mash_water_volume):
        #(i)  Vsp = Vb + Vbds+ (Hl * Tb)  + (G *Rr) + Vmtds -Vmw
        evaporation = self.equipment.boiler_evaporation_rate * self.boiling_time/60
        retention= self.get_malt_mass() * mcst.MALT_WATER_RETENTION_RATIO
        tun_dead_space=0
        if self.equipment.type == 0: tun_dead_space =self.equipment.mash_tun_dead_space
       
        print('mtds ' +str(tun_dead_space))
        print ('retention '+str(retention))
        print('evaporation '+ str(evaporation))
        print('batch volume '+str(self.batch_volume))
        sparge_water_volume = self.batch_volume + self.equipment.boiler_dead_space +evaporation+\
        (self.get_malt_mass()*mcst.MALT_WATER_RETENTION_RATIO) + tun_dead_space -mash_water_volume
        print('sparge '+str(sparge_water_volume))
        return sparge_water_volume
        
        
    def get_f_t(self,t): 
        f_t= (1 - math.exp(-0.04 * t))   / 4.15
        print('f(t) ='+str(f_t))
        return f_t
    
    def get_f_G(self,gravity):
        f_G=1.65 * (0.000125 **(gravity-1))
        print('f_G = '+str(f_G))
        return f_G
    
        
    def get_IBU(self,duration,gravity,mass, alpha,final_volume): 
        '''
        duration in min.,specific gravity i.e. 1.060, mass of hop in g, alpha en % i.e. 12
        ''' 
        return (10 / final_volume) * mass * self.get_f_G(gravity) * self.get_f_t(duration) * alpha  
            
            
        