#!/usr/bin/python3

# Imports
from enum import Enum

# Class
class Rarity(Enum):
    """
    Represents the different rarity levels for cards in the game.

    Cards are classified by rarity, which influences their power and availability in the game.
    """
    COMMON = "Common"
    FREE = "Free"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"
