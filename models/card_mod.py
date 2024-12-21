#!/usr/bin/python3

# Enum Imports
from utils.card_type_enum import CardType
from utils.rarity_enum import Rarity

# Class
class Card():
    """
    Represents a generic card in a card game. This class serves as the base class
    for other specific types of cards like Unit cards or Spell cards.

    Attributes:
        id (int): The unique identifier for the card.
        name (str): The name of the card.
        cost (int): The mana or resource cost to play the card, cannot be negative.
        description (str): A textual description of the card's effects or abilities.
        card_type (CardType): The type of the card (e.g., Unit, Spell).
        card_rarity (Rarity): The rarity of the card (e.g., Common, Rare, Epic, Legendary).

    Raises:
        ValueError: If `card_type` is not an instance of `CardType`.
        ValueError: If `card_rarity` is not an instance of `Rarity`.
        ValueError: If `cost` is negative.
    """

    def __init__(self,
                id: int, 
                name: str, 
                cost: int, 
                description: str, 
                card_type: CardType, 
                card_rarity: Rarity
                ) -> None:
        """
        Initializes a Card object with its attributes.

        Args:
            id (int): A unique identifier for the card.
            name (str): The name of the card.
            cost (int): The mana or resource cost required to play this card, cannot be negative.
            description (str): A description of the card's effects or abilities.
            card_type (CardType): The type of the card, which should be one of the options defined in the CardType enum.
            card_rarity (Rarity): The rarity of the card, which should be one of the options defined in the Rarity enum.

        Raises:
            ValueError: If `card_type` is not an instance of `CardType`.
            ValueError: If `card_rarity` is not an instance of `Rarity`.
            ValueError: If `cost` is negative.
        """
        self.id = id
        self.name = name

        if cost < 0:
            raise ValueError(f"Invalid cost: {cost}. Cost cannot be negative.")
        self.cost = cost

        self.description = description

        if not isinstance(card_type, CardType):
            raise ValueError(f"Invalid card type: {card_type}. Must be a CardType enum.")
        self.card_type = card_type

        if not isinstance(card_rarity, Rarity):
            raise ValueError(f"Invalid rarity: {card_rarity}. Must be a Rarity enum.")
        self.card_rarity = card_rarity

    def to_dict(self) -> dict:
        """
        Converts the Card object into a dictionary for serialization or storage.

        Returns:
            dict: A dictionary representation of the card, including:
                  - ID
                  - Name
                  - Cost
                  - Description
                  - Card type
                  - Card rarity
        """
        return {
            "id": self.id,
            "name": self.name,
            "cost": self.cost,
            "description": self.description,
            "card_type": self.card_type.value,
            "card_rarity": self.card_rarity.value,
        }