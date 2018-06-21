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
from PyQt5.QtWidgets import QWidget
from gen import FolderChooserUI
from PyQt5.QtWidgets import QFileDialog
import os

class FolderChooser(QWidget,FolderChooserUI.Ui_Form ):
    
    def __init__(self):
        QWidget.__init__(self,None,QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.database_path=''
        self.set_editable_text()
        self.folder_name=None
        self.set_connexions()

    def set_editable_text(self):
        self.pushButton.setText(self.tr('Choose a folder for databases'))
        self.textEdit.setText(self.tr('''
        <h2>Choose a Folder for your Databases</h2>
        
        <p>As you know, JolieMousse uses databases for storing definitions for  malt, yeast, hop, recipe, equipment, etc.  </p>
        
        <p>In order to make these databases protected during updating of the software, it is necessary to put them in a folder
        that is independent from installation folder.</p>
        
        <p>Moreover, you may want to use different folders in order to save different sets of databases</p>
        
        <p>By clicking the button below, you can choose a folder for these databases. Later, you will be able to change it using the Preferences menu.</p>
        
        '''))
        
    def set_connexions(self):
            self.pushButton.clicked.connect(self.navigate_files)
            
    def navigate_files(self):        
        name=QFileDialog.getExistingDirectory()
        
        f = open('database_folder.txt', 'w')
        f.write(name)
        f.close()
        
        print(name)
        self.close()
    
    def closeEvent(self,event):
        print('closing FolderChooser Window')
        if (os.path.isfile('database_folder.txt')):
            f = open('database_folder.txt', 'r')
            self.database_path=f.read()
            f.close()
            print('lecture du path des DB : '+self.database_path) 
            
