"""This module represents item definitions for Trails in the Sky the 3rd"""

import itertools
from typing import Dict, List, NamedTuple, Optional, Set

from .names.item_name import ItemName
from BaseClasses import Item, ItemClassification


class TitsThe3rdItem(Item):
    """Trails in the Sky the 3rd Item Definition"""

    game: str = "Trails in the Sky the 3rd"

    def __init__(self, name, classification: ItemClassification, code: Optional[int], player: int):
        super(TitsThe3rdItem, self).__init__(name, classification, code, player)


class TitsThe3rdItemData(NamedTuple):
    """Trails in the Sky the 3rd Item Data"""

    code: int
    classification: ItemClassification


def get_item_id(item_name: ItemName):
    if item_name not in item_data_table:
        raise Exception(f"{item_name} is not part of location list. Something went wrong?")
    return item_data_table[item_name].code

meta_data_table: Dict[str, TitsThe3rdItemData] = {
    ItemName.mira_min_id: TitsThe3rdItemData(100000, ItemClassification.filler),
    ItemName.mira_max_id: TitsThe3rdItemData(199999, ItemClassification.filler),
    ItemName.lower_elements_sepith_min_id: TitsThe3rdItemData(300000, ItemClassification.filler),
    ItemName.lower_elements_sepith_max_id: TitsThe3rdItemData(300999, ItemClassification.filler),
    ItemName.higher_elements_sepith_min_id: TitsThe3rdItemData(350000, ItemClassification.filler),
    ItemName.higher_elements_sepith_max_id: TitsThe3rdItemData(350999, ItemClassification.filler),
    ItemName.character_min_id: TitsThe3rdItemData(70000, ItemClassification.filler),
    ItemName.character_max_id: TitsThe3rdItemData(71000, ItemClassification.filler),
    ItemName.location_min_id: TitsThe3rdItemData(200000, ItemClassification.filler),
    ItemName.location_max_id: TitsThe3rdItemData(299999, ItemClassification.filler),
}

consumable_table: Dict[str, TitsThe3rdItemData] = {
    ItemName.extra_spicy_fries: TitsThe3rdItemData(408, ItemClassification.filler),
    ItemName.fresh_water: TitsThe3rdItemData(411, ItemClassification.filler),
    ItemName.fishy_finale: TitsThe3rdItemData(437, ItemClassification.filler),
    ItemName.tear_balm: TitsThe3rdItemData(501, ItemClassification.filler),
    ItemName.teara_balm: TitsThe3rdItemData(502, ItemClassification.filler),
    ItemName.reviving_balm: TitsThe3rdItemData(508, ItemClassification.filler),
    ItemName.ep_charge: TitsThe3rdItemData(510, ItemClassification.filler),
    ItemName.smelling_salts: TitsThe3rdItemData(512, ItemClassification.filler),
}

recipe_table: Dict[str, TitsThe3rdItemData] = {
    ItemName.easy_paella_recipe: TitsThe3rdItemData(10000, ItemClassification.filler),
}

equipment_table: Dict[str, TitsThe3rdItemData] = {
    ItemName.royal_spikes: TitsThe3rdItemData(102, ItemClassification.useful),
    ItemName.black_bangle: TitsThe3rdItemData(356, ItemClassification.useful),
    ItemName.glam_choker: TitsThe3rdItemData(358, ItemClassification.useful),
}

quartz_table: Dict[str, TitsThe3rdItemData] = {
    ItemName.hit_2: TitsThe3rdItemData(619, ItemClassification.useful),
    ItemName.information: TitsThe3rdItemData(657, ItemClassification.useful),
}

