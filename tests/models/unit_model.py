#!/usr/bin/python3

# Imports

# Modules Imports
from modules.unit_mod import Unit

# Enum Imports
from enums.card_class_enum import CardClass
from enums.card_type_enum import CardType
from enums.rarity_enum import Rarity
from enums.race_enum import Race

# Script
def create_unit_by_model(data: dict) -> Unit:
    """
    Create a Unit object from a dictionary model.

    Args:
        data (dict): A dictionary containing all necessary fields to create a Unit.

    Returns:
        Unit: An instance of the Unit class.
    """
    unit = Unit(
        id = data["id"],
        name = data["name"],
        cost = data["cost"],
        description = data["description"],
        card_classes=[CardClass[cls] for cls in data["card_classes"]],
        card_type = CardType[data["card_type"]],
        card_rarity = Rarity[data["card_rarity"]],
        unit_race = Race[data["unit_race"]],
        attack = data["attack"],
        health = data["health"],
        armor = data["armor"],
        effects = data["effects"]
    )
    return unit
