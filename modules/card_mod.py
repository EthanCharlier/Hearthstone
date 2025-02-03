#!/usr/bin/python3

# Constants Imports
from utils.constants import (
    CARD_MAXIMUM_ATTACK,
    CARD_MAXIMUM_ARMOR,
    CARD_MAXIMUM_HEALTH,
    HERO_MAXIMUM_MANA
)

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
        id (int): Unique identifier for the card.
        name (str): Name of the card.
        cost (int): Mana or resource cost to play the card (0 to HERO_MAXIMUM_MANA if defined).
        description (str): Description of the card's effects or abilities.
        card_classes (list[CardClass]): The classes associated with the card.
        card_type (CardType): The type of the card.
        card_rarity (Rarity): The rarity of the card.
        status (CardStatus): The status of the card.
        attack (int): The attack value of the card (0 to MAX_CARD_ATTACK if defined).
        health (int): The health value of the card (0 to MAX_CARD_HEALTH if defined).
        armor (int): The armor value of the card (0 to MAX_CARD_ARMOR if defined).
    """

    def __init__(self,
                id: int, 
                name: str, 
                cost: int, 
                description: str, 
                card_classes: list[CardClass], 
                card_type: CardType, 
                card_rarity: Rarity,
                status: CardStatus = CardStatus.IN_DECK,
                attack: int = 0,
                health: int = 0,
                armor: int = 0
                ) -> None:
        """
        Initializes a Card object with its attributes.

        Args:
            id (int): Unique identifier for the card.
            name (str): Name of the card.
            cost (int): The mana cost (0-10).
            description (str): Description of the card.
            card_classes (list[CardClass]): Associated classes.
            card_type (CardType): The card type.
            card_rarity (Rarity): The card rarity.
            status (CardStatus): The current status.
            attack (int): The attack value (0 to MAX_CARD_ATTACK if defined).
            health (int): The health value (0 to MAX_CARD_HEALTH if defined).
            armor (int): The armor value (0 to MAX_CARD_ARMOR if defined).

        Raises:
            ValueError: If any value is invalid.
        """
        self.id = id
        self.name = name

        if cost < 0:
            raise ValueError(f"Invalid cost: {cost}. Cost cannot be negative.")
        self.cost = min(cost, HERO_MAXIMUM_MANA) if HERO_MAXIMUM_MANA is not None else cost

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

        if attack < 0:
            raise ValueError(f"Invalid attack: {attack}. Attack cannot be negative.")
        self.attack = min(attack, CARD_MAXIMUM_ATTACK) if CARD_MAXIMUM_ATTACK is not None else attack

        if health < 0:
            raise ValueError(f"Invalid health: {health}. Health cannot be negative.")
        self.health = min(health, CARD_MAXIMUM_HEALTH) if CARD_MAXIMUM_HEALTH is not None else health

        if armor < 0:
            raise ValueError(f"Invalid armor: {armor}. Armor cannot be negative.")
        self.armor = min(armor, CARD_MAXIMUM_ARMOR) if CARD_MAXIMUM_ARMOR is not None else armor

    def take_damage(self, amount: int) -> None:
        """
        Apply damage to the card.

        Args:
            amount (int): The amount of damage to deal.
        """
        self.armor -= amount
        if self.armor < 0:
            self.health += self.armor
            self.armor = 0

    def apply_effects(self, spell_card: object) -> None:
        """
        Apply the effects of a spell card to this card.
        """
        if spell_card.health > 0:
            self.health = (min(self.health + spell_card.health, CARD_MAXIMUM_HEALTH)
                           if CARD_MAXIMUM_HEALTH is not None else self.health + spell_card.health)

        if spell_card.armor > 0:
            self.armor = (min(self.armor + spell_card.armor, CARD_MAXIMUM_ARMOR)
                          if CARD_MAXIMUM_ARMOR is not None else self.armor + spell_card.armor)

        if spell_card.attack > 0:
            self.attack = (min(self.attack + spell_card.attack, CARD_MAXIMUM_ATTACK)
                           if CARD_MAXIMUM_ATTACK is not None else self.attack + spell_card.attack)

    def to_dict(self) -> dict:
        """
        Converts the Card object into a dictionary for serialization or storage.

        Returns:
            dict: A dictionary representation of the card.
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
            "attack": self.attack,
            "health": self.health,
            "armor": self.armor,
        }
