#!/usr/bin/python3

# Imports
from enum import Enum

# Class
class Race(Enum):
    """
    Represents the different races available in the game.

    Some cards belong to specific races, which may affect gameplay interactions, synergies, 
    and special abilities.
    """
    DRAENEI = "Draenei"
    ORC = "Orc"
    UNDEAD = "Undead"
    MURLOC = "Murloc"
    DEMON = "Demon"
    MECH = "Mech"
    ELEMENTAL = "Elemental"
    BEAST = "Beast"
    TOTEM = "Totem"
    PIRATE = "Pirate"
    DRAGON = "Dragon"
    ALL = "All"
    QUILBOAR = "Quilboar"
    NAGA = "Naga"
    HUMAN = "Human"
