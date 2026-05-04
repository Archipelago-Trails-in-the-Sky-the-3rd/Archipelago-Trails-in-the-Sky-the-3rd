"""This module represents location definitions for Trails in the Sky the 3rd"""
from typing import Callable, Dict, Optional, Set
import json
import os

from BaseClasses import CollectionState, MultiWorld, Location
from .names.location_name import LocationName
from .names.item_name import ItemName
from .tables.location_list import (
    location_table,
    LocationData,
    estelle_craft_locations,
    joshua_craft_locations,
    scherazard_craft_locations,
    olivier_craft_locations,
    kloe_craft_locations,
    agate_craft_locations,
    tita_craft_locations,
    zin_craft_locations,
    kevin_craft_locations,
    anelace_craft_locations,
    josette_craft_locations,
    richard_craft_locations,
    mueller_craft_locations,
    julia_craft_locations,
    ries_craft_locations,
    renne_craft_locations
)
from .names.check_type_name import CheckTypeName
from .options import TitsThe3rdOptions, CraftPlacement
from .spoiler_mapping import scrub_spoiler_data

MIN_CRAFT_LOCATION_ID = 100000
MAX_CRAFT_LOCATION_ID = 100000 + 9999
MIN_WEAPON_UNLOCK_ID = 110000
MAX_WEAPON_UNLOCK_ID = 110000 + 9999

class TitsThe3rdLocation(Location):
    """Trails in the Sky the 3rd Location Definition"""
    game: str = "Trails in the Sky the 3rd"


def get_location_id(location_name: LocationName):
    """
    Get the location id for a given location name.
    """
    if location_name not in location_table:
        raise RuntimeError(f"{location_name} is not part of location list. Something went wrong?")
    return location_table[location_name].flag


def create_location(multiworld: MultiWorld, player: int, location_name: str, options: TitsThe3rdOptions, rule: Optional[Callable[[CollectionState], bool]] = None):
    """
    Create a location in accordance with the location table in location_list.py

    Args:
        multiworld: The multiworld object.
        player: The player number.
        location_name: The name of the location to create.
        rule: A rule to apply to the location.
    """
    region = multiworld.get_region(location_table[location_name].region, player)
    shown_location_name = location_name
    if options.name_spoiler_option:
        shown_location_name = scrub_spoiler_data(location_name)
    location = TitsThe3rdLocation(player, shown_location_name, location_table[location_name].flag, region)
    if rule:
        location.access_rule = rule
    region.locations.append(location)


def create_locations(multiworld: MultiWorld, player: int, options: TitsThe3rdOptions):
    """
    Define AP locations for Trails in the Sky the 3rd.
    Assumes regions have already been created.

    Args:
        multiworld: The multiworld object.
        player: The player number.
    """
    for location_name in location_table:
        location_data = location_table[location_name]
        rule = get_location_requirements(location_data, location_name, player, options)
        create_location(multiworld, player, location_name, options, rule)


def get_relevant_character_item_for_craft_location(location_name: str):
    name_to_item_mapping = {
        "joshua": ItemName.joshua,
        "estelle": ItemName.estelle,
        "scherazard": ItemName.scherazard,
        "olivier": ItemName.olivier,
        "kloe": ItemName.kloe,
        "agate": ItemName.agate,
        "tita": ItemName.tita,
        "zin": ItemName.zin,
        "kevin": ItemName.kevin,
        "anelace": ItemName.anelace,
        "josette": ItemName.josette,
        "richard": ItemName.richard,
        "mueller": ItemName.mueller,
        "julia": ItemName.julia,
        "ries": ItemName.ries,
        "renne": ItemName.renne
    }
    return name_to_item_mapping[location_name.split(" ")[0].lower()]

def get_character_items_which_use_weapon(location_name: str):
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
    for weapon, users in weapon_to_user_mapping.items():
        if location_name.lower().startswith(weapon.lower()):
            return users


def _get_num_progressive_weapons_required_for_tier(tier: int):
    weapon_name_to_item_name = {
        "scythe": ItemName.progressive_scythe,
        "rapier": ItemName.progressive_rapier,
        "gun": ItemName.progressive_gun,
        "greatsword": ItemName.progressive_greatsword,
        "katana": ItemName.progressive_katana,
        "staff": ItemName.progressive_staff,
        "whip": ItemName.progressive_whip,
        "twinswords": ItemName.progressive_twinswords,
        "orbal cannon": ItemName.progressive_orbal_cannon,
        "gauntlets": ItemName.progressive_gauntlets,
        "crossbow": ItemName.progressive_crossbow,
        "templar sword": ItemName.progressive_templar_sword
    }
    weapon_to_tier_mapping = json.load(open(os.path.join(os.path.dirname(__file__), "tables/weapon_tier_to_id_list.json")))
    num_progressive_weapons_required = {}
    for weapon_name, tier_to_id_list in weapon_to_tier_mapping.items():
        # subtract 1 for the base game weapon, which doesn't count towards the progressive weapon requirement
        num_progressive_weapons_required[weapon_name] = (sum(len(id_list) for tier_threshold, id_list in tier_to_id_list.items() if int(tier_threshold) <= tier)) - 1
    return num_progressive_weapons_required


