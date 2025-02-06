#!/usr/bin/python3

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
from utils.database_utils import Database

# Enum Imports
from enums.card_class_enum import CardClass
from enums.card_type_enum import CardType
from enums.rarity_enum import Rarity
from enums.card_status_enum import CardStatus

# Class
class Spell(Card):
    """
    Represents a spell card in a card game. Spell cards usually have special 
    effects or abilities that are executed when played.

    Attributes:
        id (int): Unique identifier for the card.
        name (str): Name of the card.
        cost (int): Mana or resource cost to play the card.
        description (str): Textual description of the card's effects or abilities.
        card_classes (list[CardClass]): The classes associated with the card.
        card_rarity (Rarity): The rarity of the card.
        status (CardStatus): The current status of the card (e.g., IN_DECK, PLAYED).
        attack (int): Attack value (default: 0, cannot be negative).
        health (int): Health value (default: 0, cannot be negative).
        armor (int): Armor value (default: 0, cannot be negative).
    """

    def __init__(self,
                id: int, 
                name: str, 
                cost: int, 
                description: str, 
                card_classes: list[CardClass], 
                card_rarity: Rarity, 
                status: CardStatus = CardStatus.IN_DECK,
                attack: int = 0,
                health: int = 0,
                armor: int = 0
                ) -> None:
        """
        Initializes a Spell card with its attributes.

        Args:
            id (int): A unique identifier for the spell card.
            name (str): The name of the spell card.
            cost (int): The mana or resource cost to play this card.
            description (str): A description of the spell's effects or abilities.
            card_classes (list[CardClass]): The classes associated with the card.
            card_rarity (Rarity): The rarity of the card.
            status (CardStatus): The current status of the card.
            attack (int): The attack value of the spell (default: 0).
            health (int): The health value of the spell (default: 0).
            armor (int): The armor value of the spell (default: 0).

        Raises:
            ValueError: If `attack`, `health`, or `armor` is negative.
        """
        # Initialize the parent Card class with basic attributes and set the type as SPELL
        super().__init__(id, name, cost, description, card_classes, CardType.SPELL, card_rarity, status, attack, health, armor)

        # Ensure the cost, attack, health, and armor do not exceed the maximum allowed values
        self.cost = min(self.cost, HERO_MAXIMUM_MANA) if HERO_MAXIMUM_MANA is not None else self.cost
        self.attack = min(self.attack, CARD_MAXIMUM_ATTACK) if CARD_MAXIMUM_ATTACK is not None else self.attack
        self.health = min(self.health, CARD_MAXIMUM_HEALTH) if CARD_MAXIMUM_HEALTH is not None else self.health
        self.armor = min(self.armor, CARD_MAXIMUM_ARMOR) if CARD_MAXIMUM_ARMOR is not None else self.armor

        # Save the spell card to the database
        self.save_to_table()

    def save_to_table(self) -> None:
        """
        Saves the current Spell instance to a specific table in the hearthstone_database.json file.

        This method accesses the database, adds the spell data as a new entry, and then closes the connection.
        """
        # Initialize the database and insert the Spell card data
        spells_db = Database.initialize_database(DATABASE_PATH)
        Database.insert_data_to_table(spells_db, "Spells", [self.to_dict()])
        spells_db.close()  # Close the database connection after saving

    def to_dict(self) -> dict:
        """
        Converts the Spell object into a dictionary for serialization or storage.

        This method is used to prepare the Spell instance for saving into a database.

        Returns:
            dict: A dictionary representation of the spell, including its attributes and values.
        """
        return {
            "id": self.id,  # Card's unique ID
            "name": self.name,  # Name of the spell card
            "cost": self.cost,  # Cost of casting the spell
            "description": self.description,  # Description of the spell's effects or abilities
            "card_classes": [cls.value for cls in self.card_classes],  # List of card classes (converted to their values)
            "card_type": self.card_type.value,  # Type of the card (always `CardType.SPELL` for this class)
            "card_rarity": self.card_rarity.value,  # Rarity of the spell card
            "status": self.status.value,  # Current status of the card (e.g., IN_DECK, PLAYED)
            "attack": self.attack,  # Attack value of the spell
            "health": self.health,  # Health value of the spell
            "armor": self.armor  # Armor value of the spell
        }
