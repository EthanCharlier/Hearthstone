#!/usr/bin/python3

# Imports
from enum import Enum

# Class
class CardStatus(Enum):
    """
    Represents the different states a card can be in during the game.

    Cards can be in the deck, in the player's hand, on the board, 
    or in the graveyard after being used or destroyed.
    """
    IN_DECK = "in_deck"
    IN_HAND = "in_hand"
    ON_BOARD = "on_board"
    IN_GRAVEYARD = "in_graveyard"
