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
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,QHBoxLayout,QLabel,QLineEdit,QMessageBox,QFrame,QComboBox
import view.constants as vcst
import view.styles as sty
import collections


class Utils(QWidget):
    '''
    This class is derived from QWidget to benefit from the self.tr function
    '''
    hop_usage_dic=None
    
    def __init__(self):
        QWidget.__init__(self)
 
        
    def init_hop_usage_dic(self):
        d=collections.OrderedDict()
        d[vcst.HOP_USAGE_UNDEFINED]= ''
        print('voici vcst.HOP_MASH_HOPPING : '+vcst.HOP_MASH_HOPPING)
        d[vcst.HOP_MASH_HOPPING]=self.tr('Mash hopping')
        d[vcst.HOP_FIRST_WORT_HOPPING]=self.tr('First wort hopping')
        d[vcst.HOP_BOILING_HOPPING]=self.tr('Boil hopping')
        d[vcst.HOP_HOP_BACK_HOPPING]=self.tr('Hop back hopping')
        d[vcst.HOP_DRY_HOPPING]=self.tr('Dry hopping')
        self.hop_usage_dic=d
        print('printing dic')
        print(d) 
                    
    def alerte(self,message,icon=QMessageBox.Information, title=None):
        msg = QMessageBox()
        msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        msg.setIcon(icon)
        msg.setText(message)
        if title: msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
       
        
  
    def alerte_bad_input(self,txt=''): 
        #print(MW.tr('translated indirectly'))
        msg = QMessageBox()   
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        msg.setText(txt)
        msg.setWindowTitle(self.tr("Warning Bad Input: "))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        
    
   
    def check_input(self,w,flag_txt=True,info='',acceptNone=False,min_value=0.0,max_value=0.0,calculated_value=None):
  
        '''
        w is the widget whose value is checked
        flag_txt: True if text expected, False if num expected
        info: additional text to the basic message of alerte_bad_input
        acceptNone: accept None value silently (no alert)
        '''    
       
        if isinstance(w,QComboBox):
            t=w.currentText()   
        else: 
            t=w.text()
        print (t)  
            
        #case nothing entered    
        if acceptNone and not t:
            print('None accepted')
            return '_undeclared_'    
        
        #case of string
        if flag_txt and t:
            
            if calculated_value: w.setStyleSheet(sty.field_styles['calculated'])
            else: w.setStyleSheet(sty.field_styles['editable'])
            return t
        #case on numerical value
        elif ((not flag_txt) and t):
            try:
                print('value before float transformation '+str(t))
                value=float(t)
                print('value converted '+str(value))
            except :
                tx=self.tr('Value for '+info+self.tr('was not convertible to float.Please check your input.'))  
                w.setStyleSheet(vcst.EDIT_ALERTE_STYLE)
                self.alerte_bad_input(tx)
                return None  
            
            print('ready to check value '+str(value))
            if isinstance(value, float):#if value and value >=0.0:
                print('value is good')
                if value <min_value or value>max_value:
                    tx=self.tr('Value for ')+info+self.tr(', is not valid. It should be between ')+str(min_value)+ \
                    self.tr(' and ')+str(max_value)
                    w.setStyleSheet(vcst.EDIT_ALERTE_STYLE)
                    self.alerte_bad_input(tx)
                    print('returning None')
                    return None
                
                print('testing calculated_value')
                if calculated_value: w.setStyleSheet(sty.field_styles['calculated'])
                else: w.setStyleSheet(sty.field_styles['editable'])
                print('returning '+str(value))
                return float(w.text())#why not return(value)
            
            print('before EE '+str(value))
            tx=self.tr('Input for ')+info+ self.tr(' is not a readable value')+str(value)
            w.setStyleSheet(vcst.EDIT_ALERTE_STYLE)
            self.alerte_bad_input(tx)
       
        
        tx=self.tr('CC There is no readable value for ')+info+self.tr('. Please check your input!')
        w.setStyleSheet(vcst.EDIT_ALERTE_STYLE)
        self.alerte_bad_input(tx)
        return None 
    
    def confirm_dialog(self,message):
        question=QMessageBox()
        question.setIcon(QMessageBox.Information)
        question.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        question.setText(message)
        question.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        return(question.exec_())
        



    #list all widgets included in a layout recursively
    def get_included_widgets(self,layout):
        result=[]
        for i in range(layout.count()): 
            item = layout.itemAt(i)
            if item.widget():
                result.append(item.widget())
            elif(item.layout()) :
                tampon=self.get_included_widgets(item.layout())  
                result=result+tampon
        return result        
    
    def clearLayout(self, layout):
        if layout:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                else :
                    self.clearLayout(item.layout())
                layout.removeItem(item) 

    def get_by_name(self,layout,name):
        'return the widgt which name is given in first level'
        for i in range(layout.count()):
            try:
                if layout.itemAt(i).widget().accessibleName()==name:
                    return layout.itemAt(i).widget()
            except:
                pass
        return None    
      
    def get_by_name_recursive(self,layout,name):
        'find a widget by name whatever its deepness' 
        for i in range(layout.count()):
            item = layout.itemAt(i)
            try:
                if item.widget().accessibleName() == name:
                    return item.widget()
                                  
            except:
                try: 
                    if item.layout():
                        w=self.get_by_name_recursive(item.layout(),name)
                        if w: return w
                except:
                    pass
              
        return None     


    def get_containing_layout(self,layout,name):
        'Find a layout in a layout that contains the widget the name of which is given: Recursive'
        #print ('trying to find a containing layout')
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item.widget():
                #print('get_containing :'+item.widget().accessibleName())
                if item.widget().accessibleName()==name:
                    #print ('returning a layout')
                    return layout
            
            if item.layout():
                    #print('looping on found layout')
                    return self.get_containing_layout(item.layout(), name)
  
        return None 
    
    def get_usage_key(self,v):
        for key,val in   self.hop_usage_dic.items():
            if val == v:
                return key
        return None    