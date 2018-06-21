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

class Malt(object):
    '''
    A class to store a malt\'s attributes in a brewing session
    '''
    def __init__(self,name,maker,max_yield,color,kolbach_min,kolbach_max):   
        self.name = name
        self.maker=maker 
        self.max_yield = max_yield
        self.color=color    #Fine Grain Dry Basis yield (a percentage)
        self.kolbach_min=kolbach_min
        self.kolbach_max=kolbach_max
        
    # def __repr__(self):
    #     return ('maltType[name=%s, full_name=%s,FGDB=%d,color=%d]' % 
    #     ( self.name,self.full_name, self.FGDB,self.color) )
   
    def test(self): 
        print('I am a MaltType object')



        