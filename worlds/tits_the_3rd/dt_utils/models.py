from dataclasses import dataclass
from enum import Enum
from typing import Optional


class WeaponType(Enum):
    STAFF = 1
    TWINSWORDS = 2
    WHIP = 3
    GUN = 4
    RAPIER = 5
    GREATSWORD = 6
    ORBALCANNON = 7
    GAUNTLETS = 8
    CROSSBOW = 9
    KATANA = 10
    TEMPLARSWORD = 11
    SCYTHE = 12


class IconType(Enum):
    STAFF = 1
    TWINSWORDS = 2
    WHIP = 3
    GUN = 4
    RAPIER = 5
    GREATSWORD = 6
    ORBALCANNON = 7
    GAUNTLETS = 8
    CROSSBOW = 9
    KATANA = 11
    TEMPLARSWORD = 28
    SCYTHE = 30


class TargetType(Enum):
    WALK_SINGLE_TARGET = 1
    WALK_AOE = 2


@dataclass
class Weapon:
    item_id: int
    weapon_type: WeaponType
    name: str
    desc: str

    strength: int
    defence: int = 0
    arts: int = 0
    art_defence: int = 0
    dexterity: int = 0
    agility: int = 0
    move: int = 0
    speed: int = 0
    attack_range: int = 1
    aoe_size: int = 1

    inventory_limit: int = 99
    sell_price: int = 0

    target_type: Optional[TargetType] = None
    icon_type: Optional[IconType] = None

    def __post_init__(self):
        # Default target_type based on weapon_type
        if self.target_type is None:
            if self.weapon_type == WeaponType.ORBALCANNON:
                self.target_type = TargetType.WALK_AOE
            else:
                self.target_type = TargetType.WALK_SINGLE_TARGET

        # Default icon_type to match weapon_type name
        if self.icon_type is None:
            self.icon_type = IconType[self.weapon_type.name]
