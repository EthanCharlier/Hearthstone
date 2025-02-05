#!/usr/bin/python3

# Imports
from enum import Enum

# Class
class CardType(Enum):
    """
    Represents the different types of cards in the game.

    - UNIT: A card that represents a character or creature that can be placed on the board.
    - SPELL: A card that represents a magical effect or ability used during the game.
    """
    UNIT = "Unit"
    SPELL = "Spell"
