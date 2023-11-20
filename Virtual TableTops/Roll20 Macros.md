*Note:*  Ending curly braces ``}`` in Roll20 macros need to be escaped as html entities ``&#125`` when nested.  Saving these as macros will convert the html entities to  braces, so you will need to replace *all* of the code if you wish to make changes.




### Pathfinder 2nd Edition
<hr />

#### Treat Wounds  
A drop-down menu allows you to choose which level of Treat Wounds you wish to perform, gives the appropriate DC, and rolls the dice for every possible outcome.

<code>?{Choose a DC for Treat Wounds
|
DC 15 - Trained,
&{template:default&#125;{{name=Treat Wounds - Trained &#125;&#125;  {{Medicine (+@{medicine}) = [[d20+@{medicine}]] vs **DC 15** &#125;&#125; {{Success=Target gains [[2d8]] hit points &#125;&#125; {{Critical Success=Target gains [[2d8]] additional hit points &#125;&#125; {{Critical Failure=Target takes [[1d8]] damage &#125;&#125;
|
DC 20 - Expert,
&{template:default&#125;{{name=Treat Wounds - Expert &#125;&#125;  {{Medicine (+@{medicine}) = [[d20+@{medicine}]] vs **DC 20** &#125;&#125; {{Success=Target gains [[2d8+10]] hit points &#125;&#125; {{Critical Success=Target gains [[2d8]] additional hit points &#125;&#125; {{Critical Failure=Target takes [[1d8]] damage &#125;&#125; 
|
DC 30 - Master,
&{template:default&#125;{{name=Treat Wounds - Master &#125;&#125;  {{Medicine (+@{medicine}) = [[d20+@{medicine}]] vs **DC 30** &#125;&#125; {{Success=Target gains [[2d8+30]] hit points &#125;&#125; {{Critical Success=Target gains [[2d8]] additional hit points &#125;&#125; {{Critical Failure=Target takes [[1d8]] damage &#125;&#125; 
|
DC 40 - Legendary,
&{template:default&#125;{{name=Treat Wounds - Legendary &#125;&#125;  {{Medicine (+@{medicine}) = [[d20+@{medicine}]] vs **DC 40** &#125;&#125; {{Success=Target gains [[2d8+50]] hit points &#125;&#125; {{Critical Success=Target gains [[2d8]] additional hit points &#125;&#125; {{Critical Failure=Target takes [[1d8]] damage &#125;&#125; 
}
</code>

// Optional Additions

``*Add +5 hit points if the target has [Godless Healing](https://2e.aonprd.com/Feats.aspx?ID=869)*``

``*[Mortal Healing](https://2e.aonprd.com/Feats.aspx?ID=1181): A success becomes a critical success if treated outside of combat and the patient has not regained hit points from divine magic in the past 24 hours.*``