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


class Yeast(object):
  
    def __init__(self,name,maker,max_allowed_temperature,min_allowed_temperature,max_advised_temperature,min_advised_temperature,form,attenuation,floculation):   
        self.name = name 
        self.maker = maker
        self.max_allowed_temperature=max_allowed_temperature
        self.min_allowed_temperature=min_allowed_temperature
        self.max_advised_temperature=max_advised_temperature
        self.min_advised_temperature=min_advised_temperature
        self.form = form
        self.attenuation=attenuation
        self.floculation=floculation

    
   
    def test(self): 
        print(self.tr('I am a Yeast object'))