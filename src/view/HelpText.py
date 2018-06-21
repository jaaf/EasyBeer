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

ACID_REST='''
<h2>Acid Rest</h2>
<p>This kind of rest in not used nowadays, because the same result – i.e. lowering the mash ph – can 
be achieved otherwise.</p>

<h2>It is intended to acidify the mash when using pale malts. The recommended temperature range is 
<strong>30° — 52°C (86 — 126°F)</strong>.
<p>At these temperature the phytase enzymes break down phytin nto phosphates and myo-inositol (vitamin).</p>

<p>The phosphates react with calcium and magnesium to form insoluble phosphates compounds releasing 2
hydrogen ions that lower the mash ph.</p>

'''

DOUGHING-IN='''
<h2>Doughing-in</h2>
A short rest at temperature between 35 and 45°C (95 to 113°C) helps to liquefy the mash but 
it is considered optional and having more negative effect than positive when using well modified 
malts.
Indeed, long fatty acids can be oxidized producing undesirable flavors in the beer afterwards.

'''

BETA-GLUCANASE_REST='''
<h2>Betaglucanase Rest</h2>
<p>This rest is recommended when using more than 20% of unmalted or flaked barley, oatmeal, rye or
 wheat in the grain bill as those last contain beta-glucans (non starch polysaccharides) that 
 are responsible for the stiffness of the mash.</p>
 
 <p>The recommended range for temperature is between 40 and 48°C (104 -118°F).
 When the percentage of unmalted adjuncts is between 10 and 20%, a mash-out rest may be used
 instead. </p>

'''

PROTEIN_REST='''
<h2>Protein Rest</h2>
<p>During malting and mashing, amino acids are cleaved from the peptides (amino acid chains)  by
specialized enzymes called 'proteolytic enzymes' – proteolysis being the breakdown of polypeptides 
into smaller ones.</p>
<p>Some of these enzymes cleave the large insoluble protein chains into smaller soluble protein which 
enhance the head retention of the beer but contribute to haze formation.</p>

<p>Other proteolytic enzyme remove amino acid from the ends of the protein chains to produce small 
peptides and individual amino acis that the yeast can use as nutrients.In fact, the enzyme do the 
greatest part of their job during malting.</p>

<p>Well modified malts do not require such a rest and a long – >30mn – protein rest at 50°C could
be counterproductive regarding foam stability and body.</p>

<p>This rest is used by craft brewer that want to take more control of the mashing process using
moderately modified malts or a proportion of unmalted adjunct more than 20%. 
In such a case a rest of 15-30mn at 50°C is used.
It can also be combined with a beta-glucanase rest:  30mn at 45-50°C (113-122°F)</p>
'''

SACCHARIFICATION_REST='''
<h2>Saccharification </h2>

<p>This kind of rest is the main event in the mashing process. It allows the conversion of starches
into fermentable sugars.</h«>

<p>Before explaining what happen during this rest let's present the various kind of sugar the wort
generally contains before fermentation.</p>
<ul>
<li><strong>Glucose:</strong> 10 to 15%. It is a monosaccharide that we will note G </li>
<li><strong>Fructose:</strong> 1 to 2%. It is a monosaccharid (isomer of G) that we will not F</li>
<li><strong>Sucrose:</strong> 1 to 2%.It is a disaccharide consisting of one G and one F bound together</li>
<li><strong>Maltose:</strong> 50 to 60%. It is a disaccharide consisting of 2 G</li>
<li><strong>Maltotriose:</strong> 15 to 20%. It a trisaccharide consisting of  3 G bound together</li>
<li><strong>Dextrins:</strong> 20 to 30%. They are larger suggars called oligosaccharides consisting
 of more than 3G. Dextrins are <strong>not fermentable</strong></li>
</ul>

<p>The enzymes involved in the  process of breaking down starches are called <strong>diastatic enzymes</strong>, each one having its own
capacity in breaking down the <strong>amyloses</strong> –  amyloses are single straight-chain starch molecules, typically hundreds or thousands of glucose
units long. The can even branch to each other forming very large molecules called <strong>amylopectines</strong>.</p>

<p>Let's review the diastatic enzymes and their temperature and ph range of effectiveness:</p>
<ul>
<li> <strong>Beta-amylases :</strong> 
   <ul>
        <li>PH active 5 — 6 *** PH preferred 5.4 — 5.5</li>
        <li>  Temp active 55 — 65 °C / 131 — 149 °F *** Temp preferred 55 — 65 °C / 131 — 149 °F</li>
       
    </ul>
    <p>Beta-amylases enzymes remove maltose chains (2G) only from the twig extremities of amylopectines not the root
    or the middle of the branch.
     They cannot get close to the branch joints.They stop working about 3G away from the branch joints.
     They leave behind amylopectines with small 3G branches that are called beta-amylase limit dextrin</p>
 </li>
<li> <strong>Alpha-amylases :</strong>
   <ul>
        <li>PH active 5 — 6 *** PH preferred 5.6 — 5.8</li>
        <li>  Temp active 60 — 75 °C / 140 — 176 °F *** Temp preferred 60 — 70 °C / 140 — 158 °F</li>
       
    </ul>
    <p>Alpha-amylases enzymes unlike beta-amylases can break the amylopectines anywhere. Thus they make smaller
    amylopectines that the beta-amylases can work on. Nevertheless they cannot get close to the branch joints. They stop a 1G 
    away from the branch joints letting behind alpha-amylases limit dextrin </p>

</li>
<li><strong>Limit dextrinases :</strong>
   <ul>
        <li>PH active 4.5 — 5.8 *** PH preferred 4.8 — 5.4</li>
        <li>  Temp active 60 — 67 °C / 140 — 153 °F *** Temp preferred 60 — 65 °C / 140 — 149 °F</li>
       
    </ul>
    <p>Limit-dextrinase enzymes can cut up the limit-dextrin into smaller chains letting behind unbranched chains that 
    can be used by alpha and beta-amylases to produce more glucose, maltose and maltotriose.  </p>
</li>
</ul>

<p>Practically :
<ul>
   <li>Temperatures 62 — 65 °C / 144 — 149 °F favor beta-amylases and are still in the optimal range of 
   limit dextrinases leading to beer with a <strong>light body</strong>.</li>
   <li>Temperature 68— 72 / 154 — 162 °F favor alpha-amylases but are no longer in the active range of 
   limit-dextrinases leading to a beer with a <strong>heavy body and less attenuated</strong>.</li>
   <li>Temperature in between produces a range of body and fermentability.</li>
</ul>

<p>Regarding the duration of this rest, it can vary between 30 and 60 mn depending of factors such as
mash ph (see optimal values for each category of enzymes), water to grain ratio and temperature.
To guaranty a high level of fermentability <strong>60 mn </strong> is the recommended duration.

'''