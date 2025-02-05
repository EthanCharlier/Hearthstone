#!/usr/bin/python3

# Imports
from enum import Enum

# Enum Imports
from enums.card_class_enum import CardClass

# Class
class HeroPower(Enum):
    """
    Represents the different hero powers available in the game.

    Each hero power is unique to a specific hero class and provides a special ability 
    that can be used during gameplay.
    """
    FIREBLAST = "Fireblast"
    ARMOR_UP = "Armor Up!"
    SHAPESHIFT = "Shapeshift"
    STEADY_SHOT = "Steady Shot"
    REINFORCE = "Reinforce"
    LESSER_HEAL = "Lesser Heal"
    DAGGER_MASTERY = "Dagger Mastery"
    TOTEMIC_CALL = "Totemic Call"
    LIFE_TAP = "Life Tap"
    DEMON_CLAWS = "Demon Claws"

HERO_CLASS_TO_POWER = {
    CardClass.MAGE: HeroPower.FIREBLAST,
    CardClass.WARRIOR: HeroPower.ARMOR_UP,
    CardClass.DRUID: HeroPower.SHAPESHIFT,
    CardClass.HUNTER: HeroPower.STEADY_SHOT,
    CardClass.PALADIN: HeroPower.REINFORCE,
    CardClass.PRIEST: HeroPower.LESSER_HEAL,
    CardClass.ROGUE: HeroPower.DAGGER_MASTERY,
    CardClass.SHAMAN: HeroPower.TOTEMIC_CALL,
    CardClass.WARLOCK: HeroPower.LIFE_TAP,
    CardClass.DEMON_HUNTER: HeroPower.DEMON_CLAWS,
}
