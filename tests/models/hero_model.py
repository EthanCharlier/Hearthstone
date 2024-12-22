#!/usr/bin/python3

# Imports

# Modules Imports
from modules.hero_mod import Hero

# Enum Imports
from enums.card_class_enum import CardClass
from enums.hero_power_enum import HeroPower

# Script
def create_hero_by_model(data: dict) -> Hero:
    hero = Hero(
        id = data["id"],
        name = data["name"],
        description = data["description"],
        hero_class = CardClass[data["hero_class"]],
        hero_power = HeroPower[data["hero_power"]],
        health = data["health"],
        mana = data["mana"],
        armor = data["armor"]
    )
    return hero
