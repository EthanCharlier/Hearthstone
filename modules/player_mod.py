#!/usr/bin/python3

# Imports
from __future__ import annotations
from typing import Union

# Constants Imports
from utils.constants import (
    CARD_MAXIMUM_ATTACK,
    CARD_MAXIMUM_ARMOR,
    CARD_MAXIMUM_HEALTH
)

# Modules Imports
from modules.deck_mod import Deck
from modules.hero_mod import Hero
from modules.card_mod import Card

# Class
class Player:
    """
    Represents a player in the card game.

    Attributes:
        name (str): The name of the player.
        attack (int): The player's current attack.
        health (int): The player's current health.
        mana (int): The player's current mana.
        armor (int): The player's current armor.
        hero (Hero): The hero associated with the player.
        deck (Deck): The player's deck of cards.
    """

    def __init__(self, name: str, hero: Hero, deck: Deck) -> None:
        """
        Initializes a Player object.

        Args:
            name (str): The name of the player.
            hero (Hero): The hero associated with the player.
            deck (Deck): The player's deck of cards.
        
        Raises:
            TypeError: If `name`, `hero`, or `deck` is not of the correct type.
        """
        # Ensure 'name' is a string
        if not isinstance(name, str):
            raise TypeError(f"Expected 'name' to be a Player, got {type(name).__name__}")
        self.name: str = name

        # Ensure 'hero' is an instance of Hero class
        if not isinstance(hero, Hero):
            raise TypeError(f"Expected 'hero' to be a Player, got {type(hero).__name__}")
        self.hero: Hero = hero

        # Ensure 'deck' is an instance of Deck class
        if not isinstance(deck, Deck):
            raise TypeError(f"Expected 'deck' to be a Deck, got {type(deck).__name__}")
        self.deck: Deck = deck

        # Initialize attack, health, mana, and armor based on the hero's values
        self._attack = hero.attack
        self.max_attack = hero.get_maximum_attack

        self._health = hero.health
        self.max_health = hero.get_maximum_health

        self._mana = hero.mana
        self.max_mana = hero.get_maximum_mana

        self._armor = hero.armor
        self.max_armor = hero.get_maximum_armor

    def draw_card(self) -> Card:
        """
        Draw a card from the deck.

        Returns:
            Card: The drawn card.

        Raises:
            ValueError: If the deck is empty or hand limit is reached.
        """
        return self.deck.draw()

    def play_card(self, card: Card) -> None:
        """
        Play a card from the player's hand to the board.

        Args:
            card (Card): The card to play.

        Raises:
            ValueError: If the player does not have enough mana or if the board is full.
        """
        # Check if the player has enough mana to play the card
        if card.cost > self._mana:
            raise ValueError(f"Not enough mana to play {card.name}. Requires {card.cost} mana, but you have {self._mana}.")
        
        # Deduct the mana for playing the card and play it
        self._mana -= card.cost
        self.deck.play_card(card)

    def take_damage(self, amount: int) -> None:
        """
        Apply damage to the player.

        Args:
            amount (int): The amount of damage to deal.
        """
        self._armor -= amount  # First, damage the armor
        if self._armor < 0:  # If armor is depleted, damage health
            self._health += self._armor  # Armor might make health go below zero
            self._armor = 0  # Reset armor to zero after it is depleted

    def attack_player_or_unit(self, target: Union[Card, "Player"]) -> None:
        """
        Attacks a target, reducing its health by the unit's attack value.

        Args:
            target (Card or Player): The target to attack.

        Raises:
            ValueError: If the unit's attack value is zero or less.
            AttributeError: If the target doesn't have a `take_damage` method.
        """
        # Ensure the player has a positive attack value
        if self._attack <= 0:
            raise ValueError(f"{self.name} cannot attack because its attack value is zero or less.")
        
        # Ensure the target has the method `take_damage`
        if not hasattr(target, "take_damage"):
            raise AttributeError(f"{target} does not have a `take_damage(amount)` method.")
        
        # Apply damage to the target
        target.take_damage(self._attack)

    def apply_effects(self, spell_card: object) -> None:
        """
        Apply the effects of a spell card to this player.

        Args:
            spell_card (object): The spell card whose effects to apply.
        """
        # Apply health, ensuring it doesn't exceed the maximum value
        if spell_card.health > 0:
            self._health = (min(self._health + spell_card.health, CARD_MAXIMUM_HEALTH)
                           if CARD_MAXIMUM_HEALTH is not None else self._health + spell_card.health)

        # Apply armor, ensuring it doesn't exceed the maximum value
        if spell_card.armor > 0:
            self._armor = (min(self._armor + spell_card.armor, CARD_MAXIMUM_ARMOR)
                          if CARD_MAXIMUM_ARMOR is not None else self._armor + spell_card.armor)

        # Apply attack, ensuring it doesn't exceed the maximum value
        if spell_card.attack > 0:
            self._attack = (min(self._attack + spell_card.attack, CARD_MAXIMUM_ATTACK)
                           if CARD_MAXIMUM_ATTACK is not None else self._attack + spell_card.attack)

    # Properties for attack, health, mana, and armor with getters and setters
    @property
    def attack(self) -> int:
        """
        Getter for the player's attack.

        Returns:
            int: The player's current attack value.
        """
        return self._attack

    @attack.setter
    def attack(self, amount: int) -> None:
        """
        Sets the player's attack, ensuring it stays within valid bounds.

        Args:
            amount (int): The new attack value to set.
        """
        self._attack = amount
        if self.max_attack is not None:
            self._attack = min(self._attack, self.max_attack)

    @property
    def health(self) -> int:
        """
        Getter for the player's health.

        Returns:
            int: The player's current health value.
        """
        return self._health

    @health.setter
    def health(self, amount: int) -> None:
        """
        Sets the player's health, ensuring it stays within valid bounds.

        Args:
            amount (int): The new health value to set.
        """
        self._health = amount
        if self.max_health is not None:
            self._health = min(self._health, self.max_health)

    @property
    def mana(self) -> int:
        """
        Getter for the player's mana.

        Returns:
            int: The player's current mana value.
        """
        return self._mana

    @mana.setter
    def mana(self, amount: int) -> None:
        """
        Sets the player's mana, ensuring it stays within valid bounds.

        Args:
            amount (int): The new mana value to set.
        """
        self._mana = amount
        if self.max_mana is not None:
            self._mana = min(self._mana, self.max_mana)

    @property
    def armor(self) -> int:
        """
        Getter for the player's armor.

        Returns:
            int: The player's current armor value.
        """
        return self._armor

    @armor.setter
    def armor(self, amount: int) -> None:
        """
        Sets the player's armor, ensuring it stays within valid bounds.

        Args:
            amount (int): The new armor value to set.
        """
        self._armor = amount
        if self.max_armor is not None:
            self._armor = min(self._armor, self.max_armor)

    def reset(self) -> None:
        """
        Reset the player's state for a new game.

        Resets the player's health, mana, deck, and clears hand, board, and graveyard.
        """
        self.health = self.hero.health  # Reset health to hero's base health
        self.mana = self.hero.mana  # Reset mana to hero's base mana
        self.deck.reset_deck()  # Reset the deck
        self.deck.hand.clear()  # Clear the hand
        self.deck.board.clear()  # Clear the board
        self.deck.graveyard.clear()  # Clear the graveyard

    def __str__(self) -> str:
        """
        String representation of the player.

        Returns:
            str: A string representing the player's name, hero, health, and mana.
        """
        return f"{self.name}, Hero: {self.hero.name}, Health: {self._health}/{self.max_health}, Mana: {self._mana}/{self.max_mana}"
