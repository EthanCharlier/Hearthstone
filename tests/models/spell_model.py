#!/usr/bin/python3

# Imports

# Modules Imports
from modules.spell_mod import Spell

# Enum Imports
from enums.card_type_enum import CardType
from enums.rarity_enum import Rarity

# Script
def create_spell_by_model(data: dict) -> Spell:
    spell = Spell(
        id = data["id"],
        name = data["name"],
        cost = data["cost"],
        description = data["description"],
        card_type = CardType[data["card_type"]],
        card_rarity = Rarity[data["card_rarity"]],
        effects = data["effects"]
    )
    return spell
