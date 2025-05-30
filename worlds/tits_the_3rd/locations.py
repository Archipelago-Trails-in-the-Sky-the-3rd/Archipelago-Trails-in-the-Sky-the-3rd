"""This module represents location definitions for Trails in the Sky the 3rd"""
from typing import Callable, Dict, Optional, Set

from BaseClasses import CollectionState, MultiWorld, Location
from .names.location_name import LocationName
from .names.region_name import RegionName
from .names.item_name import ItemName

class TitsThe3rdLocation(Location):
    """Trails in the Sky the 3rd Location Definition"""
    game: str = "Trails in the Sky the 3rd"


def get_location_id(location_name: LocationName):
    if location_name not in location_table:
        raise Exception(f"{location_name} is not part of location list. Something went wrong?")
    return location_table[location_name]


def create_location(multiworld: MultiWorld, player: int, region_name: str, location_name: str, rule: Optional[Callable[[CollectionState], bool]] = None):
    """
    Create a location in the given region.

    Args:
        multiworld: The multiworld object.
        player: The player number.
        region_name: The name of the region to create the location in.
        location_name: The name of the location to create.
        rule: A rule to apply to the location.
    """
    region = multiworld.get_region(region_name, player)
    location = TitsThe3rdLocation(player, location_name, location_table[location_name], region)
    if rule:
        location.access_rule = rule
    region.locations.append(location)


