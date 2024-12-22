#!/usr/bin/python3

# Imports
from enum import Enum

# Enum Imports
from enums.card_class_enum import CardClass

# Class
class HeroPower(Enum):
    """
    """
    FIREBLAST = "Fireblast"  # Mage: Deal 1 damage.
    ARMOR_UP = "Armor Up!"  # Warrior: Gain 2 armor.
    SHAPESHIFT = "Shapeshift"  # Druid: Gain 1 attack and 1 armor.
    STEADY_SHOT = "Steady Shot"  # Hunter: Deal 2 damage to enemy hero.
    REINFORCE = "Reinforce"  # Paladin: Summon a 1/1 Silver Hand Recruit.
    LESSER_HEAL = "Lesser Heal"  # Priest: Restore 2 health.
    DAGGER_MASTERY = "Dagger Mastery"  # Rogue: Equip a 1/2 dagger.
    TOTEMIC_CALL = "Totemic Call"  # Shaman: Summon a random totem.
    LIFE_TAP = "Life Tap"  # Warlock: Draw a card and take 2 damage.
    DEMON_CLAWS = "Demon Claws"  # Demon Hunter: Gain 1 attack.

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
