#!/usr/bin/python3

# Imports

# Modules Imports
from modules.spell_mod import Spell

# Enum Imports
from enums.card_class_enum import CardClass
from enums.card_type_enum import CardType
from enums.rarity_enum import Rarity

# Script
def create_spell_by_model(data: dict) -> Spell:
    """
    Create a Spell object from a dictionary model.

    Args:
        data (dict): A dictionary containing all necessary fields to create a Spell.

    Returns:
        Spell: An instance of the Spell class.
    """
    spell = Spell(
        id = data["id"],
        name = data["name"],
        cost = data["cost"],
        description = data["description"],
        card_classes=[CardClass[cls] for cls in data["card_classes"]],
        card_type = CardType[data["card_type"]],
        card_rarity = Rarity[data["card_rarity"]],
        effects = data["effects"]
    )
    return spell
