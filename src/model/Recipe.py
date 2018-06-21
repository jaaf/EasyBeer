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

class Recipe(object):
    'A recipe'
    
    
    
    def __init__(self,name, malts_in_mash,mash_rests,hops_in_recipe,targeted_original_gravity,targeted_bitterness,boiling_time,yeast_in_recipe,
                 fermentation_explanation):
        self.name = name
        self.malts_in_mash=malts_in_mash
        self.mash_rests = mash_rests #the various rests in mashing
        self.hops_in_recipe=hops_in_recipe
        self.targeted_original_gravity=targeted_original_gravity
        self.targeted_bitterness=targeted_bitterness
        self.boiling_time =boiling_time
        self.yeast_in_recipe=yeast_in_recipe
        self.fermentation_explanation=fermentation_explanation
        