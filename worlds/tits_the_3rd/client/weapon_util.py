import os
import json
from functools import lru_cache
from worlds.tits_the_3rd.tables.location_list import location_id_to_name
from worlds.tits_the_3rd.names.item_name import ItemName
from worlds.tits_the_3rd.items import character_name_to_id, item_id_to_name
from worlds.tits_the_3rd.tables.location_list import location_table
from worlds.tits_the_3rd.names.region_name import RegionName

region_name_scena_flag = {
    RegionName.jade_corridor_start: 12400,
    RegionName.night_grancel_south: 12401,
    RegionName.golden_road: 274
}

def _has_user_of_weapon(memory_io, location_name):
    weapon_to_user_mapping = {
        "rapier": [ItemName.kloe, ItemName.julia],
        "gun": [ItemName.olivier, ItemName.josette],
        "greatsword": [ItemName.agate, ItemName.mueller],
        "katana": [ItemName.richard, ItemName.anelace],
        "staff": [ItemName.estelle],
        "whip": [ItemName.scherazard],
        "twinswords": [ItemName.joshua],
        "orbal cannon": [ItemName.tita],
        "gauntlets": [ItemName.zin],
        "crossbow": [ItemName.kevin],
        "templar sword": [ItemName.ries],
        "scythe": [ItemName.renne]
    }
    weapon_users = None
    for weapon, users in weapon_to_user_mapping.items():
        if location_name.lower().startswith(weapon.lower()):
            weapon_users = users
    weapon_users = [character_name_to_id[user] for user in weapon_users]
    for character_id in weapon_users:
        if memory_io.has_character(character_id):
            return True
    return False

def _has_unlock_location(memory_io, location_name):
    location_data = location_table[location_name]
    scena_flag = region_name_scena_flag[location_data.region]
    return memory_io.read_flag(scena_flag)


def has_weapon_unlock_conditions(memory_io, location_id):
    location_name = location_id_to_name[location_id]
    return (
        _has_user_of_weapon(memory_io, location_name) and
        _has_unlock_location(memory_io, location_name)
    )

@lru_cache(maxsize=None)
def get_weapon_progression_mapping():
    weapon_progression_mapping = json.load(open(
        os.path.join(os.path.dirname(__file__), "../tables/weapon_tier_to_id_list.json")
    ))
    return weapon_progression_mapping

def get_weapon_item_id_and_quantity(item_id, num_already_recieved):
    item_name = item_id_to_name[item_id].replace("Progressive ", "")
    weapon_progression_mapping = get_weapon_progression_mapping()
    progression = None
    for weapon, weapon_progression in weapon_progression_mapping.items():
        if item_name.lower().startswith(weapon.lower()):
            progression = weapon_progression
            break
    order_of_items = []
    for key in sorted(progression.keys(), key=int):
        order_of_items.extend(progression[key])
    item_id = order_of_items[num_already_recieved + 1]
    quantity = 1
    if item_name.lower().startswith("rapier") or item_name.lower().startswith("gun") or \
            item_name.lower().startswith("katana") or item_name.lower().startswith("greatsword"):
        quantity = 2
    return item_id, quantity
