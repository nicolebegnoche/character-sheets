import os
import json

input_type = "Pathbuilder"
input_file = os.path.join("input", "pathbuilder_export.json")
output_folder = "output"

sheet_options = {
    "query_roll_critical_damage_dice":  0,
    "query_roll_damage_dice":           0,
    "alchemy_toggle":                   0,
    "alchemy_toggle_infused":           0,
    "alchemy_toggle_research_field":    0,
    "roll_option_critical_damage":      None,
    "roll_show_notes":                  "[[1]]",
}

class Character:
    def __repr__(self):
        out = [f"{x}: {y}" for x, y in vars(self).items()]
        return "\n".join(out)

    def export(self):
        # this code is specific to roll20
        if self.ancestry not in self.heritage:
            self.heritage += " " + self.ancestry

        data = {
            "schema_version": 3,
            "type": "character",
            "character": {
                "name": self.name,
                "avatar": "",
                "tags": "[]",
                "controlledby": "",
                "inplayerjournals": "",
                "attribs": [],
                "abilities": [],
            },
        }
        keys_to_add = {
            "ancestry_heritage":    self.heritage,
            "deity":                self.deity,
            "class":                self.class_,
            "background":           self.background,
            "size":                 self.size,
            "alignment":            self.alignment,
            "level":                self.level,
            "languages":            self.languages,
            "age":                  self.age,
            "gender_pronouns":      self.gender,
        }
        keys_to_add.update(sheet_options)

        # roll20 import needs every key to be in this format 
        for k,v in keys_to_add.items():
            key = {"name":k,"current":v,"id":"","max":""}
            data['character']['attribs'].append(key)

        write_to_json(data)



def import_pathbuilder(data):
    d = data["build"]
    x = Character()
    x.name = d["name"]
    x.ancestry = d["ancestry"]
    x.heritage = d["heritage"]
    x.deity = d["deity"]
    x.class_ = d["class"]
    x.background = d["background"]
    x.size = d["sizeName"]
    x.alignment = d["alignment"]
    x.level = d["level"]
    x.languages = d["languages"]
    x.age = d["age"]
    x.gender = d["gender"]
    return x


def write_to_json(data):
    name = data['character']['name']
    filename = name.replace(" ", "") + ".json"
    output_file = os.path.join(output_folder, filename)

    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        json.dump(data, open(output_file, "w"), indent=4)
    
    except Exception as e:
        print("Exception occured while saving file: ", e)
        quit() 
    


if __name__ == "__main__":
    try:
        data = json.load(open(input_file))
        character = import_pathbuilder(data)

    except Exception as e:
        print("Exception occurred during data import:", e)
        quit()

    character.export()
    print("\nProgram Finished.")