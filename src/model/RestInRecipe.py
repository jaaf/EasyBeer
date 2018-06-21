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

class RestInRecipe(object):
    'A class to store a malt\'s attributes in a breewing session'
    def __init__(self,purpose, duration, temperature):
        self.purpose = purpose  
        self.duration = duration 
        self.temperature=temperature

    def __repr__(self):
        return ('RestInSession[purpose=%s, duration=%d, temperature=%d]' % 
        ( self.purpose, self.duruation,self.temperature ))