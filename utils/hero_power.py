#!/usr/bin/python3

# Imports
from enum import Enum

# Enum Imports
from utils.hero_class_enum import HeroClass

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
    DAGGER_MASTER = "Dagger Mastery"  # Rogue: Equip a 1/2 dagger.
    TOTEMIC_CALL = "Totemic Call"  # Shaman: Summon a random totem.
    LIFE_TAP = "Life Tap"  # Warlock: Draw a card and take 2 damage.
    DEMON_CLAWS = "Demon Claws"  # Demon Hunter: Gain 1 attack.

HERO_CLASS_TO_POWER = {
    HeroClass.MAGE: HeroPower.FIREBLAST,
    HeroClass.WARRIOR: HeroPower.ARMOR_UP,
    HeroClass.DRUID: HeroPower.SHAPESHIFT,
    HeroClass.HUNTER: HeroPower.STEADY_SHOT,
    HeroClass.PALADIN: HeroPower.REINFORCE,
    HeroClass.PRIEST: HeroPower.LESSER_HEAL,
    HeroClass.ROGUE: HeroPower.DAGGER_MASTER,
    HeroClass.SHAMAN: HeroPower.TOTEMIC_CALL,
    HeroClass.WARLOCK: HeroPower.LIFE_TAP,
    HeroClass.DEMON_HUNTER: HeroPower.DEMON_CLAWS,
}
