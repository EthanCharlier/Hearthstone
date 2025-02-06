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

        # Validate if the race is an instance of Race enum
        if not isinstance(unit_race, Race):
            raise ValueError(f"Invalid race: {unit_race}. Must be a Race enum.")
        self.unit_race = unit_race

        # Ensure cost, attack, health, and armor do not exceed the maximum allowed values
        self.cost = min(self.cost, HERO_MAXIMUM_MANA) if HERO_MAXIMUM_MANA is not None else self.cost
        self.attack = min(self.attack, CARD_MAXIMUM_ATTACK) if CARD_MAXIMUM_ATTACK is not None else self.attack
        self.health = min(self.health, CARD_MAXIMUM_HEALTH) if CARD_MAXIMUM_HEALTH is not None else self.health
        self.armor = min(self.armor, CARD_MAXIMUM_ARMOR) if CARD_MAXIMUM_ARMOR is not None else self.armor

        # Save the card to the database
        self.save_to_table()

    def save_to_table(self) -> None:
        """
        Saves the current Unit instance to a specific table in the hearthstone_database.json file.

        This function converts the Unit object to a dictionary and inserts it into the database.
        """
        # Initialize the database
        units_db = Database.initialize_database(DATABASE_PATH)

        # Insert the Unit into the "Units" table
        Database.insert_data_to_table(units_db, "Units", [self.to_dict()])

        # Close the database connection
        units_db.close()

    def take_damage(self, amount: int) -> None:
        """
        Apply damage to the unit by reducing its armor first. If armor is exhausted, damage is applied to health.

        Args:
            amount (int): The amount of damage to deal to the unit.
        """
        self.armor -= amount  # Reduce armor first
        if self.armor < 0:
            # If armor is exhausted, apply the remaining damage to health
            self.health += self.armor
            self.armor = 0  # Set armor to 0 as it's depleted

    def attack_player_or_unit(self, target: Union[Card, "Player"]) -> None:
        """
        Attacks a target, reducing its health by the unit's attack value.

        Args:
            target (Card or Player): The target to attack (either a card or a player).

        Raises:
            ValueError: If the unit's attack value is zero or less.
            AttributeError: If the target doesn't have a `take_damage` method.
        """
        # Ensure the unit has a valid attack value
        if self.attack <= 0:
            raise ValueError(f"{self.name} cannot attack because its attack value is zero or less.")
        
        # Check if the target has the `take_damage` method (i.e., it can take damage)
        if not hasattr(target, "take_damage"):
            raise AttributeError(f"{target} does not have a `take_damage(amount)` method.")

        # Inflict damage on the target
        target.take_damage(self.attack)

    def to_dict(self) -> dict:
        """
        Converts the Unit object into a dictionary for serialization or storage in the database.

        Returns:
            dict: A dictionary representation of the unit, suitable for database insertion.
        """
        return {
            "id": self.id,  # Card's unique ID
            "name": self.name,  # Name of the unit
            "cost": self.cost,  # Cost of the unit
            "description": self.description,  # Description of the unit's abilities or effects
            "card_classes": [cls.value for cls in self.card_classes],  # List of card classes (converted to their values)
            "card_type": self.card_type.value,  # Type of card (always `CardType.UNIT` for this class)
            "card_rarity": self.card_rarity.value,  # Rarity of the unit card
            "status": self.status.value,  # Current status of the unit (e.g., IN_DECK)
            "unit_race": self.unit_race.value,  # The race of the unit (converted to value)
            "attack": self.attack,  # The attack value of the unit
            "health": self.health,  # The health value of the unit
            "armor": self.armor,  # The armor value of the unit
        }
