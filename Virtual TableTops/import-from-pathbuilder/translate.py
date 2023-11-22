import json
import os

input_file = os.path.join('exports', 'pathbuilder_export.json')
output_folder = 'script_output'

abilities = {
    'str': 'strength',
    'dex': 'dexterity',
    'con': 'constitution',
    'int': 'intelligence',
    'wis': 'wisdom',
    'cha': 'charisma',
}

# this global variable does not change after being populated
data = {}


class Character:
    def __init__(self, data):
        self.name = data['name']
        self.attribs = []
        self.abilities = []

    def __repr__(self):
        padding = 25
        string = self.name + '\n'

        for key in self.attribs + self.abilities:
            string += str(key.get('name') + ':').ljust(padding)
            string += str(key.get('current')) + '\n'
        return string

    def add(self, list_of_keys, target_list=None):
        target = self.abilities if target_list == 'abilities' else self.attribs
        for key, value in list_of_keys:
            target.append({'name': key, 'current': value, 'max': '', 'id': ''})

    def export(self):
        export = {
            'schema_version': 3,
            'type': 'character',
            'character': {
                'name': self.name,
                'avatar': '',
                'tags': '[]',
                'controlledby': '',
                'inplayerjournals': '',
                'attribs': self.attribs,
                'abilities': self.abilities,
            },
        }
        write_to_json(export)


def main():
    global data
    data = read_json(input_file)['build']
    character = Character(data)

    # import scores but also capture for later use
    character.add(scores := ability_scores())
    modifiers = dict(zip(abilities.keys(), [y for x, y in scores if 'mod' in x]))

    character.add(basics())
    character.add(heritage())
    character.add(speed())
    character.add(hit_points(modifiers['con']))
    character.add(class_dc(modifiers))
    # character.add(armor_class(modifiers['dex']))
    # character.add(saving_throws(modifiers))
    # character.add(skills(modifiers))
    # character.add(weapon_proficiencies(modifiers))
    # character.add(perception(modifiers))

    # write to file
    character.export()
    print(character)


def ability_scores():
    # pathbuilder exports style: ['abilities']['str'] = 20
    # roll20 imports:
    #       strength = 20
    #       strength_score = '20'
    #       strength_modifier = 5

    # this key is also present but doesn't appear to be necessary
    #       strength_ability_check_modifier = ''

    keys = []
    for abbr, ability_name in abilities.items():
        score = data['abilities'][abbr]
        mod = (score - 10) // 2

        # I have triple-checked and yes, it really does require all three
        keys.append([ability_name, score])
        keys.append([ability_name + '_score', score])
        keys.append([ability_name + '_modifier', mod])
    return keys


def basics():
    """Import simple fields that require minimal conversion"""

    matching_names = ['age', 'alignment', 'background', 'class', 'deity', 'level']
    keys = [[x, data[x]] for x in matching_names]

    # TODO: possibly break down speed into base + bonus with a note explaining where the bonus comes from 

    keys.extend(
        [
            ['size', data['sizeName']],
            ['gender_pronouns', data['gender']],
            ['languages', ', '.join(data['languages'])],
        ]
    )
    return keys


def class_dc(scores):
    """Import minimum keys to calculate class dc. """

    # Required keys:
    #   class_dc_rank                     8   (which would be legendary)
    #   class_dc_key_ability_select       @{strength_modifier}

    # These keys exist but do not appear to be required
    #   class_dc                         22 (total score)
    #   class_dc_key_ability             2  (str modifier)            
    #   class_dc_proficiency             13 (level + training)
    #   class_dc_proficiency_display    'L'

    stat = abilities[data['keyability']]
    return [
        ['class_dc_key_ability_select', '@{' + stat + '_modifier}'],
        ['class_dc_rank', data['proficiencies']['classDC']],
    ]


def heritage():
    """Combine ancestry and heritage observing the following rules:

    Include the race name if absent but do not allow it to be duplicated
        'Elf' and 'Ancient Elf' returns 'Ancient Elf'
        'Dwarf' and 'Ancient-Blooded' returns 'Ancient-Blooded Dwarf'

    For mixed ancestries, the heritage should not include 'human' but should include any other race
        'Human' and 'Half-Elf' returns 'Half-Elf'
        'Tiefling' and 'Half-Elf' returns 'Half-Elf Tiefling'
    """
    ancestry = data['ancestry']
    heritage = data['heritage']
    if ancestry not in heritage:
        if not (ancestry == 'Human' and 'Half' in heritage):
            heritage += ' ' + ancestry
    return [['ancestry_heritage', heritage]]


def hit_points(con):
    # TODO:  compare total_hp against value in stat_block.html
    # TODO:  find the pathbuilder keys that correspond with:    hit_points_item,  hit_points_other

    level = data['level']
    class_ = data['attributes']['classhp']
    bonus = data['attributes']['bonushpPerLevel']
    race = data['attributes']['ancestryhp']
    total_hp = level * (class_ + con + bonus) + race

    return [
        ['hit_points', total_hp],
        ['hit_points_ancestry', race],
        ['hit_points_class', class_],
    ]


def speed():
    """Calculate speed"""

    # TODO: separate speed into base + bonus with note explaining where they come from
    #       keys are  speed_status_bonus, speed_item_bonus, speed_circumstance_bonus, and speed_notes
    #       for each bonus, there's another field of the same name for penalties
    speed_total = data['attributes']['speed'] + data['attributes']['speedBonus']
    return [['speed_base', speed_total]]

def read_json(file):
    if not os.path.exists(file):
        print(f'File \'{file}\' does not exist.')
        quit()
    else:
        try:
            return json.load(open(input_file))
        except Exception as e:
            print('Exception occurred while trying to read file:', e)
            quit()

def write_to_json(data):
    name = data['character']['name']
    filename = name.replace(' ', '') + '.json'
    output_file = os.path.join(output_folder, filename)

    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        json.dump(data, open(output_file, 'w'), indent=4)
    except Exception as e:
        print('Exception occured while saving file: ', e)
        quit()


if __name__ == '__main__':
    main()
    print('\nProgram Finished.')
