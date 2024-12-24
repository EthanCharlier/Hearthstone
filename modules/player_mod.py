#!/usr/bin/python3

# Modules Imports
from modules.deck_mod import Deck
from modules.hero_mod import Hero
from modules.card_mod import Card

# Enum Imports
from enums.card_status_enum import CardStatus

# Class
class Player:
    """
    """

    def __init__(self, name: str, hero: Hero, deck: Deck) -> None:
        """
        Initialize a Player.

        Args:
            name (str): The player's name.
            hero (Hero): The player's chosen hero.
            deck (Deck): The player's deck of cards.
        """
        self.name = name
        self.hero = hero
        self.deck = deck