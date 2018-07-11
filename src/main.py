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
from PyQt5.QtWidgets import QApplication
import sys, os
from view.MainWindow import MainWindow
import encodings

 

if __name__=='__main__':
    current_exit_code=MainWindow.EXIT_CODE_REBOOT
    while current_exit_code == MainWindow.EXIT_CODE_REBOOT:
        app = QApplication(sys.argv)
        translator = QtCore.QTranslator()
        (filepath,filename)=os.path.split(__file__)
        #trad_path=os.path.join(filepath,'translate','fr_FR.qm')
        #translator.load(os.path.join(trad_path))
   
        app.installTranslator(translator)
        mainWindow = MainWindow(translator)
        MainWindow.show(mainWindow)
        #sys.exit(app.exec_())
        current_exit_code=app.exec_()
        app=None