"""
This module servies as an entrypoint into the Trails in the Sky the 3rd AP world.
"""
from typing import ClassVar, Dict, Set

from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, launch_subprocess, Type
from worlds.tits_the_3rd.names.item_name import ItemName
from worlds.tits_the_3rd.names.location_name import LocationName
from .items import default_item_pool, item_data_table, item_groups, item_table, TitsThe3rdItem, TitsThe3rdItemData, character_table, filler_items
from .locations import create_locations, location_groups, location_table
from .options import TitsThe3rdOptions
from .regions import create_regions, connect_regions
from .settings import TitsThe3rdSettings
from .web import TitsThe3rdWeb

def launch_client():
    """Launch a Trails in the Sky the 3rd client instance"""
    from worlds.tits_the_3rd.client.client import launch
    launch_subprocess(launch, name="TitsThe3rdClient")

components.append(Component(
    "Trails in the Sky the 3rd Client",
    "TitsThe3rdClient",
    func=launch_client,
    component_type=Type.CLIENT
))

class TitsThe3rdWorld(World):
    """
    Trails in the Sky the 3rd is a JRPG from the "Trails of" / "Kiseki" series,
    released in 2007 and developed by Nihon Falcom. Embark on an emotional rollercoaster
    following Father Kevin Graham and Ries Argent during their journey to escape the
    mysterious dimension of Phantasma. It is highly recommended to pick up the first two
    games before playing this one, Trails in the Sky FC / SC.
    """
    game: str = "Trails in the Sky the 3rd"
    options_dataclass = TitsThe3rdOptions
    options: TitsThe3rdOptions
    topology_present: bool = True
    settings: ClassVar[TitsThe3rdSettings]
    web: WebWorld = TitsThe3rdWeb()
    base_id: int = 1954308624560

    item_name_groups: Dict[str, Set[str]] = item_groups
    location_name_groups: Dict[str, Set[str]] = location_groups
    item_name_to_id: Dict[str, int] = item_table
    location_name_to_id: Dict[str, int] = location_table

    def create_item(self, name: str) -> TitsThe3rdItem:
        """Create a Trails in the Sky the 3rd item for this player"""
        data: TitsThe3rdItemData = item_data_table[name]
        return TitsThe3rdItem(name, data.classification, data.code, self.player)

    def create_event(self, name: str) -> TitsThe3rdItem:
        """Create a Trails in the Sky the 3rd event for this player"""
        return TitsThe3rdItem(name, True, None, self.player)

    def create_regions(self) -> None:
        """Define regions and locations for Trails in the Sky the 3rd AP"""
        create_regions(self.multiworld, self.player)
        connect_regions(self.multiworld, self.player)
        create_locations(self.multiworld, self.player)

    def create_items(self) -> None:
        """Define items for Trails in the Sky the 3rd AP"""
        for item_name, quantity in default_item_pool.items():
            for _ in range(quantity):
                self.multiworld.itempool.append(self.create_item(item_name))

    def set_rules(self) -> None:
        """Set remaining rules."""
        self.multiworld.completion_condition[self.player] = lambda _: True

    def pre_fill(self):
        # For now hard code beating Bennu as victory
        victory_item = self.create_item(ItemName.bennu_defeat)
        self.multiworld.get_location(LocationName.chapter1_boss_defeated, self.player).place_locked_item(victory_item)

        # Randomize starting characters here
        # TODO: Maybe add some options regarding this
        character_list = list(character_table.keys())
        self.multiworld.random.shuffle(character_list)
        for _ in range(2):
            character_item = self.create_item(character_list.pop())
            self.push_precollected(character_item)
        # Put the rest into item pool
        for character in character_list:
            character_item = self.create_item(character)
            self.multiworld.itempool.append(character_item)
        # Generate fillers to put into item pool
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        self.multiworld.itempool += [self.create_filler() for _ in range(total_locations - len(self.multiworld.itempool))]

    def get_filler_item_name(self):
        filler_item_name = self.multiworld.random.choice(filler_items)

        # TODO: Maybe add more logic here

        return filler_item_name
