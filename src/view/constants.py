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
'''
Created on 15 juin 2017

@author: jaaf
'''
from PyQt5.QtGui import QFont


FIELD_DEFAULT_COLORS={
    'editable': ['#F3D3E9','#000000'],
    'calculated':['#F5AC4C','#000000'],
    'read_only': ['#CCCCCC','#000000'],
    'min_max_allowed': ['#EB5811','#FFFFFF'],
    'min_max_advised': ['#7AD853','#000000'],
    'optional_editable':['#f0D0E7','#000000']    
    }      

MAIN_COMBO_SELECTION_STYLE="selection-background-color:rgba(0,255,255); color: black;"


#EDITABLE_STYLE="color: #F3D3E9; background-color: pink;"
OPTIONAL_EDITABLE_STYLE="color: rgba(255,0,0); background-color: violet;"
READ_ONLY_STYLE="color: rgb(0, 0, 0);background-color: rgb(230,230,230);"
MIN_MAX_ALLOWED_STYLE="color: rgb(255, 0, 0);background-color: orange;"
MIN_MAX_ADVISED_STYLE="color: rgb(0, 120, 0);background-color: rgba(0,255,0,50);"
BUTTON_DELETE_STYLE="font-size: 14px;color: 'red';background-color: rgb(230,230,230);font-weight: bold; "
EDIT_ALERTE_STYLE="background-color: red; color: white;"
EDIT_NORMAL_STYLE="background-color: white; color: black;"
EDIT_CALCULATED_STYLE="font-size: 14px;color: 'green';background-color: orange;font-weight: bold; "
WARNING_STYLE="font-size: 14px;color: 'green';background-color: rgb(255,153,0);font-weight: bold; "
QUESTION_BUTTON_STYLE='font-size: 14px; font-weight: bold'
CUSTOM_LABEL_STYLE="color: green; font-style:oblique"
ORIGINAL_GRAVITY_ALERT='texte à traduire'


MAX_MASH_TUN_SIZE=100
MAX_MASH_TUN_HEAT_LOSSES=10
HOP_USAGE_UNDEFINED ='Undefined'
HOP_MASH_HOPPING= "Mash"
HOP_FIRST_WORT_HOPPING= "First Wort"
HOP_BOILING_HOPPING='Boiling'
HOP_HOP_BACK_HOPPING='Hop back'
HOP_DRY_HOPPING='Dry'

QUESTION_BUTTON_MAX_WIDTH=30

'QFont(QString family, int pointSize = -1, int weight = -1, bool italic = False)'
'QFont(QString family, int pointSize = -1, int weight = -1, bool italic = False)'
TITLE_FONT_L=QFont('Free Sans',11,QFont.Bold)
BUTTON_FONT_L=QFont('Free Sans',10,QFont.DemiBold)
FIELD_LABEL_FONT_L=QFont('Free Sans',10,QFont.Normal)
TITLE_SLANTED_FONT_L=QFont('Free Sans',11,QFont.Normal,True)



'QFont(QString family, int pointSize = -1, int weight = -1, bool italic = False)'
TITLE_FONT_W=QFont('Helvetica',11,QFont.Bold)
BUTTON_FONT_W=QFont('Helvetica',10,QFont.DemiBold)
FIELD_LABEL_FONT_W=QFont('Helvetica',10,QFont.Normal)
TITLE_SLANTED_FONT_W=QFont('Helvetica',10,QFont.Normal,True)


