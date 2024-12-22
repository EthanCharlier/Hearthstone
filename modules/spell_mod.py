#!/usr/bin/python3

# Imports

# Constants Imports
from utils.constants import DATABASE_PATH

# Modules Imports
from modules.card_mod import Card
from utils.database_utils import Database

# Enum Imports
from enums.card_class_enum import CardClass
from enums.card_type_enum import CardType
from enums.rarity_enum import Rarity

# Class
class Spell(Card):
    """
    Represents a spell card in a card game. Spell cards usually have special 
    effects or abilities that are executed when played. Unlike unit cards, 
    they do not have attack or health attributes.

    Attributes:
        id (int): Unique identifier for the card.
        name (str): Name of the card.
        cost (int): Mana or resource cost to play the card, cannot be negative, 10 is the maximum.
        description (str): Textual description of the card's effects or abilities.
        card_class (CardClass): The class associated with the card (e.g., Mage, Warrior).
        card_type (CardType): The type of the card (should always be `CardType.SPELL` for this class).
        card_rarity (Rarity): The rarity of the card (e.g., Common, Rare, Epic, Legendary).
        effects (list): A list of effects or abilities that the spell performs (default: empty list).

    Raises:
        ValueError: If `card_type` is not `CardType.SPELL`.
    """

    def __init__(self,
                id: int, 
                name: str, 
                cost: int, 
                description: str, 
                card_class: CardClass, 
                card_type: CardType, 
                card_rarity: Rarity, 
                effects: list = []
                ) -> None:
        """
        Initializes a Spell card with its attributes.

        Args:
            id (int): A unique identifier for the spell card.
            name (str): The name of the spell card.
            cost (int): The mana or resource cost to play this card, cannot be negative, 10 is the maximum.
            description (str): A description of the spell's effects or abilities.
            card_class (CardClass): The class associated with the card (e.g., Mage, Warrior).
            card_type (CardType): The type of the card, which must be `CardType.SPELL`.
            card_rarity (Rarity): The rarity of the card, which must be a valid `Rarity` enum.
            effects (list): A list of special effects or abilities the spell performs (default: empty list).

        Raises:
            ValueError: If `card_type` is not `CardType.SPELL`.
        """
        super().__init__(id, name, cost, description, card_class, card_type, card_rarity)

        if not isinstance(card_type, CardType) or card_type != CardType.SPELL:
            raise ValueError(f"Invalid card type: {card_type}. Must be CardType.SPELL.")
        
        self.effects = effects

        self.save_to_table()

    def save_to_table(self) -> None:
        """
        Saves the current Spell instance to a single table within the hearthstone_database.json file.
        """
        spells_db = Database.initialize_database(DATABASE_PATH)
        Database.insert_data_to_table(spells_db, "Spells", [self.to_dict()])
        spells_db.close()

    def to_dict(self) -> dict:
        """
        Converts the Spell object into a dictionary for serialization or storage.

        Returns:
            dict: A dictionary representation of the spell, including:
                  - ID
                  - Name
                  - Cost
                  - Description
                  - Card class
                  - Card type
                  - Card rarity
                  - Effects
        """
        return {
            "id": self.id,
            "name": self.name,
            "cost": self.cost,
            "description": self.description,
            "card_class": self.card_class.value,
            "card_type": self.card_type.value,
            "card_rarity": self.card_rarity.value,
            "effects": self.effects,
        }
