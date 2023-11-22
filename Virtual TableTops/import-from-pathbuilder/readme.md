Developing a script to parse a json export from [Pathbuilder](https://pathbuilder2e.com/app.html) to match the fields on [Roll20's Pathfinder 2nd Edition](https://roll20.net/pathfinder2) character sheet.

#### Progress:
🗸 &nbsp; Creates a file with the bare minimum information needed for import  
🗸 &nbsp; imports certain settings  
🗸 &nbsp; imports basic text fields <sub>(name, ancestry, deity, class, background, size, alignment, level, languages, age, gender)</sub>
🗸 &nbsp; imports ability scores

---
#### unexpected to-do:  
- [ ] write script to combine data from stat block export and json export [(details)](input/export_from_pathbuilder/readme.md)

---

#### To do - requires coordinating and calculating multiple fields:
- [ ] class dc
- [ ] speed
- [ ] weapon proficiencies
- [ ] armor class
- [ ] saving throws
- [ ] skills
- [x] hit points    <small>*(minor to-dos left)*</small>
- [ ] perception

#### To do - "repeating" sections:
- [ ] lores
- [ ] class abilities
- [ ] feats
- [ ] weapon strikes <sub>(stretch goal)</sub>
- [ ] resistances & immunities <sub>(stretch)</sub>

#### stretch goals:
- [ ] spells  <sub>(***very*** stretch; this might need to be a separate project)</sub>
- [ ] actions
- [ ] pets
- [ ] alchemist tab
- [ ] inventory <sub>(maybe)</sub>