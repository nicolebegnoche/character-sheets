#! ..\..\..\..\venv\scripts\python.exe
import os, json
from bs4 import BeautifulSoup
import re

json_file = "export_as_json.json"
stat_block_file = "export_as_stat_block.html"





# json = json.load(open(json_file))["build"]


def qprint(list):
    print('type', type(list), end=' ')

    try: print('of', type(list[0]), end=' ')
    except Exception: pass
    
    try: print('length', len(list), end=' ')
    except Exception: pass

    print('\n')

    if type(list) is str:
        print(list)
        return

     
    try: 
        for item in list:
            item = re.sub('\n', '', str(item))
            item = re.sub(' +', ' ', str(item))
            print(item, '\n\n')
    except:
        try:
            print(item)
        except Exception as e:
            print('\nNot a string, not iterable, and doesn\'t like to print.')
            print('\nError message:', e)




def main():
    # get statblock content
    html = BeautifulSoup(open(stat_block_file), "html.parser").body

    # print(html)
    # print(html.prettify())

    div = html.div

    contents = div.children


    def lam(x):
        x = str(x)
        x = re.sub('\n|\t', '', x)
        x = re.sub(' +', ' ', x)
        return x

    string = ' '.join([lam(x) for x in contents])
    lines = string.split('<br/>')
    qprint(string)

    languages = ''
    links = {
        "spells"    : '',
        "recipes"   : '',
        'feats'     : '',
        'specials'  : '',
    }

    # b = html.find_all('b')
    # for x in b:
    #     print(x, '\n')



    # for x in b: 
    #     x = re.sub('\n', '', str(x))
    #     x = re.sub(' +', ' ', x) 
    #     print(x)

    # print(html.prettify())


if __name__ == '__main__':
    main()
    print('\nProcess Finished.')






#  custom language names

#  text for class abilities

#  links for spells

#  links for formulae / recipes

#  links for feats

#  links for special abilities

