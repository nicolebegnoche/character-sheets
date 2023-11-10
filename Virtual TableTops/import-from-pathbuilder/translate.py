import os
import json
import string


import_file = 'dev\\tulie_pathbuilder.json'
# import_file = "pathbuilder_export.json"
output_folder = "output"

sheet_options = [
    ("query_roll_critical_damage_dice", "0"),
    ("query_roll_damage_dice", "0"),
    ("alchemy_toggle", "0"),
    ("alchemy_toggle_infused", "0"),
    ("alchemy_toggle_research_field", "0"),
    ("roll_option_critical_damage", "none"),
    ("roll_show_notes", "[[1]]"),
]

class PathbuilderCharacter:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def get(self, attribute):
        return getattr(self, attribute)


class Roll20Character:
    def __init__(self, name=""):
        self.name = name
        self.avatar = ""
        self.tags = []
        self.controlledby = ""
        self.inplayerjournals = ""
        self.attribs = []
        self.abilities = []

    def __repr__(self):
        out = [("name", self.name)]
        out += [(x['name'], x['current']) for x in self.attribs] 
        return '\n'.join([f'{x}: {y}' for x,y in out])

    def add_attribute(self, key, value):
        self.attribs.append(Roll20Character.format_key(key,value))

    def format_key(key, value):
        return {"name":key,"current":value,"max":"","id":""}

    def export(self):
        # these keys are on the same level as character
        data = {"schema_version": 3, "type": "character"}
        data.update({"character": vars(self)})
        for k,v in sheet_options: self.add_attribute(k,v)
        out = json.dumps(data, indent=4)
        filepath = os.path.join(output_folder,self.name + ".json")
        with open(filepath, "w") as file:
            file.write(out)
        print(out)

if __name__ == '__main__':
    import_data = json.load(open(import_file))['build']

    p = PathbuilderCharacter(**import_data)
    r = Roll20Character(p.name)

    if p.ancestry not in p.heritage:
        p.heritage += " " + p.ancestry

    ## keys that already match
    for attribute in ["class", "level", "background", "age", "alignment", "deity"]:
        r.add_attribute(attribute, p.get(attribute))

    # MATCH KEYS
    matched_keys = [
        ("size", p.sizeName),
        ("gender_pronouns", p.gender),
        ("ancestry_heritage", p.heritage),
        ("repeating_languages_-NirukZNpIxz7uPQnfbZ_language", ', '.join(p.languages))
    ]


    # r.export()

    # print('\nProcess Finished.')