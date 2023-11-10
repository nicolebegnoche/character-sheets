from collections import OrderedDict
import json
from pprint import pprint

import_file = "pathbuilder.json"
output_file = "roll20.json"

class Character:
    def __init__(self):
        # bare keys needed under "character"
        self.name = "name"
        self.avatar = ""
        self.tags = "[]"
        self.controlledby = ""
        self.inplayerjournals = ""
        self.attribs = []
        self.abilities = []

    def to_dict(self):
        return vars(self)

    def __repr__(self):
        return "\n".join([f"{x[0]} : {x[1]}" for x in vars(self).items()])


def main():
    x = Character()
    export_roll20(x)


def export_roll20(character: Character = None, filepath: str = None) -> dict:
    # these keys are on the same level as character (eg:  {item:value, item:value, Character object})
    data = OrderedDict({"schema_version": 3, "type": "character"})
    data.update({"character": character.to_dict()})

    # these need to be added to [character][attribs]
    sheet_options = [
        ("query_roll_critical_damage_dice", "0"),
        ("query_roll_damage_dice", "0"),
        ("alchemy_toggle", "0"),
        ("alchemy_toggle_infused", "0"),
        ("alchemy_toggle_research_field", "0"),
        ("roll_option_critical_damage", "none"),
        ("roll_show_notes", "[[1]]"),
    ]
    for x, y in sheet_options:
        key = {"name":x,"current":y,"max":"","id":""}
        data['character']['attribs'].append(key)

    with open(output_file, "w") as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    main()
    print("\nProcess Finished.")