currency_table: Dict[str, TitsThe3rdItemData] = {
    # Mira
    ItemName.mira_300: TitsThe3rdItemData(meta_data_table[ItemName.mira_min_id].code + 300, ItemClassification.filler),
    ItemName.mira_500: TitsThe3rdItemData(meta_data_table[ItemName.mira_min_id].code + 500, ItemClassification.filler),
    ItemName.mira_1000: TitsThe3rdItemData(meta_data_table[ItemName.mira_min_id].code + 1000, ItemClassification.filler),
    ItemName.mira_5000: TitsThe3rdItemData(meta_data_table[ItemName.mira_min_id].code + 5000, ItemClassification.filler),
    ItemName.mira_10000: TitsThe3rdItemData(meta_data_table[ItemName.mira_min_id].code + 10000, ItemClassification.filler),
    # Low Sepith
    ItemName.lower_elements_sepith_50: TitsThe3rdItemData(meta_data_table[ItemName.lower_elements_sepith_min_id].code + 50, ItemClassification.filler),
    ItemName.lower_elements_sepith_100: TitsThe3rdItemData(meta_data_table[ItemName.lower_elements_sepith_min_id].code + 100, ItemClassification.filler),
    ItemName.lower_elements_sepith_250: TitsThe3rdItemData(meta_data_table[ItemName.lower_elements_sepith_min_id].code + 250, ItemClassification.filler),
    ItemName.lower_elements_sepith_500: TitsThe3rdItemData(meta_data_table[ItemName.lower_elements_sepith_min_id].code + 500, ItemClassification.filler),
    # High Sepith
    ItemName.higher_elements_sepith_50: TitsThe3rdItemData(meta_data_table[ItemName.higher_elements_sepith_min_id].code + 50, ItemClassification.filler),
    ItemName.higher_elements_sepith_100: TitsThe3rdItemData(meta_data_table[ItemName.higher_elements_sepith_min_id].code + 100, ItemClassification.filler),
    ItemName.higher_elements_sepith_250: TitsThe3rdItemData(meta_data_table[ItemName.higher_elements_sepith_min_id].code + 250, ItemClassification.filler),
    ItemName.higher_elements_sepith_500: TitsThe3rdItemData(meta_data_table[ItemName.higher_elements_sepith_min_id].code + 500, ItemClassification.filler),
}

character_table: Dict[str, TitsThe3rdItemData] = {
    ItemName.kevin: TitsThe3rdItemData(meta_data_table[ItemName.character_min_id].code + 8, ItemClassification.progression),
    ItemName.ries: TitsThe3rdItemData(meta_data_table[ItemName.character_min_id].code + 14, ItemClassification.progression),
    ItemName.tita: TitsThe3rdItemData(meta_data_table[ItemName.character_min_id].code + 6, ItemClassification.progression),
    ItemName.julia: TitsThe3rdItemData(meta_data_table[ItemName.character_min_id].code + 13, ItemClassification.progression),
}

location_unlock_table: Dict[str, TitsThe3rdItemData] = {  # Item ID is 200000 + flag number
    ItemName.jade_corridor_unlock_1: TitsThe3rdItemData(meta_data_table[ItemName.location_min_id].code + 256, ItemClassification.progression),
    ItemName.jade_corridor_unlock_2: TitsThe3rdItemData(meta_data_table[ItemName.location_min_id].code + 257, ItemClassification.progression),
    ItemName.jade_corridor_arseille_unlock: TitsThe3rdItemData(meta_data_table[ItemName.location_min_id].code + 258, ItemClassification.progression),
}

key_item_table: Dict[str, TitsThe3rdItemData] = {ItemName.bennu_defeat: TitsThe3rdItemData(500000, ItemClassification.progression)}


item_data_table: Dict[str, TitsThe3rdItemData] = {
    **consumable_table,
    **recipe_table,
    **equipment_table,
    **quartz_table,
    **currency_table,
    **key_item_table,
    **character_table,
    **location_unlock_table,
    **meta_data_table,
}

item_groups: Dict[str, Set[str]] = {
    "Consumables": set(consumable_table.keys()),
    "Recipes": set(recipe_table.keys()),
    "Equipment": set(equipment_table.keys()),
    "Quartz": set(quartz_table.keys()),
    "Currency": set(currency_table.keys()),
    "Characters": set(character_table.keys()),
    "Location Unlock": set(location_unlock_table.keys()),
}

filler_items: List[str] = list(
    itertools.chain(
        item_groups["Consumables"],
        item_groups["Currency"],
        item_groups["Equipment"],
        item_groups["Quartz"],
    )
)

item_table: Dict[str, int] = {name: data.code for name, data in item_data_table.items()}

default_item_pool: Dict[str, int] = {
    # ItemName.easy_paella_recipe: 1,
    ItemName.jade_corridor_unlock_1: 1,
    ItemName.jade_corridor_unlock_2: 1,
    ItemName.jade_corridor_arseille_unlock: 1,
}
