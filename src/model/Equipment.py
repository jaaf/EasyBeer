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


class Equipment(object):
    
    '''
    A class to store an equipment\'s attributes in a brewing session
    '''
    
 
        
    def __init__(self,name,brewing_efficiency,boiler_size,\
                 boiler_dead_space,boiler_evaporation_rate, fermentor_size,fermentor_dead_space,type,mash_tun_size,mash_tun_dead_space,\
                 mash_tun_heat_losses):
        self.name = name      #designation
        self.brewing_efficiency = brewing_efficiency
        self.type=type
        self.mash_tun_size=mash_tun_size
        self.mash_tun_dead_space=mash_tun_dead_space
        self.mash_tun_heat_losses=mash_tun_heat_losses
        self.boiler_size=boiler_size
        self.boiler_dead_space=boiler_dead_space
        self.boiler_evaporation_rate = boiler_evaporation_rate
        self.fermentor_size=fermentor_size
        self.fermentor_dead_space=fermentor_dead_space
        
    def __repr__(self):

        return 'Equipment(name={self.name!r}\n\
         brewing_efficiency = {self.brewing_efficiency!r}\n\
         type = {self.type!r}\n\
         mash_tun_size = {self.mash_tun_size!r}\n\
         mash_tun_dead_space ={self.mash_tun_dead_space!r}\n\
         mash_tun_heat_losses ={self.mash_tun_heat_losses!r}\n\
         boiler_size = {self.boiler_size!r}\n\
         boiler_evaporation_rate = {self.boiler_evaporation_rate!r}\n\
         boiler_dead_space= {self.boiler_dead_space!r}\n\
         fermentor_size ={self.fermentor_size!r}\n\
         fermentor_dead_space ={self.fermentor_dead_space!r}\n\
         )'.format(self=self)
        