"""
<b>Languages</b> Common, Elven, Kitsune, Ekujae Shape-Script, Sylvan<br/>

<b>Clue In</b> <b>Frequency</b> once per 10 minutes<br/><b>Trigger</b> Another creature attempts a check to investigate a lead you're pursuing. You share information with the triggering creature. They gain a circumstance bonus to their check equal to your circumstance bonus to checks investigating your subject from Pursue a Lead. The GM can add any relevant traits to this reaction depending on the situation, such as auditory and linguistic if you're conveying information verbally. <hr/><b>Speed</b> 35 feet<br/><b>Melee</b> +1 Striking Rapier +14 (Deadly d8, Disarm, Finesse, Magical), <b>Damage</b> 2d6 P +2d6<sup><span class="superscript-damage color-precision">Precision</span></sup><br/><b>Ranged</b> +1 Striking Justice +14 (Deadly d10, Magical), <b>Damage</b> 2d6 P +1d4<sup><span class="superscript-damage">Good</span></sup> +2d6<sup><span class="superscript-damage color-precision">Precision</span></sup><br/>

<b>Quick Tincture</b>  (Investigator, Manipulate) <b>Cost</b> 1 versatile vial<br/><b>Requirements</b> You know the formula for the alchemical item you're creating, you are holding or wearing alchemist's tools, and you have a free hand.<br/>You quickly brew up a short-lived tincture. You create a single alchemical elixir or tool of your level or lower without having to spend the normal monetary cost in alchemical reagents or needing to attempt a Crafting check. This item has the infused trait, but it remains potent only until the end of the current turn.<br/>

<b>Devise a Stratagem</b>  (Concentrate, Fortune, Investigator) <b>Frequency</b> once per round<br/>You assess a foe's weaknesses in combat and use them to formulate a plan of attack against your enemy. Choose a creature you can see and roll a d20. If you Strike the chosen creature later this round, you must use the result of the roll you made to Devise a Stratagem for your Strike's attack roll instead of rolling. You make this substitution only for the first Strike you make against the creature this round, not any subsequent attacks.<br/><br/>When you make this substitution, you can also add your Intelligence modifier to your attack roll instead of your Strength or Dexterity modifier, provided your Strike uses an agile or finesse melee weapon, an agile or finesse unarmed attack, a ranged weapon (which must be agile or finesse if it's a melee weapon with the thrown trait), or a sap. <br/><br/>If you're aware that the creature you choose is the subject of a lead you're pursuing, you can use this ability as a free action.<br/><b>Precision Damage</b> Strategic Strike 2d6<br/>

<b>Arcane Prepared Spells</b> DC 21, attack +11; 

<b>Cantrips</b> <a href="https://2e.aonprd.com/Spells.aspx?ID=3">Acid Splash</a>, <a href="https://2e.aonprd.com/Spells.aspx?ID=1261">Ancient Dust</a><br/>

<b>Arcane Innate Spells</b> DC 17, attack +7; 

<b>Cantrips</b> <a href="https://2e.aonprd.com/Spells.aspx?ID=66">Detect Magic</a><br/>

<b>Formula Book</b> <a href="https://2e.aonprd.com/Equipment.aspx?ID=80">Antidote (Lesser)</a>, <a href="https://2e.aonprd.com/Equipment.aspx?ID=844">Bookthief Brew</a>, <a href="https://2e.aonprd.com/Equipment.aspx?ID=77">Frost Vial (Lesser)</a><br/>

<b>Additional Feats</b> <a href="https://2e.aonprd.com/Feats.aspx?ID=750">Additional Lore</a>, <a href="https://2e.aonprd.com/Feats.aspx?ID=752">Alchemical Crafting</a>, <a href="https://2e.aonprd.com/Feats.aspx?ID=3905">Ambush Tactics</a>, <a href="https://2e.aonprd.com/Feats.aspx?ID=754">Arcane Sense</a>, <a href="https://2e.aonprd.com/Feats.aspx?ID=2119">Criminal Connections</a>, <a href="https://2e.aonprd.com/Archetypes.aspx?ID=85">Detective Dedication</a>, <a href="http://2e.aonprd.com/Feats.aspx?ID=14">Elven Weapon Familiarity</a>, <a href="https://2e.aonprd.com/Feats.aspx?ID=780">Experienced Tracker</a>, <a href="https://2e.aonprd.com/Feats.aspx">Eyes of the City</a>, <a href="https://2e.aonprd.com/Feats.aspx?ID=604">Familiar</a>, <a href="https://2e.aonprd.com/Feats.aspx?ID=786">Forager</a>, <a href="https://2e.aonprd.com/Feats.aspx?ID=2129">Glean Contents</a>, <a href="https://2e.aonprd.com/Feats.aspx?ID=1447">Known Weaknesses</a>, <a href="https://2e.aonprd.com/Feats.aspx?ID=811">Lie to Me</a>, <a href="http://2e.aonprd.com/Feats.aspx?ID=16">Nimble Elf</a>, <a href="https://2e.aonprd.com/Feats.aspx?ID=824">Quick Identification</a>, <a href="https://2e.aonprd.com/Feats.aspx?ID=1454">Shared Stratagem</a>, <a href="https://2e.aonprd.com/Feats.aspx?ID=846">Streetwise</a>, <a href="https://2e.aonprd.com/Feats.aspx?ID=852">Terrain Stalker</a>, <a href="https://2e.aonprd.com/Feats.aspx?ID=2154">Thorough Search</a>, <a href="https://2e.aonprd.com/Feats.aspx?ID=1451">Underworld Investigator</a>, <a href="https://2e.aonprd.com/Archetypes.aspx?ID=12">Wizard Dedication</a>, <a href="http://2e.aonprd.com/Heritages.aspx?Ancestry=2">Woodland Elf</a><br/>

<b>Additional Specials</b> <a href="https://2e.aonprd.com/Classes.aspx?ID=12">Arcane School</a>, <a href="https://2e.aonprd.com/Classes.aspx?ID=13">Keen Recollection</a>, <a href="https://2e.aonprd.com/Classes.aspx?ID=13">Methodology (Alchemical Sciences)</a>, <a href="https://2e.aonprd.com/Classes.aspx?ID=13">On the Case</a>, <a href="https://2e.aonprd.com/Classes.aspx?ID=13">Pursue a Lead</a>, <a href="https://2e.aonprd.com/Classes.aspx?ID=13">Skillful Lessons</a>, <a href="https://2e.aonprd.com/Classes.aspx?ID=13">Strategic Strike</a>, <a href="https://2e.aonprd.com/">Terrain Stalker (Underbrush)</a>, <a href="https://2e.aonprd.com/">Wizard Archetype Arcane School (Universalist)</a> </div> """
