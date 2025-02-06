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
    for other specific types of cards, such as Unit cards or Spell cards.

    Attributes:
        id (int): Unique identifier for the card.
        name (str): Name of the card.
        cost (int): Mana or resource cost to play the card (0 to HERO_MAXIMUM_MANA if defined).
        description (str): Description of the card's effects or abilities.
        card_classes (list[CardClass]): The classes associated with the card.
        card_type (CardType): The type of the card.
        card_rarity (Rarity): The rarity of the card.
        status (CardStatus): The current status of the card (e.g., in deck, in hand).
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
            card_classes (list[CardClass]): List of associated classes for the card.
            card_type (CardType): The type of the card (e.g., Spell, Unit).
            card_rarity (Rarity): The rarity of the card (e.g., Common, Rare).
            status (CardStatus): The current status of the card (default is IN_DECK).
            attack (int): The attack value (0 to MAX_CARD_ATTACK if defined).
            health (int): The health value (0 to MAX_CARD_HEALTH if defined).
            armor (int): The armor value (0 to MAX_CARD_ARMOR if defined).

        Raises:
            ValueError: If any value is invalid (e.g., negative cost, attack, health, etc.).
        """
        self.id = id  # Set the unique identifier for the card
        self.name = name  # Set the name of the card

        # Validate the cost of the card, it should not be negative
        if cost < 0:
            raise ValueError(f"Invalid cost: {cost}. Cost cannot be negative.")
        # Set the cost, limiting it to HERO_MAXIMUM_MANA if defined
        self.cost = min(cost, HERO_MAXIMUM_MANA) if HERO_MAXIMUM_MANA is not None else cost

        self.description = description  # Set the description of the card

        # Validate that all card_classes are instances of CardClass
        if not all(isinstance(cls, CardClass) for cls in card_classes):
            raise ValueError("Invalid card classes: All elements in card_classes must be instances of CardClass.")
        self.card_classes = card_classes  # Set the list of card classes associated with the card

        # Validate that card_type is an instance of CardType
        if not isinstance(card_type, CardType):
            raise ValueError(f"Invalid card type: {card_type}. Must be a CardType enum.")
        self.card_type = card_type  # Set the card type (e.g., Spell, Unit)

        # Validate that card_rarity is an instance of Rarity
        if not isinstance(card_rarity, Rarity):
            raise ValueError(f"Invalid rarity: {card_rarity}. Must be a Rarity enum.")
        self.card_rarity = card_rarity  # Set the card rarity (e.g., Common, Rare)
        
        # Validate that status is an instance of CardStatus
        if not isinstance(status, CardStatus):
            raise ValueError(f"Invalid status: {status}. Must be a CardStatus enum.")
        self.status = status  # Set the status of the card (e.g., IN_DECK, IN_HAND)

        # Validate that attack is non-negative
        if attack < 0:
            raise ValueError(f"Invalid attack: {attack}. Attack cannot be negative.")
        # Set the attack value, limiting it to CARD_MAXIMUM_ATTACK if defined
        self.attack = min(attack, CARD_MAXIMUM_ATTACK) if CARD_MAXIMUM_ATTACK is not None else attack

        # Validate that health is non-negative
        if health < 0:
            raise ValueError(f"Invalid health: {health}. Health cannot be negative.")
        # Set the health value, limiting it to CARD_MAXIMUM_HEALTH if defined
        self.health = min(health, CARD_MAXIMUM_HEALTH) if CARD_MAXIMUM_HEALTH is not None else health

        # Validate that armor is non-negative
        if armor < 0:
            raise ValueError(f"Invalid armor: {armor}. Armor cannot be negative.")
        # Set the armor value, limiting it to CARD_MAXIMUM_ARMOR if defined
        self.armor = min(armor, CARD_MAXIMUM_ARMOR) if CARD_MAXIMUM_ARMOR is not None else armor

    def take_damage(self, amount: int) -> None:
        """
        Applies damage to the card, reducing its armor and potentially its health.

        Args:
            amount (int): The amount of damage to apply.
        """
        self.armor -= amount  # Subtract damage from the armor
        if self.armor < 0:  # If armor is less than 0, reduce health by the remaining damage
            self.health += self.armor  # Deduct the negative armor value from health
            self.armor = 0  # Set armor to 0 as it has been depleted

    def apply_effects(self, spell_card: object) -> None:
        """
        Applies the effects of a spell card to this card, modifying its health, armor, and attack values.

        Args:
            spell_card (object): The spell card whose effects will be applied to this card.
        """
        # Apply health change from spell card, limiting to CARD_MAXIMUM_HEALTH if defined
        if spell_card.health > 0:
            self.health = (min(self.health + spell_card.health, CARD_MAXIMUM_HEALTH)
                           if CARD_MAXIMUM_HEALTH is not None else self.health + spell_card.health)

        # Apply armor change from spell card, limiting to CARD_MAXIMUM_ARMOR if defined
        if spell_card.armor > 0:
            self.armor = (min(self.armor + spell_card.armor, CARD_MAXIMUM_ARMOR)
                          if CARD_MAXIMUM_ARMOR is not None else self.armor + spell_card.armor)

        # Apply attack change from spell card, limiting to CARD_MAXIMUM_ATTACK if defined
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
            "id": self.id,  # The unique ID of the card
            "name": self.name,  # The name of the card
            "cost": self.cost,  # The cost of the card
            "description": self.description,  # The description of the card's effects
            "card_classes": [cls.value for cls in self.card_classes],  # The card classes as a list of values
            "card_type": self.card_type.value,  # The card type as its value (e.g., "Unit")
            "card_rarity": self.card_rarity.value,  # The card rarity as its value (e.g., "Common")
            "status": self.status.value,  # The card's status as its value (e.g., "IN_DECK")
            "attack": self.attack,  # The attack value of the card
            "health": self.health,  # The health value of the card
            "armor": self.armor,  # The armor value of the card
        }
