import json
import os

input_file = os.path.join("exports", "pathbuilder_export.json")
output_folder = "script_output"

# this global variable does not change after being populated
data = {}


class Character:
    def __init__(self, data):
        self.name = data["name"]
        self.attribs = []
        self.abilities = []

    def __repr__(self):
        padding = 25
        string = self.name + "\n"
       
        for key in self.attribs + self.abilities:
            string += str(key.get("name") + ":").ljust(padding)
            string += str(key.get("current")) + "\n"  
        return string

    def add(self, list_of_keys, target_list=None):
        target = self.abilities if target_list == "abilities" else self.attribs
        for key, value in list_of_keys:
            target.append({"name": key, "current": value, "max": "", "id": ""})

    def export(self):
        export = {
            "schema_version": 3,
            "type": "character",
            "character": {
                "name": self.name,
                "avatar": "",
                "tags": "[]",
                "controlledby": "",
                "inplayerjournals": "",
                "attribs": self.attribs,
                "abilities": self.abilities,
            },
        }
        write_to_json(export)


def main():
    global data
    data = read_json(input_file)["build"]
    character = Character(data)

    # simple values that require no work to import  (name, deity, class, background, size, alignment, level, age, gender)
    character.add(basics())

    # combine ancestry and heritage without duplicating or omitting ancestry
    character.add(heritage())

    character.add(ability_scores())
    # character.add(hit_points())
    # character.add(armor_class())
    # character.add(saving_throws())
    # character.add(skills())
    # character.add(speed())
    # character.add(weapon_proficiencies())
    # character.add(class_dc())
    # character.add(perception())

    # write to file
    character.export()
    print(character)


def basics():
    """Import simple fields that require minimal conversion"""

    matching_names = ["age", "alignment", "background", "class", "deity", "level"]
    keys = [[x, data[x]] for x in matching_names]

    keys.extend(
        [
            ["size", data["sizeName"]],
            ["gender_pronouns", data["gender"]],
            ["languages", ", ".join(data["languages"])],
        ]
    )
    return keys

def heritage():
    """Combine ancestry and heritage observing the following rules:

    Include the race name if absent but do not allow it to be duplicated
        'Elf' and 'Ancient Elf' returns 'Ancient Elf'
        'Dwarf' and 'Ancient-Blooded' returns 'Ancient-Blooded Dwarf'

    For mixed ancestries, the heritage should not include 'human' but should include any other race
        'Human' and 'Half-Elf' returns 'Half-Elf'
        'Tiefling' and 'Half-Elf' returns 'Half-Elf Tiefling'
    """
    ancestry = data["ancestry"]
    heritage = data["heritage"]
    if ancestry not in heritage:
        if not (ancestry == "Human" and "Half" in heritage):
            heritage += " " + ancestry
    return [["ancestry_heritage", heritage]]

def ability_scores():
    # pathbuilder exports style: ['abilities']['str'] = 20
    # roll20 imports
    #       strength = 20
    #       strength_score = '20'
    #       strength_modifier = 5
    # this key is also present but doesn't appear to be necessary
    #       strength_ability_check_modifier = ''
    abilities = [
        "strength",
        "dexterity",
        "constitution",
        "intelligence",
        "wisdom",
        "charisma",
    ]
    keys = []
    for ability in abilities:
        abbr = ability[:3]
        score = data["abilities"][abbr]
        mod = (score - 10) // 2

        # I have triple-checked and yes, it really does require all three
        keys.append([ability, score])
        keys.append([ability + "_score", score])
        keys.append([ability + "_modifier", mod])
    return keys


def read_json(file):
    if not os.path.exists(file):
        print(f'File "{file}" does not exist.')
        quit()
    else:
        try:
            return json.load(open(input_file))
        except Exception as e:
            print("Exception occurred during data import:", e)
            quit()

def write_to_json(data):
    name = data["character"]["name"]
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
    main()
    print("\nProgram Finished.")
