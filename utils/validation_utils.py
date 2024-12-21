#!/usr/bin/python3

# Imports

# Modules Imports
from models.hero_mod import Hero

# Enum Imports
from enums.hero_class_enum import HeroClass
from enums.hero_power_enum import HeroPower

# Script
def validate_hero(data: dict) -> bool:
    try:
        Hero(
            id=int(data["id"]),
            name=str(data["name"]),
            description=str(data["description"]),
            hero_class=HeroClass["MAGE"],
            hero_power=HeroPower["FIREBLAST"],
            health=int(data["health"]),
            mana=int(data["mana"]),
            armor=int(data["armor"])
        )
        return True
    except (KeyError, ValueError, TypeError):
        return False