def create_locations(multiworld: MultiWorld, player: int, spoiler_mode: bool = False):
    """
    Define AP locations for Trails in the Sky the 3rd.
    Assumes regions have already been created.

    Args:
        multiworld: The multiworld object.
        player: The player number.
    """
    if spoiler_mode:
        create_location(multiworld, player, RegionName.hermit_garden, LocationName.kevin_initial_weapon_spoiler)
        create_location(multiworld, player, RegionName.hermit_garden, LocationName.kevin_initial_armor_spoiler)
        create_location(multiworld, player, RegionName.hermit_garden, LocationName.kevin_initial_boots_spoiler)
        create_location(multiworld, player, RegionName.hermit_garden, LocationName.ries_initial_weapon_spoiler)
        create_location(multiworld, player, RegionName.hermit_garden, LocationName.ries_initial_armor_spoiler)
        create_location(multiworld, player, RegionName.hermit_garden, LocationName.ries_initial_boots_spoiler)
    else:
        create_location(multiworld, player, RegionName.hermit_garden, LocationName.kevin_initial_weapon)
        create_location(multiworld, player, RegionName.hermit_garden, LocationName.kevin_initial_armor)
        create_location(multiworld, player, RegionName.hermit_garden, LocationName.kevin_initial_boots)
        create_location(multiworld, player, RegionName.hermit_garden, LocationName.ries_initial_weapon)
        create_location(multiworld, player, RegionName.hermit_garden, LocationName.ries_initial_armor)
        create_location(multiworld, player, RegionName.hermit_garden, LocationName.ries_initial_boots)

    create_location(multiworld, player, RegionName.lusitania, LocationName.lusitania_chest_bedroom_beside_banquet)
    create_location(multiworld, player, RegionName.lusitania, LocationName.lusitania_chest_bedroom_past_library)
    create_location(multiworld, player, RegionName.lusitania, LocationName.lusitania_chest_bedroom_past_casino_left)
    create_location(multiworld, player, RegionName.lusitania, LocationName.lusitania_chest_bedroom_past_casino_right)

    create_location(multiworld, player, RegionName.jade_corridor_start, LocationName.jade_corridor_chest_first_hall_straight_from_start)
    create_location(multiworld, player, RegionName.jade_corridor_start, LocationName.jade_corridor_chest_first_hall_elevated_platform)
    create_location(multiworld, player, RegionName.jade_corridor_start, LocationName.jade_corridor_chest_first_hall_before_first_warp)
    create_location(multiworld, player, RegionName.jade_corridor_start, LocationName.sealing_stone_jade_corridor_1_unlock)
    create_location(multiworld, player, RegionName.jade_corridor_start, LocationName.sealing_stone_arseille_unlock)
    if spoiler_mode:
        create_location(multiworld, player, RegionName.jade_corridor_start, LocationName.sealing_stone_tita_spoiler)
        create_location(multiworld, player, RegionName.jade_corridor_start, LocationName.tita_initial_weapon_spoiler)
        create_location(multiworld, player, RegionName.jade_corridor_start, LocationName.tita_initial_armor_spoiler)
        create_location(multiworld, player, RegionName.jade_corridor_start, LocationName.tita_initial_boots_spoiler)
        create_location(multiworld, player, RegionName.jade_corridor_start, LocationName.tita_orbment_item_1_spoiler)
        create_location(multiworld, player, RegionName.jade_corridor_start, LocationName.tita_orbment_item_2_spoiler)
        create_location(multiworld, player, RegionName.jade_corridor_start, LocationName.tita_orbment_item_3_spoiler)
        create_location(multiworld, player, RegionName.jade_corridor_start, LocationName.tita_orbment_item_4_spoiler)
    else:
        create_location(multiworld, player, RegionName.jade_corridor_start, LocationName.sealing_stone_tita)
        create_location(multiworld, player, RegionName.jade_corridor_start, LocationName.tita_initial_weapon)
        create_location(multiworld, player, RegionName.jade_corridor_start, LocationName.tita_initial_armor)
        create_location(multiworld, player, RegionName.jade_corridor_start, LocationName.tita_initial_boots)
        create_location(multiworld, player, RegionName.jade_corridor_start, LocationName.tita_orbment_item_1)
        create_location(multiworld, player, RegionName.jade_corridor_start, LocationName.tita_orbment_item_2)
        create_location(multiworld, player, RegionName.jade_corridor_start, LocationName.tita_orbment_item_3)
        create_location(multiworld, player, RegionName.jade_corridor_start, LocationName.tita_orbment_item_4)

    create_location(multiworld, player, RegionName.jade_corridor_expansion_area_1, LocationName.jade_corridor_chest_down_from_checkpoint_lowered_platform_second_chest)
    create_location(multiworld, player, RegionName.jade_corridor_expansion_area_1, LocationName.jade_corridor_chest_down_from_checkpoint_lowered_platform_third_chest)
    create_location(multiworld, player, RegionName.jade_corridor_expansion_area_1, LocationName.jade_corridor_chest_down_from_checkpoint_lowered_platform_first_chest)
    create_location(multiworld, player, RegionName.jade_corridor_expansion_area_1, LocationName.jade_corridor_chest_left_of_sun_door_one)
    create_location(multiworld, player, RegionName.jade_corridor_expansion_area_1, LocationName.jade_corridor_chest_right_of_sun_door_one)

    create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.jade_corridor_chest_arseille_deck)
    create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.jade_corridor_chest_arseille_confrence_room)
    create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.jade_corridor_chest_arseille_kitchen)
    create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.jade_corridor_chest_arseille_bedroom_one)
    create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.jade_corridor_chest_arseille_bedroom_two)
    create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.sealing_stone_jade_corridor_2_unlock)
    if spoiler_mode:
        create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.sealing_stone_julia_spoiler)
        create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.julia_initial_weapon_spoiler)
        create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.julia_initial_armor_spoiler)
        create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.julia_initial_boots_spoiler)
        create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.julia_orbment_item_1_spoiler)
        create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.julia_orbment_item_2_spoiler)
        create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.julia_orbment_item_3_spoiler)
        create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.julia_orbment_item_4_spoiler)
        create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.julia_orbment_item_5_spoiler)
        create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.julia_orbment_item_6_spoiler)
        create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.julia_orbment_item_7_spoiler)
    else:
        create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.sealing_stone_julia)
        create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.julia_initial_weapon)
        create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.julia_initial_armor)
        create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.julia_initial_boots)
        create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.julia_orbment_item_1)
        create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.julia_orbment_item_2)
        create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.julia_orbment_item_3)
        create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.julia_orbment_item_4)
        create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.julia_orbment_item_5)
        create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.julia_orbment_item_6)
        create_location(multiworld, player, RegionName.jade_corridor_arseille, LocationName.julia_orbment_item_7)

    create_location(multiworld, player, RegionName.jade_corridor_expansion_area_2, LocationName.jade_corridor_chest_left_from_checkpoint_first_chest)
    create_location(multiworld, player, RegionName.jade_corridor_expansion_area_2, LocationName.jade_corridor_chest_left_from_checkpoint_second_chest)
    create_location(multiworld, player, RegionName.jade_corridor_expansion_area_2, LocationName.jade_corridor_chest_left_from_checkpoint_third_chest)
    create_location(multiworld, player, RegionName.jade_corridor_expansion_area_2, LocationName.jade_corridor_chest_left_from_checkpoint_fourth_chest)
    create_location(multiworld, player, RegionName.jade_corridor_expansion_area_2, LocationName.chapter1_boss_defeated)


chapter_1_chests: Dict[str, int] = {
    LocationName.lusitania_chest_bedroom_beside_banquet: 9720,
    LocationName.lusitania_chest_bedroom_past_library: 9721,
    LocationName.lusitania_chest_bedroom_past_casino_left: 9722,
    LocationName.lusitania_chest_bedroom_past_casino_right: 9723,
    LocationName.jade_corridor_chest_first_hall_straight_from_start: 9857,
    LocationName.jade_corridor_chest_first_hall_elevated_platform: 9858,
    LocationName.jade_corridor_chest_first_hall_before_first_warp: 9859,
    LocationName.jade_corridor_chest_down_from_checkpoint_lowered_platform_second_chest: 9864,
    LocationName.jade_corridor_chest_down_from_checkpoint_lowered_platform_third_chest: 9865,
    LocationName.jade_corridor_chest_down_from_checkpoint_lowered_platform_first_chest: 9866,
    LocationName.jade_corridor_chest_left_of_sun_door_one: 9867,
    LocationName.jade_corridor_chest_right_of_sun_door_one: 9868,
    LocationName.jade_corridor_chest_arseille_deck: 9869,
    LocationName.jade_corridor_chest_arseille_confrence_room: 9872,
    LocationName.jade_corridor_chest_arseille_kitchen: 9873,
    LocationName.jade_corridor_chest_arseille_bedroom_one: 9874,
    LocationName.jade_corridor_chest_arseille_bedroom_two: 9875,
    LocationName.jade_corridor_chest_left_from_checkpoint_first_chest: 9880,
    LocationName.jade_corridor_chest_left_from_checkpoint_second_chest: 9881,
    LocationName.jade_corridor_chest_left_from_checkpoint_third_chest: 9884,
    LocationName.jade_corridor_chest_left_from_checkpoint_fourth_chest: 9885,
}

