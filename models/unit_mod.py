#!/usr/bin/python3

# Imports

# Constants Imports
from utils.constants import DATABASE_PATH

# Modules Imports
from models.card_mod import Card
from utils.database_utils import Database

# Enum Imports
from utils.card_type_enum import CardType
from utils.rarity_enum import Rarity
from utils.race_enum import Race

# Class
class Unit(Card):
    """
    Represents a unit card in a card game. A unit card has additional attributes 
    such as attack, health, race, and special effects that differentiate it 
    from other card types like spells.

    Attributes:
        id (int): Unique identifier for the card.
        name (str): Name of the card.
        cost (int): Mana or resource cost to play the card, cannot be negative, 10 is the maximum.
        description (str): Textual description of the card's effects or abilities.
        card_type (CardType): The type of the card (should always be `CardType.UNIT` for this class).
        card_rarity (Rarity): The rarity of the card (e.g., Common, Rare, Epic, Legendary).
        unit_race (Race): The race or category of the unit (e.g., Beast, Dragon).
        attack (int): The attack value of the unit (default: 0, cannot be negative).
        health (int): The health value of the unit (default: 0, cannot be negative).
        armor (int): The armor value of the unit (default: 0, cannot be negative).
        effects (list): List of special effects or abilities the unit has (default: empty list).

    Raises:
        ValueError: If `card_type` is not `CardType.UNIT`.
        ValueError: If `unit_race` is not an instance of `Race`.
        ValueError: If `attack`, `health`, or `armor` is negative.
    """

    def __init__(self, 
                id: int, 
                name: str, 
                cost: int, 
                description: str, 
                card_type: CardType, 
                card_rarity: Rarity, 
                unit_race: Race, 
                attack: int = 0, 
                health: int = 0, 
                armor: int = 0, 
                effects: list = []
                ) -> None:
        """
        Initializes a Unit card with its attributes.

        Args:
            id (int): A unique identifier for the unit card.
            name (str): The name of the unit card.
            cost (int): The mana or resource cost to play this card, cannot be negative, 10 is the maximum.
            description (str): A description of the unit's effects or abilities.
            card_type (CardType): The type of the card, which must be `CardType.UNIT`.
            card_rarity (Rarity): The rarity of the card, which must be a valid `Rarity` enum.
            unit_race (Race): The race of the unit, which must be a valid `Race` enum.
            attack (int): The attack value of the unit (default: 0, cannot be negative).
            health (int): The health value of the unit (default: 0, cannot be negative).
            armor (int): The armor value of the unit (default: 0, cannot be negative).
            effects (list): A list of special effects or abilities the unit has (default: empty list).

        Raises:
            ValueError: If `card_type` is not `CardType.UNIT`.
            ValueError: If `unit_race` is not an instance of `Race`.
            ValueError: If `attack`, `health`, or `armor` is negative.
        """
        super().__init__(id, name, cost, description, card_type, card_rarity)

        if not isinstance(card_type, CardType) or card_type != CardType.UNIT:
            raise ValueError(f"Invalid card type: {card_type}. Must be CardType.UNIT.")
        
        if not isinstance(unit_race, Race):
            raise ValueError(f"Invalid race: {unit_race}. Must be a Race enum.")
        self.unit_race = unit_race

        if attack < 0:
            raise ValueError(f"Invalid attack: {attack}. Attack cannot be negative.")
        if health < 0:
            raise ValueError(f"Invalid health: {health}. Health cannot be negative.")
        if armor < 0:
            raise ValueError(f"Invalid armor: {armor}. Armor cannot be negative.")

        self.attack = attack
        self.health = health
        self.armor = armor
        self.effects = effects

        self.save_to_table()

    def save_to_table(self) -> None:
        """
        Saves the current Unit instance to a single table within the hearthstone_database.json file.
        """
        units_db = Database.initialize_database(DATABASE_PATH)
        Database.insert_data_to_table(units_db, "Spells", [self.to_dict()])
        units_db.close()

    def to_dict(self) -> dict:
        """
        Converts the Unit object into a dictionary for serialization or storage.

        Returns:
            dict: A dictionary representation of the unit, including:
                  - ID
                  - Name
                  - Cost
                  - Description
                  - Card type
                  - Card rarity
                  - Unit race
                  - Attack
                  - Health
                  - Armor
                  - Effects
        """
        return {
            "id": self.id,
            "name": self.name,
            "cost": self.cost,
            "description": self.description,
            "card_type": self.card_type.value,
            "card_rarity": self.card_rarity.value,
            "unit_race": self.unit_race.value,
            "attack": self.attack,
            "health": self.health,
            "armor" : self.armor,
            "effects": self.effects,
        }
