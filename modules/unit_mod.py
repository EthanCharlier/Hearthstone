#!/usr/bin/python3

# Imports
from typing import Union

# Constants Imports
from utils.constants import (
    DATABASE_PATH,
    CARD_MAXIMUM_ATTACK,
    CARD_MAXIMUM_ARMOR,
    CARD_MAXIMUM_HEALTH,
    HERO_MAXIMUM_MANA
)

# Modules Imports
from modules.card_mod import Card
from modules.player_mod import Player
from utils.database_utils import Database

# Enum Imports
from enums.card_class_enum import CardClass
from enums.card_type_enum import CardType
from enums.rarity_enum import Rarity
from enums.race_enum import Race
from enums.card_status_enum import CardStatus

# Class
class Unit(Card):
    """
    Represents a unit card in a card game. A unit card has additional attributes 
    such as attack, health, race, and special effects that differentiate it 
    from other card types like spells.

    Attributes:
        id (int): Unique identifier for the card.
        name (str): Name of the card.
        cost (int): Mana or resource cost to play the card.
        description (str): Textual description of the card's effects or abilities.
        card_classes (list[CardClass]): The classes associated with the card.
        card_type (CardType): The type of the card (should always be `CardType.UNIT` for this class).
        card_rarity (Rarity): The rarity of the card.
        unit_race (Race): The race of the unit.
        status (CardStatus): The current status of the card.
        attack (int): The attack value of the unit.
        health (int): The health value of the unit.
        armor (int): The armor value of the unit.
    """

    def __init__(self, 
                id: int, 
                name: str, 
                cost: int,
                description: str, 
                card_classes: list[CardClass], 
                card_rarity: Rarity, 
                unit_race: Race, 
                status: CardStatus = CardStatus.IN_DECK, 
                attack: int = 0, 
                health: int = 0, 
                armor: int = 0
                ) -> None:
        """
        Initializes a Unit card with its attributes.

        Args:
            id (int): A unique identifier for the unit card.
            name (str): The name of the unit card.
            cost (int): The mana or resource cost to play this card.
            description (str): A description of the unit's effects or abilities.
            card_classes (list[CardClass]): The classes associated with the card.
            card_rarity (Rarity): The rarity of the card.
            unit_race (Race): The race of the unit.
            status (CardStatus): The current status of the card.
            attack (int): The attack value of the unit.
            health (int): The health value of the unit.
            armor (int): The armor value of the unit.

        Raises:
            ValueError: If `unit_race` is not an instance of `Race`.
        """
        super().__init__(id, name, cost, description, card_classes, CardType.UNIT, card_rarity, status, attack, health, armor)

        if not isinstance(unit_race, Race):
            raise ValueError(f"Invalid race: {unit_race}. Must be a Race enum.")
        self.unit_race = unit_race

        self.cost = min(self.cost, HERO_MAXIMUM_MANA) if HERO_MAXIMUM_MANA is not None else self.cost
        self.attack = min(self.attack, CARD_MAXIMUM_ATTACK) if CARD_MAXIMUM_ATTACK is not None else self.attack
        self.health = min(self.health, CARD_MAXIMUM_HEALTH) if CARD_MAXIMUM_HEALTH is not None else self.health
        self.armor = min(self.armor, CARD_MAXIMUM_ARMOR) if CARD_MAXIMUM_ARMOR is not None else self.armor

        self.save_to_table()

    def save_to_table(self) -> None:
        """
        Saves the current Unit instance to a single table within the hearthstone_database.json file.
        """
        units_db = Database.initialize_database(DATABASE_PATH)
        Database.insert_data_to_table(units_db, "Units", [self.to_dict()])
        units_db.close()

    def take_damage(self, amount: int) -> None:
        """
        Apply damage to the unit.

        Args:
            amount (int): The amount of damage to deal.
        """
        self.armor -= amount
        if self.armor < 0:
            self.health += self.armor
            self.armor = 0

    def attack_player_or_unit(self, target: Union[Card, "Player"]) -> None:
        """
        Attacks a target, reducing its health by the unit's attack value.

        Args:
            target (Card or Unit): The target to attack.

        Raises:
            ValueError: If the unit's attack value is zero or less.
        """
        if self.attack <= 0:
            raise ValueError(f"{self.name} cannot attack because its attack value is zero or less.")
        
        if not hasattr(target, "take_damage"):
            raise AttributeError(f"{target} does not have a `take_damage(amount)` method.")

        target.take_damage(self.attack)

    def to_dict(self) -> dict:
        """
        Converts the Unit object into a dictionary for serialization or storage.

        Returns:
            dict: A dictionary representation of the unit.
        """
        return {
            "id": self.id,
            "name": self.name,
            "cost": self.cost,
            "description": self.description,
            "card_classes": [cls.value for cls in self.card_classes],
            "card_type": self.card_type.value,
            "card_rarity": self.card_rarity.value,
            "status": self.status.value,
            "unit_race": self.unit_race.value,
            "attack": self.attack,
            "health": self.health,
            "armor": self.armor,
        }
