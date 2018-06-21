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

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,QHBoxLayout,QLabel,QLineEdit,QMessageBox,QFrame,QProgressBar

DEFAULT_STYLE = """
QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}

QProgressBar::chunk {
    background-color: green;
    width: 10px;
    margin: 0px;
}
"""

COMPLETED_STYLE = """
QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}

QProgressBar::chunk {
    background-color: red;
    width: 10px;
    margin: 0px;
}
"""

class CustomProgressBar(QProgressBar):
    def __init__(self, parent = None):
        QProgressBar.__init__(self, parent)
        self.setStyleSheet(DEFAULT_STYLE)

    def setValue(self, value):
        QProgressBar.setValue(self, value)
        print('CustomProgressBar : maximum = '+str(self.maximum()))
        print ('CustomProgressBar : minimum = '+str(self.minimum()))
        low=float(self.maximum() ) * 0.45
        
        print('CustomProgressBar : low = '+ str(low))
        
        up=float(self.maximum()) * 0.55
        print('CustomProgressBar : up = '+str(up))
        if float(value) <low  or float(value) > up :
            
            self.setStyleSheet(COMPLETED_STYLE)
        else:
            self.setStyleSheet(DEFAULT_STYLE)    