import json
import os

input_file = os.path.join("exports", "pathbuilder_export.json")
output_folder = "script_output"


class Character:
    def __init__(self, name):
        self.name = name
        self.attribs = []
        self.abilities = []

    def __repr__(self):
        padding = 15
        string = self.name + "\n"
        for key in self.attribs:
            string += str(key.get("name") + ":").ljust(padding)
            string += str(key.get("current")) + "\n"

        for key in self.abilities:
            string += str(key.get("name") + ":").ljust(padding)
            string += str(key.get("current")) + "\n"

        return string

    def add_attribute(self, key, value):
        self.attribs.append({"name": key, "current": value, "max": "", "id": ""})

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


def import_pathbuilder(data):
    d = data["build"]
    c = Character(d["name"])

    # combine ancestry with heritage without duplicating or omitting race
    heritage = modify_heritage(d["ancestry"], d["heritage"])

    keys = [
        ["age", d["age"]],
        ["alignment", d["alignment"]],
        ["ancestry_heritage", heritage],
        ["background", d["background"]],
        ["class", d["class"]],
        ["deity", d["deity"]],
        ["gender_pronouns", d["gender"]],
        ["languages", ", ".join(d["languages"])],
        ["level", d["level"]],
        ["size", d["sizeName"]],
    ]

    # pathbuilder exports style: ['abilities']['str'] = 20
    # roll20 imports
    #       strength = 20
    #       strength_score = "20"
    #       strength_modifier = 5

    # this key is also present but doesn't appear to be necessary
    #       strength_ability_check_modifier = ""

    abilities = [
        "strength",
        "dexterity",
        "constitution",
        "intelligence",
        "wisdom",
        "charisma",
    ]

    for ability in abilities:
        abbr = ability[:3]
        score = d["abilities"][abbr]
        mod = (score - 10) // 2

        # I have triple-checked and yes, it really does require all three
        keys.append([ability, score])
        keys.append([ability + "_score", score])
        keys.append([ability + "_modifier", mod])

    for k, v in keys:
        c.add_attribute(k, v)

    return c


def modify_heritage(ancestry, heritage):
    # Half-Elves and Half-Orc humans won't append "Human" but a Half-Orc Elf will
    if "Half-" in heritage and ancestry == "Human":
        return heritage

    # "Skilled Heritage" becomes simply "Skilled"  (Human is added in next step)
    if "Heritage" in heritage:
        heritage = heritage.replace("Heritage", "").strip()

    # "Ancient-Blooded" + "Dwarf" becomes "Ancient-Blooded Dwarf"
    # but "Ancient Elf" + "Elf" does NOT become "Ancient Elf Elf" :)
    if ancestry not in heritage:
        heritage += " " + ancestry

    return heritage


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
    try:
        data = json.load(open(input_file))
        character = import_pathbuilder(data)

    except Exception as e:
        print("Exception occurred during data import:", e)
        quit()

    character.export()

    print("\nProgram Finished.")
