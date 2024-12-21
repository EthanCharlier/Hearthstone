#!/usr/bin/python3

# Imports
from tinydb import TinyDB, Query

# Constants Imports
from utils.constants import SPELLS_DB_PATH

# Modules Imports
from models.card_mod import Card
from utils.database_utils import DatabaseUtils

# Enum Imports
from utils.card_type_enum import CardType
from utils.rarity_enum import Rarity

# Class
class Spell(Card):
    """
    Represents a spell card in a card game. Spell cards usually have special 
    effects or abilities that are executed when played. Unlike unit cards, 
    they do not have attack or health attributes.

    Attributes:
        id (int): Unique identifier for the card.
        name (str): Name of the card.
        cost (int): Mana or resource cost to play the card, cannot be negative.
        description (str): Textual description of the card's effects or abilities.
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
                card_type: CardType, 
                card_rarity: Rarity, 
                effects: list = []
                ) -> None:
        """
        Initializes a Spell card with its attributes.

        Args:
            id (int): A unique identifier for the spell card.
            name (str): The name of the spell card.
            cost (int): The mana or resource cost to play this card, cannot be negative.
            description (str): A description of the spell's effects or abilities.
            card_type (CardType): The type of the card, which must be `CardType.SPELL`.
            card_rarity (Rarity): The rarity of the card, which must be a valid `Rarity` enum.
            effects (list): A list of special effects or abilities the spell performs (default: empty list).

        Raises:
            ValueError: If `card_type` is not `CardType.SPELL`.
        """
        super().__init__(id, name, cost, description, card_type, card_rarity)

        if not isinstance(card_type, CardType) or card_type != CardType.SPELL:
            raise ValueError(f"Invalid card type: {card_type}. Must be CardType.SPELL.")
        
        self.effects = effects

        with DatabaseUtils.initialize_database(SPELLS_DB_PATH) as spells_db:
            spells_db.insert(self.to_dict())

    def to_dict(self) -> dict:
        """
        Converts the Spell object into a dictionary for serialization or storage.

        Returns:
            dict: A dictionary representation of the spell, including:
                  - ID
                  - Name
                  - Cost
                  - Description
                  - Card type
                  - Card rarity
                  - Effects
        """
        return {
            "id": self.id,
            "name": self.name,
            "cost": self.cost,
            "description": self.description,
            "card_type": self.card_type.value,
            "card_rarity": self.card_rarity.value,
            "effects": self.effects,
        }
