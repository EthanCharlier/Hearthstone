#!/usr/bin/python3

# Imports
from __future__ import annotations

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
        """
        self.name = name
        self.hero = hero
        self.deck = deck

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
        if card.cost > self._mana:
            raise ValueError(f"Not enough mana to play {card.name}. Requires {card.cost} mana, but you have {self._mana}.")
        self._mana -= card.cost
        self.deck.play_card(card)

    def take_damage(self, amount: int) -> None:
        """
        Apply damage to the player.

        Args:
            amount (int): The amount of damage to deal.
        """
        self._armor -= amount
        if self._armor < 0:
            self._health += self._armor
            self._armor = 0

    def attack_player(self, target: Player) -> None:  #TODO: Think about split or note attack player and attack unit
        """
        Attacks a target, reducing its health by the hero's attack value.

        Args:
            target: The target to attack. The target must have a `take_damage(amount)` method.

        Raises:
            ValueError: If the hero's attack value is zero or less.
        """
        if self._attack <= 0:
            raise ValueError("The hero cannot attack because their attack value is zero or less.")
        target.take_damage(self._attack)

    @property
    def attack(self) -> int:
        """
        Getter for the player's attack.
        """
        return self._attack

    @attack.setter
    def attack(self, amount: int) -> None:
        """
        Sets the player's attack, ensuring it stays within valid bounds.
        """
        self._attack += amount
        if self.max_attack is not None:
            self._attack = min(self._attack, self.max_attack)

    @property
    def health(self) -> int:
        """
        Getter for the player's health.
        """
        return self._health

    @health.setter
    def health(self, amount: int) -> None:
        """
        Sets the player's health, ensuring it stays within valid bounds.
        """
        self._health += amount
        if self.max_health is not None:
            self._health = min(self._health, self.max_health)

    @property
    def mana(self) -> int:
        """
        Getter for the player's mana.
        """
        return self._mana

    @mana.setter
    def mana(self, amount: int) -> None:
        """
        Sets the player's mana, ensuring it stays within valid bounds.
        """
        self._mana += amount
        if self.max_mana is not None:
            self._mana = min(self._mana, self.max_mana)

    @property
    def armor(self) -> int:
        """
        Getter for the player's armor.
        """
        return self._armor

    @armor.setter
    def armor(self, amount: int) -> None:
        """
        Sets the player's armor, ensuring it stays within valid bounds.
        """
        self._armor += amount
        if self.max_armor is not None:
            self._armor = min(self._armor, self.max_armor)

    def reset(self) -> None:  #TODO
        """
        Reset the player's state for a new game.
        """
        self.health = self.hero.health
        self.mana = self.hero.mana
        self.deck.reset_deck()
        self.deck.hand.clear()
        self.deck.board.clear()
        self.deck.graveyard.clear()

    def __str__(self) -> str:  #TODO
        """
        String representation of the player.

        Returns:
            str: Player's status as a string.
        """
        return f"{self.name}, Hero: {self.hero.name}, Health: {self._health}/{self.max_health}, Mana: {self._mana}/{self.max_mana}"