boss_requirements = {
    LocationName.chapter1_boss_defeated: 2,
    LocationName.miniboss_grancel_arena: 3,
    LocationName.chapter2_boss_defeated: 3,
}

character_to_weapon = {
    ItemName.estelle: "staff",
    ItemName.joshua: "twinswords",
    ItemName.scherazard: "whip",
    ItemName.olivier: "gun",
    ItemName.kloe: "rapier",
    ItemName.agate: "greatsword",
    ItemName.tita: "orbal cannon",
    ItemName.zin: "gauntlets",
    ItemName.kevin: "crossbow",
    ItemName.anelace: "katana",
    ItemName.josette: "gun",
    ItemName.richard: "katana",
    ItemName.mueller: "greatsword",
    ItemName.julia: "rapier",
    ItemName.ries: "templar sword",
    ItemName.renne: "scythe"
}

weapon_to_progressive_weapon_mapping = {
    "scythe": ItemName.progressive_scythe,
    "rapier": ItemName.progressive_rapier,
    "gun": ItemName.progressive_gun,
    "greatsword": ItemName.progressive_greatsword,
    "katana": ItemName.progressive_katana,
    "staff": ItemName.progressive_staff,
    "whip": ItemName.progressive_whip,
    "twinswords": ItemName.progressive_twinswords,
    "orbal cannon": ItemName.progressive_orbal_cannon,
    "gauntlets": ItemName.progressive_gauntlets,
    "crossbow": ItemName.progressive_crossbow,
    "templar sword": ItemName.progressive_templar_sword
}

def _get_boss_requirements(location_name: str, player: int, options: TitsThe3rdOptions):
    if not options.weapon_shuffle.value:
        return None

    # Assert that the player has 4 characters with weapons that meet the standard for the boss's chapter.
    # E.g. For the chapter 1 boss, the player should logically have at least 4 characters
    # that each have a (base-game) jade-corridor level weapon.
    gear_tier_required = boss_requirements[location_name]
    num_progressive_weapons_for_tier = _get_num_progressive_weapons_required_for_tier(gear_tier_required)
    if options.name_spoiler_option:
        return lambda state, loc_name=location_name: sum(
            1 for character, weapon in character_to_weapon.items()
            if state.has(scrub_spoiler_data(character), player, 1) and
            state.has(scrub_spoiler_data(weapon_to_progressive_weapon_mapping[weapon]), player, num_progressive_weapons_for_tier[weapon])
        ) >= 4
    else:
        return lambda state, loc_name=location_name: sum(
            1 for character, weapon in character_to_weapon.items()
            if state.has(character, player, 1) and
            state.has(weapon_to_progressive_weapon_mapping[weapon], player, num_progressive_weapons_for_tier[weapon])
        ) >= 4

def get_location_requirements(location: LocationData, location_name: str, player: int, options: TitsThe3rdOptions):
    if location.check_type == CheckTypeName.craft and options.craft_placement == CraftPlacement.option_default and not options.craft_shuffle:
        return None
    if location.check_type == CheckTypeName.craft:
        character_item = get_relevant_character_item_for_craft_location(location_name)
        return lambda state, loc_name=location_name: \
            state.has(scrub_spoiler_data(character_item) if options.name_spoiler_option else character_item, player, 1)
    if location.check_type == CheckTypeName.weapon:
        character_items = get_character_items_which_use_weapon(location_name)
        return lambda state, loc_name=location_name: any(
            state.has(scrub_spoiler_data(character_item) if options.name_spoiler_option else character_item, player, 1)
            for character_item in character_items
        )
    if location.check_type == CheckTypeName.boss:
        return _get_boss_requirements(location_name, player, options)
    return None


location_groups: Dict[str, Set[str]] = {
    "Estelle Crafts": set(estelle_craft_locations.keys()),
    "Joshua Crafts": set(joshua_craft_locations.keys()),
    "Scherazard Crafts": set(scherazard_craft_locations.keys()),
    "Olivier Crafts": set(olivier_craft_locations.keys()),
    "Kloe Crafts": set(kloe_craft_locations.keys()),
    "Agate Crafts": set(agate_craft_locations.keys()),
    "Tita Crafts": set(tita_craft_locations.keys()),
    "Zin Crafts": set(zin_craft_locations.keys()),
    "Kevin Crafts": set(kevin_craft_locations.keys()),
    "Anelace Crafts": set(anelace_craft_locations.keys()),
    "Josette Crafts": set(josette_craft_locations.keys()),
    "Richard Crafts": set(richard_craft_locations.keys()),
    "Mueller Crafts": set(mueller_craft_locations.keys()),
    "Julia Crafts": set(julia_craft_locations.keys()),
    "Ries Crafts": set(ries_craft_locations.keys()),
    "Renne Crafts": set(renne_craft_locations.keys()),
}