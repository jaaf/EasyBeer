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
from PyQt5.QtWidgets import  QWidget,QMessageBox,QComboBox
import view.constants as vcst
import view.styles as sty
import collections
import os




class Utils(QWidget):
    '''
    This class is derived from QWidget to benefit from the self.tr function
    '''
    hop_usage_dic=None
    
    def __init__(self,model):
        QWidget.__init__(self)
        self.model=model
 
        
    def init_hop_usage_dic(self):
        d=collections.OrderedDict()
        d[vcst.HOP_USAGE_UNDEFINED]= ''
        d[vcst.HOP_MASH_HOPPING]=self.tr('Mash hopping')
        d[vcst.HOP_FIRST_WORT_HOPPING]=self.tr('First wort hopping')
        d[vcst.HOP_BOILING_HOPPING]=self.tr('Boil hopping')
        d[vcst.HOP_HOP_BACK_HOPPING]=self.tr('Hop back hopping')
        d[vcst.HOP_DRY_HOPPING]=self.tr('Dry hopping')
        self.hop_usage_dic=d
                    
    def alerte(self,message,icon=QMessageBox.Information, title=None):
        msg = QMessageBox()
        msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        msg.setIcon(icon)
        msg.setText(message)
        if title: msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
       
        
  
    def alerte_bad_input(self,txt=''): 
        msg = QMessageBox()   
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        msg.setText(txt)
        msg.setWindowTitle(self.tr("Warning Bad Input: "))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        
    
   
    def check_input(self,w,flag_txt=True,info='',acceptNone=False,min_value=0.0,max_value=0.0,calculated_value=None,unit=None):
  
        '''
        w is the widget whose value is checked
        flag_txt: True if text expected, False if num expected
        info: additional text to the basic message of alerte_bad_input
        acceptNone: accept None value silently (no alert)
        if unit given, convert the value
        '''  
        if isinstance(w,QComboBox):
            t=w.currentText()     
        else: 
            t=w.text()   
        #case nothing entered    
        if acceptNone and not t:
            return ''    
        
        #case of string
        if flag_txt and t:
            
            if calculated_value: w.setStyleSheet(sty.field_styles['calculated'])
            else: w.setStyleSheet(sty.field_styles['editable'])
            return t
        #case on numerical value
        elif ((not flag_txt) and t):
            try:
                raw=float(t)
            except :
                tx=self.tr('Value for '+info+self.tr('was not convertible to float.Please check your input.'))  
                w.setStyleSheet(vcst.EDIT_ALERTE_STYLE)
                self.alerte_bad_input(tx)
                return None  
            
            if unit:
                value=self.convert_from(unit,raw)
                print ('unit is '+unit.unit)
                print ('converted value ='+str(value))
            else:
                value=raw   
                print ('value '+ str(value)+' has not been converted') 
                
            
            if isinstance(value, float):#if value and value >=0.0:
                print('value is float '+str(value)+' - '+str(min_value)+ ' - '+str(max_value))
                if value <min_value or value>max_value:
                    if unit:
                        v_min=self.convert_to(unit,min_value)
                        v_max=self.convert_to(unit,max_value)
                        label=self.get_unit_label(unit)
                    else:
                        v_min=min_value
                        v_max=max_value
                        label=''
                     
                        
                    tx=self.tr('Value for ')+info+self.tr(', is not valid. It should be between ')+str(v_min)+ \
                    self.tr(' and ')+str(v_max)+' '+ self.get_unit_label(unit)
                    w.setStyleSheet(vcst.EDIT_ALERTE_STYLE)
                    self.alerte_bad_input(tx)
                    return None
                
       
                if calculated_value: w.setStyleSheet(sty.field_styles['calculated'])
                else: w.setStyleSheet(sty.field_styles['editable'])
                return value
    
            tx=self.tr('Input for ')+info+ self.tr(' is not a readable value')+str(value)
            w.setStyleSheet(vcst.EDIT_ALERTE_STYLE)
            self.alerte_bad_input(tx)
       
        
        tx=self.tr('CC There is no readable value for ')+info+self.tr('. Please check your input!')
        w.setStyleSheet(vcst.EDIT_ALERTE_STYLE)
        self.alerte_bad_input(tx)
        return None 
    
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
                
    
    def confirm_dialog(self,message):
        question=QMessageBox()
        question.setIcon(QMessageBox.Information)
        question.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        question.setText(message)
        question.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        return(question.exec_())
        
    def convert_to(self,unit,value):
        'convert a mksa value in db into an other unit for display'
        target=unit.unit
        if unit.name=='temperature':
            if target == 'Farenheit':
                ret=(value*1.8)+32
                return ('{0:.1f}'.format(ret))  
            else: 
                return ('{0:.1f}'.format(value))
            
        if unit.name=='delta_temperature':
            if target=='Farenheit':
                ret=value*1.8
                return ('{0:.1f}'.format(ret) )
            else: return ('{0:.1f}'.format(value))
                 
            
        if unit.name=='malt_mass':
            if target== 'Pound':
                ret=value*2.2046244202
                return ('{0:.1f}'.format(ret) ) 
            else: return ('{0:.1f}'.format(value))
            
        if unit.name =='yeast_mass':
            if target == 'Ounce':
                ret=value*0.0352739907
                return ('{0:.2f}'.format(ret))
            else: return ('{0:.1f}'.format(value )) 
            
        if unit.name=='water_volume':
            if target=='Gallon':
                ret=value*0.2641721769
                return ('{0:.2f}'.format(ret))
            if  target =='Quart':
                ret=value*1.0566887074
                return ('{0:.1f}'.format(ret))
            if target =='Pint':
                ret=value*2.1133774149
                return ('{0:.1f}'.format(ret))
            if target =='Liter':
                return ('{0:.1f}'.format(value))
            return ('{0:.1f}'.format(value))
        
        if unit.name=='hop_rate':
            if target=='Gram per liter':
                return ('{0:.1f}'.format(value))
            if target=='Gram per gallon':
                ret=value*3.78541
                return ('{0:.1f}'.format(ret))
            if target=='Ounce per gallon':
                ret=value*0.133526
                return ('{0:.3f}'.format(ret))
            
        if unit.name=='hop_mass':
            if target=='Gram':
                return ('{0:.2f}'.format(value))
            if target=='Ounce':
                return ('{0:.2f}'.format(value*0.0352739907))
            
        if unit.name=='yeast_rate':
            if target=='Billion/°P/Liter':
                return      ('{0:.2f}'.format(value))
            if target=='Billion/°P/Gallon':
                return ('{0:.2f}'.format(value*3.78541))
            
    def convert_from(self,unit,value): 
        origin=unit.unit
        if unit.name=='temperature':
            if origin == 'Farenheit':
                return ((value-32)/1.8)
            else: 
                return value
            
        if unit.name=='delta_temperature':
            if origin =='Farenheit':
                return value/1.8
            if origin =='Celsius':    
                return value
            
        if unit.name=='malt_mass':
            if origin== 'Pound':
                return value*0.453592 
            else: return value
            
        if unit.name =='yeast_mass':
            if origin == 'Ounce':
                return value    *28.3495
            else: return value  
            
        if unit.name=='water_volume':
            if origin=='Gallon':
                return value*3.78541
            if  origin =='Quart':
                return value*0.9463525
            if origin =='Pint':
                return value*0.47317625
            if origin =='Liter':
                return value
            return value  
        
        if unit.name=='hop_rate':
            if origin=='Gram per liter':
                return value
            if origin=='Gram per gallon':
                return value*0.2641721769
            if origin=='Ounce per gallon':
                return value*7.4891
            
        if unit.name=='hop_mass':
            if origin=='Gram':
                return value
            if origin=='Ounce':
                return value*28.3495   
            
        if unit.name=='yeast_rate':
            if origin=='Billion/°P/Liter':
                return value 
            if origin=='Billion/°P/Gallon':
                return value*  0.2641721769  
    
    def create_session_sheet(self,session):
        if(os.path.isfile('session_sheet.html')):
            os.remove('session_sheet.html')
        file=open('session_sheet.html','w')
        
        table_style='''
        <!-- CSS goes in the document HEAD or added to your external stylesheet -->
        <style type="text/css">
        table.gridtable {
        width:1000px;
         font-family: verdana,arial,sans-serif;
         font-size:11px;
         color:#333333;
         border-width: 1px;
         border-color: #666666;
         border-collapse: collapse;
         }
        table.gridtable th {
          border-width: 1px;
          padding: 8px;
          border-style: solid;
          border-color: #666666;
          background-color: #dedede;
          
         }
        table.gridtable td {
            border-width: 1px;
            padding: 8px;
            border-style: solid;
            border-color: #666666;
            background-color: #ffffff;
         }
         table.gridtable tr{
            height: 50px;
         }
        </style>
        '''
        file.write('<!DOCTYPE html>')
        file.write('<html>')
        file.write('<head>')
        file.write('<meta charset="utf-8"/>')
        file.write(table_style)
        file.write('</head>')
        file.write('<body style="line-height:2em">')
        file.write('<h1>Session Sheet for '+str(session.recipe)+'</h1>')
        file.write(session.name)
        file.write('<h2>Session Targets</h2>')
        v_unit=self.model.get_unit('water_volume')
        v_unit_label=self.get_unit_label(v_unit)
        t_unit=self.model.get_unit('temperature')
        t_unit_label=self.get_unit_label(t_unit)
        m_unit=self.model.get_unit('malt_mass')
        m_unit_label=self.get_unit_label(m_unit)
        h_unit=self.model.get_unit('hop_mass')
        h_unit_label=self.get_unit_label(h_unit)
        y_unit=self.model.get_unit('yeast_mass')
        y_unit_label=self.get_unit_label(y_unit)
        
        
        
        file.write(self.tr('Batch Volume = ')+self.convert_to(v_unit,session.batch_volume)+\
                   ' '+v_unit_label+' — '+self.tr('Targeted Original Gravity = ')+str(session.targeted_original_gravity)+\
                   ' — '+self.tr('Targeted Bitterness = ')+str(session.targeted_bitterness))
        
        file.write('<hr size="5px" color="blue"/>')
        
        
        file.write('<h2>'+self.tr('Mash')+'</h2>')
        file.write('<div style="margin-left:2em">')
        file.write(self.tr('Mash Water Volume = ')+self.convert_to(v_unit,session.mash_water_volume)+' '+v_unit_label+\
                   ' at '+self.convert_to(t_unit,session.strike_temperature)+' '+t_unit_label+'</br>')
        malts=session.malts_in_session
        file.write('<h3>'+self.tr('Malts')+'</h3>') 
        for m in malts:
            file.write(m.name +' : ' +self.convert_to(m_unit,m.amount)+' '+m_unit_label+' — ')
            
        file.write('<h3>'+self.tr('Rests')+'</h3>')    
        file.write('<div style="margin-left:1em">')
        i=0    
        for r in session.rests_in_session:
            i=i+1
            file.write('<strong>'+self.tr('Rest')+' '+str(int(i))+' : </strong>'+r.purpose)
            
            file.write('<div style="margin-left:1em"> ')
            file.write(self.tr('Temperature')+' = '+self.convert_to(t_unit,r.temperature)+' '+t_unit_label+' —  '\
                       + self.tr('Duration = ')+str(r.duration)+' min.<br/>'   ) 
            file.write('</div>')
           
        file.write('</div>')  #ends rests
        
        file.write('</div>') #ends mash
           
        file.write('<hr size="5px" color="blue"/>')    
        
        file.write('<h2>'+self.tr('Boil')+'</h2>')
        file.write('<div style="margin-left:2em">')
        file.write('<h3>'+self.tr('Hops')+'</h3>') 
        file.write('<div style="margin-left:1em">')
        i=0
        for h in session.hops_in_session:
            i=i+1
            file.write('<strong>'+self.tr('Hop')+' '+str(int(i))+' : </strong>'+h.name)
            file.write('<div style="margin-left:1em"> ')
            file.write(self.tr('Usage')+' = '+str(h.usage)+' — '\
                       +self.tr('Amount = ')+self.convert_to(h_unit,h.amount) + ' '+h_unit_label+' — '+ self.tr('Duration = ')+str(h.duration)+' min.<br/>'   ) 
            file.write('</div>')
        
        file.write('</div>') #ends hops
        file.write('</div>') #ends Boil 
        
        file.write('<hr size="5px" color="blue"/>')
        file.write('<h2>'+self.tr('Pitching')+'</h2>')
        file.write('<div style="margin-left:2em">')
        file.write('<h3>'+self.tr('Yeast')+'</h3>') 
        file.write('<div style="margin-left:1em">')
        y =session.yeast_in_session
            
        
        file.write(y.name+' : '+self.tr('Amount')+ '= '+self.convert_to(y_unit,y.amount)+' '+y_unit_label)
        
        file.write('</div>') #ends yeast
        file.write('</div>') #ends pitching
        
        
        file.write('<h2>'+self.tr('Feedback')+'</h2>')
        file.write('<h3>'+self.tr('Measurements')+'</h3>')
        table='''
         <table class="gridtable">
         <tr>
            <th>
            '''\
            +self.tr('Mash PH')+ '</th><th>'+self.tr('Preboil Volume at 100°C')+'</th>\
            <th>'+self.tr('Actual Fermentor Volume')+'</th><th>'+self.tr('Original Gravity')+'</th>\
            <th>'+self.tr('Intermediate Gravity')+'</th><th>'+self.tr('Final Gravity')+'</th>\
        </tr>'\
        +'''
        <tr>
            <td> </td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            
        </tr>

        </table> 
        '''
        file.write(table)
        file.write('</body>')
        file.write('</html>')
        file.close()
      
        
        

    def get_by_name(self,layout,name):
        'return the widget which name is given in first level'
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
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item.widget():
                if item.widget().accessibleName()==name:
                    return layout
            
            if item.layout():
                    return self.get_containing_layout(item.layout(), name)
  
        return None          

    'list all widgets included in a layout recursively'
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
    
    
    def get_unit_label(self,unit):
        if unit.unit=='Farenheit': return '°F'
        if unit.unit=='Celsius': return '°C'
        if unit.unit=='Gram per liter' : return 'g/l'
        if unit.unit=='Gram per gallon': return 'g/gal.'
        if unit.unit=='Ounce per gallon': return 'oz./gal.'
        if unit.unit=='Liter': return 'l'
        if unit.unit=='Gallon':return 'gal.'
        if unit.unit=='Quart': return 'quart'   
        if unit.unit=='Pound':return 'lb'
        if unit.unit=='Kilogram': return 'kg' 
        if unit.unit=='Gram': return 'g'
        if unit.unit=='Ounce': return 'oz.'
        if unit.unit=='Billion/°P/Liter': return 'Billion/°P/l'
        if unit.unit=='Billion/°P/Gallon': return 'Billion/°P/gal.'
    
    
    def get_usage_key(self,v):
        for key,val in   self.hop_usage_dic.items():
            if val == v:
                return key
        return None  
    
      