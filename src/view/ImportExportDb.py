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

from PyQt5.QtWidgets import QWidget,QMessageBox,QFileDialog

from gen import ImportExportDbUI
from model.Malt import Malt
import view.constants as vcst
import view.styles as sty
import shutil
import os,sys

class ImportExportDb(QWidget,ImportExportDbUI.Ui_Form ):
    """
       class docs
    """   
    
    def __init__(self,model,controller,util,bundle_dir):
        QWidget.__init__(self,None,QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.model = model
        self.controller=controller
        self.util=util
        self.bundle_dir=bundle_dir
        self.fileDialog=QFileDialog()
        self.set_initial_display_attributes()
        self.set_translatable_textes()
        self.init_dialog_and_connections()
        
    def set_translatable_textes(self):
        self.explain_text_edit.setText(self.tr(
        '''
        <h2>Import or Export your Database</h2>
        <p>Whenever you record an ingredient (malt, hop, etc.), a recipe or an equipment, the recording is done in an sqlite database table. These database is placed 
        in the folder you downloaded at the time of installing the application on your computer.</p>
        <p>Each time your reinstall the application for updating, the install folder is clean from any database and a new database is created whenever you decide 
        to record something. In other word, the database you created during previous install is lost.</p>
        <p>In order to permit you to save your previous recordings, the application allows you to export, and then import, this database.</p>
        <p style="color: green; font-weight:bold;">It is something very easy you should do before an updating, or a reinstall of the program</p>
        
        
        '''    
            ))
        self.export_label.setText(self.tr('Export to'))   
        self.import_label.setText(self.tr('Import from')) 
        self.proceed_export_button.setText(self.tr('Export Now'))
        self.proceed_import_button.setText(self.tr('Import Now'))
        
 
        
    def init_dialog_and_connections(self):
        self.proceed_export_button.clicked.connect(self.export_db)
        self.proceed_import_button.clicked.connect(self.import_db)
        self.select_export_folder_button.clicked.connect(self.navigate_export)
        self.select_import_folder_button.clicked.connect(self.navigate_import)
        self.close_button.clicked.connect(self.close)
        
    def set_initial_display_attributes(self):
        self.proceed_export_button.setVisible(False)
        self.proceed_import_button.setVisible(False) 
       
            
    def import_db(self):
        answer=self.util.confirm_dialog(self.tr(
            '''
            <h2>Warning!</h2>
            <p>You are on the verge of importing a new database</p>
            <p style="color: red; font-weight:bold;"> Be aware that this will overwrite the database you are presently using.</p>
            <p>If you are not absolutely sure of the opportunity of your new import and you want to preserve your present database, <span style="color: green; font-weight:bold;">you may want 
            to export it in a safe place prior to doing the import</span></p>
            <p style="color: red; font-weight:bold;"> The application will instantly restart after an import!<p>
            <br/>
            <p style="font-weght:bold; font-size:large;">Are you sure you want to import the database?</p>  
            
            <br/>  
        
            '''
            ))
        
        if answer == QMessageBox.Ok:
            print('Ok pressed')
            results=self.move_files(self.import_folder_edit.text(),self.bundle_dir)
            self.util.alerte(self.tr(
                '''<p><strong>Congratulations!</strong> you have imported the following file'''+results+'</p>'+
                 '<p>In order to use it, your application is going to restart instantly.</p>'))
            
            self.restart_program()
            
        elif answer == QMessageBox.Cancel:
            print ('Cancel pressed')
            self.proceed_import_button.setVisible(False)
            self.import_folder_edit.clear()

                     
     
        print(str(answer))
       
    def export_db(self):
        answer=self.util.confirm_dialog(self.tr(
            '''
            <h2>Warning!</h2>
            <p>Your are on the verge of exporting your present database.</p>
            <p>This will not delete it.<span style="color: red; font-weight:bold;"> Nevertheless, be aware that this will overwrite any other database with the same name that already exist in the destination
            folder</span>. </p>
            <pstyle="color: red; font-weight:bold;">If your are not sure, cancel this operation and double check you destination folder.</p>
            <br/>
            <p style="font-weght:bold; font-size:large;">Are you sure you want to export the database?</p>
            <br/>
            '''
            ))  
        if answer == QMessageBox.Ok:
            print('Ok pressed')
            results=self.move_files(self.bundle_dir,self.export_folder_edit.text())
            self.util.alerte(self.tr(
                '''<p><strong>Congratulations!</strong> you have exported the following file'''+results+'</p>'+
                 '<p>You may want to check that it really is now in the destination folder.</p>'+
                  '<p> If you are finished with the import export dialog, you can safely close it.'))
        elif answer == QMessageBox.Cancel:
            print ('Cancel pressed')
            self.proceed_export_button.setVisible(False)
            self.export_folder_edit.clear()
                   
                   
    def move_files(self,source,destination):    
        
        print('moving files from '+source+' to '+destination)
        results=''
        files=os.listdir(source)
        for file in files:
            if file.endswith(".db"):
                print('copying file : '+file)
                results=results+'<br/>'+file
                shutil.copy(os.path.join(source,file),os.path.join(destination,file))
        return(results)    
     
    def navigate_import(self):
        print('In navigate import')
        directory=self.fileDialog.getExistingDirectory(self,'Select a directory','', QFileDialog.ShowDirsOnly)
        self.export_folder_edit.setText('')
        self.import_folder_edit.setText(directory)
        self.proceed_export_button.setVisible(False)
        self.proceed_import_button.setVisible(True) 
        print('this is the import directory : '+directory)
        
    
    def navigate_export(self):
        print('In navigate export')
        directory=self.fileDialog.getExistingDirectory(self,'Select a directory','', QFileDialog.ShowDirsOnly)
        self.import_folder_edit.setText('')
        self.export_folder_edit.setText(directory)
        self.proceed_export_button.setVisible(True)
        self.proceed_import_button.setVisible(False)  
        print('this is the export directory : '+directory)
        
    def restart_program(self):
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        python = sys.executable
        os.execl(python, python, * sys.argv)
        
          