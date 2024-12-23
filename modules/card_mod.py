#!/usr/bin/python3

# Enum Imports
from enums.card_class_enum import CardClass
from enums.card_type_enum import CardType
from enums.rarity_enum import Rarity
from enums.card_status_enum import CardStatus

# Class
class Card():
    """
    Represents a generic card in a card game. This class serves as the base class
    for other specific types of cards like Unit cards or Spell cards.

    Attributes:
        id (int): The unique identifier for the card.
        name (str): The name of the card.
        cost (int): The mana or resource cost to play the card, cannot be negative, 10 is the maximum.
        description (str): A textual description of the card's effects or abilities.
        card_classes (list[CardClass]): The classes associated with the card (e.g., Mage, Warrior).
        card_type (CardType): The type of the card (e.g., Unit, Spell).
        card_rarity (Rarity): The rarity of the card (e.g., Common, Rare, Epic, Legendary).
        status (CardStatus): The status of the card (e.g, in_deck, in_hand, on_board, in_graveyard)

    Raises:
        ValueError: If `card_class` is not an instance of `CardClass`.
        ValueError: If `card_type` is not an instance of `CardType`.
        ValueError: If `card_rarity` is not an instance of `Rarity`.
        ValueError: If `status` is not an instance of `CardStatus`.
        ValueError: If `cost` is negative.
        ValueError: If `cost` is greater than 10.
    """

    def __init__(self,
                id: int, 
                name: str, 
                cost: int, 
                description: str, 
                card_classes: list[CardClass], 
                card_type: CardType, 
                card_rarity: Rarity,
                status: CardStatus = CardStatus.IN_DECK
                ) -> None:
        """
        Initializes a Card object with its attributes.

        Args:
            id (int): A unique identifier for the card.
            name (str): The name of the card.
            cost (int): The mana or resource cost required to play this card, cannot be negative, 10 is the maximum.
            description (str): A description of the card's effects or abilities.
            card_classes (list[CardClass]): The classes associated with the card (e.g., Mage, Warrior).
            card_type (CardType): The type of the card, which should be one of the options defined in the CardType enum.
            card_rarity (Rarity): The rarity of the card, which should be one of the options defined in the Rarity enum.
            status (CardStatus): The status of the card which should be one of the options defined in the CardStatus enum.

        Raises:
            ValueError: If `card_classes` is not all elements in are instance of `CardClass`.
            ValueError: If `card_type` is not an instance of `CardType`.
            ValueError: If `card_rarity` is not an instance of `Rarity`.
            ValueError: If `status` is not an instance of `CardStatus`.
            ValueError: If `cost` is negative.
            ValueError: If `cost` is greater than 10.
        """
        self.id = id
        self.name = name

        if cost < 0:
            raise ValueError(f"Invalid cost: {cost}. Cost cannot be negative.")
        elif cost > 10:
            raise ValueError(f"Invalid cost: {cost}. Cost cannot be greater than 10.")
        self.cost = cost

        self.description = description

        if not all(isinstance(cls, CardClass) for cls in card_classes):
            raise ValueError("Invalid card classes: All elements in card_classes must be instances of CardClass.")
        self.card_classes = card_classes

        if not isinstance(card_type, CardType):
            raise ValueError(f"Invalid card type: {card_type}. Must be a CardType enum.")
        self.card_type = card_type

        if not isinstance(card_rarity, Rarity):
            raise ValueError(f"Invalid rarity: {card_rarity}. Must be a Rarity enum.")
        self.card_rarity = card_rarity
        
        if not isinstance(status, CardStatus):
            raise ValueError(f"Invalid status: {status}. Must be a CardStatus enum.")
        self.status = status

    def to_dict(self) -> dict:
        """
        Converts the Card object into a dictionary for serialization or storage.

        Returns:
            dict: A dictionary representation of the card, including:
                  - ID
                  - Name
                  - Cost
                  - Description
                  - Card classes
                  - Card type
                  - Card rarity
                  - Status
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
        }
