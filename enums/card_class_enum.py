#!/usr/bin/python3

# Imports
from enum import Enum

# Class
class CardClass(Enum):
    """
    Represents the different hero classes available in the game.

    Each class corresponds to a specific type of hero and determines 
    which cards a player can use in their deck.
    """
    DRUID = "Druid"
    HUNTER = "Hunter"
    MAGE = "Mage"
    PALADIN = "Paladin"
    PRIEST = "Priest"
    ROGUE = "Rogue"
    SHAMAN = "Shaman"
    WARLOCK = "Warlock"
    WARRIOR = "Warrior"
    DEMON_HUNTER = "Demon Hunter"
    DEATH_KNIGHT = "Death Knight"
    NEUTRAL = "Neutral"