chapter_1_characters: Dict[str, int] = {
    # Sealing Stones
    LocationName.sealing_stone_jade_corridor_1_unlock: 2256,
    LocationName.sealing_stone_jade_corridor_2_unlock: 2257,
    LocationName.sealing_stone_arseille_unlock: 2258,
    LocationName.sealing_stone_tita: 9740,
    LocationName.sealing_stone_tita_spoiler: 9740,
    LocationName.sealing_stone_julia: 9753,
    LocationName.sealing_stone_julia_spoiler: 9753,
    # Kevin
    LocationName.kevin_initial_weapon: 1180,
    LocationName.kevin_initial_armor: 1181,
    LocationName.kevin_initial_boots: 1182,
    LocationName.kevin_initial_weapon_spoiler: 1180,
    LocationName.kevin_initial_armor_spoiler: 1181,
    LocationName.kevin_initial_boots_spoiler: 1182,
    # Ries
    LocationName.ries_initial_weapon: 1240,
    LocationName.ries_initial_armor: 1241,
    LocationName.ries_initial_boots: 1242,
    LocationName.ries_initial_weapon_spoiler: 1240,
    LocationName.ries_initial_armor_spoiler: 1241,
    LocationName.ries_initial_boots_spoiler: 1242,
    # Tita
    LocationName.tita_initial_weapon: 1160,
    LocationName.tita_initial_armor: 1161,
    LocationName.tita_initial_boots: 1162,
    LocationName.tita_orbment_item_1: 1163,
    LocationName.tita_orbment_item_2: 1164,
    LocationName.tita_orbment_item_3: 1165,
    LocationName.tita_orbment_item_4: 1166,
    LocationName.tita_initial_weapon_spoiler: 1160,
    LocationName.tita_initial_armor_spoiler: 1161,
    LocationName.tita_initial_boots_spoiler: 1162,
    LocationName.tita_orbment_item_1_spoiler: 1163,
    LocationName.tita_orbment_item_2_spoiler: 1164,
    LocationName.tita_orbment_item_3_spoiler: 1165,
    LocationName.tita_orbment_item_4_spoiler: 1166,
    # Julia
    LocationName.julia_initial_weapon: 1230,
    LocationName.julia_initial_armor: 1231,
    LocationName.julia_initial_boots: 1232,
    LocationName.julia_orbment_item_1: 1233,
    LocationName.julia_orbment_item_2: 1234,
    LocationName.julia_orbment_item_3: 1235,
    LocationName.julia_orbment_item_4: 1236,
    LocationName.julia_orbment_item_5: 1237,
    LocationName.julia_orbment_item_6: 1238,
    LocationName.julia_orbment_item_7: 1239,
    LocationName.julia_initial_weapon_spoiler: 1230,
    LocationName.julia_initial_armor_spoiler: 1231,
    LocationName.julia_initial_boots_spoiler: 1232,
    LocationName.julia_orbment_item_1_spoiler: 1233,
    LocationName.julia_orbment_item_2_spoiler: 1234,
    LocationName.julia_orbment_item_3_spoiler: 1235,
    LocationName.julia_orbment_item_4_spoiler: 1236,
    LocationName.julia_orbment_item_5_spoiler: 1237,
    LocationName.julia_orbment_item_6_spoiler: 1238,
    LocationName.julia_orbment_item_7_spoiler: 1239,
}

boss_locations: Dict[str, int] = {
    LocationName.chapter1_boss_defeated: 9757,
}


location_table: Dict[str, int] = {
    **chapter_1_chests,
    **chapter_1_characters,
    **boss_locations,
}

location_groups: Dict[str, Set[str]] = {}

default_sealing_stone_quartz = {
    # Tita
    LocationName.tita_orbment_item_1: ItemName.ep_cut_2,
    LocationName.tita_orbment_item_2: ItemName.attack_1,
    LocationName.tita_orbment_item_3: ItemName.eagle_eye,
    LocationName.tita_orbment_item_4: ItemName.hp_1,
    # Julia
    LocationName.julia_orbment_item_1: ItemName.ep_cut_2,
    LocationName.julia_orbment_item_2: ItemName.action_1,
    LocationName.julia_orbment_item_3: ItemName.hit_1,
    LocationName.julia_orbment_item_4: ItemName.range_1,
    LocationName.julia_orbment_item_5: ItemName.move_1,
    LocationName.julia_orbment_item_6: ItemName.attack_1,
    LocationName.julia_orbment_item_7: ItemName.shield_1,
}
