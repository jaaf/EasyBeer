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
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from gen import HelpWindowUI

class HelpWindow(QWidget,HelpWindowUI.Ui_Form ):
    '''
    classdocs
    '''

    def __init__(self):
        
        QWidget.__init__(self) 
        self.setupUi(self)
        
    def showEvent(self,event):
        print ('display help text')
        
        self.close_button.setText('Close')
        self.text_edit.setHtml(self.tr('''<h1>Welcome to EasyBeer. What you should definitely read about this software?</h1>    
<h2>Introduction</h2>
<p>This is a very quick help as the dialogs are self explanatory.</p>

<p>EasyBeer consists of a main dialog that opens as soon as you launch the application,
 and a series of dialogs that help you to prepare a beer brewing session.</p>
 
 <p>A brewing session is the implementation of a recipe on an equipment. Thus, the recipe and the equipment have to
 to be declared and defined in the relevant dialogs prior to using them in the brewing session.</p>
 
 <p>Attention of the reader is drawn to the fact that a recipe is not based on malt quantities but on malt percentages.
 The quantities for a given batch volume are calculated in the brewing session according to the batch volume declared in the session.</p>

<p>Various dialogs can be opened from the menu in the main window. The main window 
is where you prepare a brewing session. Nevertheless, you cannot prepare a brewing 
session as long as you have not declared at least
one equipment and one recipe. Moreover, to declare a recipe, you must have created a 
database for all your ingredients, malts, hops, adjuncts and yeasts.</p>

<p>It is a good starting point to use the dialogs that permit you to create these
 databases even if you only put one or two items into them. As you will see soon, 
 it is rather simple.</p>
 <p>In other word, to use this software you should proceed in the following order:
 <ol>
 <li>Use the Database dialogs to declare your malts, hops, yeasts, etc.</li>
 <li>Use the Database dialogs to declare your equipments</li>
 <li>Use the Database dialogs to declare your recipes</li>
 <li>Use the main window to create a brewing session that is the implementation of a recipe on a given equipment.</li>
 
 </ol>

<h2>Basic Principles in Dialogs</h2>

In the dialogs, the field to display or to enter values have different colors. A distinction is made between:
<ol>
<li>Inputs to fill</li>
<li>Calculated values </li>
<li>Read only values</li>
</ol>
<p>The colors for each category can be set using the Preferences menu.</p>



<p>In addition:</p>
<ul>
<li>Question mark buttons open a contextual explanatory window</li>
<li>Some inputs may have a tool tip you make appear hovering it</li>
</ul>

<h2>Opening the database dialogs</h2>
Dialogs for storing ingredients, recipes and equipments into the database can be opened using the Database menu entry in the main window.
<ul>
<li>Database -> Edit Malt Database for Malt Dialog</li>
<li>Database -> Edit Hop Database for Hop Dialog</li>
<li>Database -> Edit Yeast Database for Yeast Dialog</li>
<li>Database -> Edit Recipe Database for Recipe Dialog</li>
<li>Database -> Edit Equipment Database for Equipment Database</li>

</ul>
<h2>In what recipes declared in EasyBeer are different from other recipes</h2>
<p>Recipes in EasyBeer are designed a bit differently from recipes you can find on the Internet</p>
<p>In general, recipes are based on quantities to make a given batch volume. In EasyBeer, recipes are based on percentages. That means that these recipes
do not correspond to any volume. Volumes are declared in the brewing session when you implement the recipe on an equipment. Quantities are then calculated
accordingly.</p>
<p>Whenever you find a recipe on the Internet, you have to convert quantities in percentage to use it in EasyBeer. For example, if the recipe says:</p>
<ul>
<li> 6 kg of malt1</li>
<li> 1 kg of malt2</li>
</ul>
<p>you should declar:</p>
<ul>
<li> 6/7 = 86 % of malt11</li>
<li> 1/7 = 14 % of malt11</li>
</ul>

<p>Be sure that the total of percentages is 100, otherwise you will no be allowed to save the recipe.</p>
<p>A recipe also defines the hops to use and the targeted bitterness. In the main window,
 while preparing the brewing session, you can adjust the amounts and see which level
  of bitterness you achieve with this values.
</p>

<p>For yeast you only declare which yeast to use and the recommended pitching rate. 
In the main window, while preparing the brewing session, the recommended amount is 
calculated based on the batch size and the targeted original gravity.
 You can change the amount and see what pitching rate it corresponds to.
</p>

<p>Once you have defined your brewing session, you can save it in the database. Later on
you will be able to enter the results you have achieved such as the actual original 
gravity and the different volumes. This inputs are only informative and for memory.</p>

<h2>Brewing Session Sheet</h2>
<p>Once you have recorded a brewing session, you can print a Session Sheet to accompany you during the actual making of the beer.</p>

<p>Start by selection a session in the main window. Then use the button View the Session Sheet or the right side of the session selector. This will open 
a navigator in the system that will show the sheet. Just use the print facility of the navigator to print your sheet.</p>


 <h2>Translating EasyBeer in other languages</h2>
 <p>The graphical interface of EasyBeer can be translated in various languages.
 If you are interested in translating the interface for your language, ask the developer for the .ts file. This kind of file can be translated, directly with a text editor,
  or in a more comfortable way.
 if your can run the Qt-Linguist software</p>
 <p>You can get in touch with the developer at jaaf64@zoraldia.com</p>
  ''')    )
  
      